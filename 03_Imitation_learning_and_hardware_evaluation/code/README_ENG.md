# Teaching the SO-101 to pick up a yellow object and place it in a red container

[日本語版](./README_JPN.md)

These scripts train an ACT (Action Chunking with Transformers) policy on human-operated SO-101 demonstrations and run it on the follower arm. ACT uses a workspace camera image and six joint positions to predict a sequence of actions.

We collected 20 demonstrations. Using the checkpoint from training step 10,000, we observed the arm pick up the yellow object and place it in the red container. To measure how often it succeeds under consistent conditions, we prepared the four batches of five trials described below. Results from that 20-trial evaluation are pending.

## What each script does

| Script | Role |
|---|---|
| [train_act.py](./train_act.py) | Runs LeRobot’s `lerobot-train` on the recorded dataset. It sets the training and validation split, the number of training steps, and the checkpoint interval. |
| [evaluate_act.py](./evaluate_act.py) | Runs five trials per batch on the physical arm. For each trial, it records video, joint positions, and action commands. The operator enters the outcome (success, failure, or interrupted), which the script writes to a CSV file alongside the trial number. |
| [rollout_current_start.py](./rollout_current_start.py) | Starts one trial. It registers the camera adapter with LeRobot, reads the follower’s six joint positions, and sets the initial motor targets to those measured positions before continuing with the standard setup and ACT control. The operator sets the starting pose before each trial. |
| [so101_shared_camera.py](./so101_shared_camera.py) | Reads the `latest.jpg` file updated by the Windows camera publisher and supplies RGB images to LeRobot in Ubuntu on WSL2. It checks for a fresh frame when connecting and returns the latest available image during evaluation. |

## Train on the demonstrations

We used Ubuntu on WSL2, LeRobot 0.6.1, and PyTorch with CUDA support. Activate a virtual environment with LeRobot’s training dependencies installed. Run the following command from the directory containing the scripts. Set `--dataset` to the dataset directory containing `meta/info.json`.

```bash
python train_act.py \
  --dataset "$HOME/.cache/huggingface/lerobot/local/so101_yellow_pick_place_20_trimmed_v1" \
  --output runs/act_pick_place
```

The 20 demonstrations contain 15,540 frames in total. We split the data by demonstration, using 16 for training and four for validation. We trained for 10,000 steps in FP32 with a batch size of two. Validation ran every 2,000 steps, and checkpoints were saved every 5,000 steps. The lowest observed validation loss occurred at step 8,000. The saved checkpoints were from steps 5,000 and 10,000. We used the latter on the robot.

## Evaluate the trained policy on the robot

Start the workspace camera’s JPEG publisher on Windows and connect the calibrated follower to WSL2. Replace the example `PORT` and `JPEG` paths below with the follower’s USB device path and the publisher’s image path. Set `--model` to the `pretrained_model` directory containing the weights, configuration, and preprocessing and postprocessing files.

```bash
PORT="/dev/serial/by-id/YOUR_FOLLOWER_USB_ID"
JPEG="/mnt/c/Users/YOUR_WINDOWS_USERNAME/so101-camera-share/latest.jpg"

python evaluate_act.py --batch 1 \
  --model runs/act_pick_place/checkpoints/010000/pretrained_model \
  --port "$PORT" --jpeg "$JPEG" --output evaluation
```

1. Set the arm, yellow object, and red container to their starting positions. Clear your hands from the arm’s reach and press Enter to start one trial.
2. ACT predicts 100 actions from the camera image and joint positions. It executes those 100 actions before making its next prediction. The target control frequency is 30 Hz, and each trial has a 60-second limit.
3. Enter the outcome after each trial. The arm stays at its final pose with holding torque enabled. When resetting the setup, avoid forcing the arm by hand while the motors are holding position.
4. The command finishes after five trials. For the next batches, rerun it with `--batch 2`, `--batch 3`, and `--batch 4`. These cover trials 6–10, 11–15, and 16–20, respectively.

Each batch creates an `evaluation/batch<number>_<timestamp>/` directory. Its `results.csv` contains the batch number, trial number, dataset name, process exit code, and operator-reported outcome. Each trial dataset contains `videos/` for the workspace recording, `data/` for joint positions and action commands, and `meta/` for the recording format and counts.
