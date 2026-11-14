# Imitation Learning and Real-World Evaluation | Nov 13, 2026

### 3-1 Verification of the Training Environment

We confirmed that GPU-accelerated training using LeRobot and PyTorch can be executed within a WSL2/Ubuntu environment on Windows.

| Item | Verification Result |
|---|---|
| Execution Environment | WSL2/Ubuntu, Python virtual environment `lerobot` |
| Python | 3.12.3 |
| LeRobot | 0.6.1 |
| PyTorch | 2.11.0+cu130 |
| GPU | NVIDIA *****, VRAM ** GiB |
| PyTorch CUDA Usage | `True` |
| Accelerate | 1.15.0 (missing dependency added) |
| Dependency Check | `No broken requirements found.` |

We verified the functionality of small-scale matrix computations using CUDA, the loading of the ACT (Action Chunking with Transformers) model, and the execution of the training process. Pre-existing (saved) data was used for training.

#### Adjustments Made During Environment Setup

- Training failed to start because `accelerate` was not installed; this dependency was added, and the environment was re-verified.
- During dataset creation, the `libx264` codec specified in `RGBEncoderConfig` was not supported in this environment. The configuration value was changed to `h264` to complete the dataset creation.
- We reviewed the LeRobot source code and configuration in use, and tailored the scripts to match the installed version.

**Result: Confirmed an environment capable of training the ACT model using a GPU.**

### 3-2 Imitation Learning and Evaluation

We trained an ACT (Action Chunking with Transformers) model using 20 collected demonstration datasets. The trained model was evaluated on the actual hardware, where it successfully completed the task of picking up a yellow-green workpiece and placing it into a red container on its first attempt.

#### Training Configuration

ACT is a model that takes camera images and joint states as input to predict a sequence of actions across multiple time steps. Training was conducted using the following configuration:

| Item | Setting |
|---|---|
| Dataset | `local/so101_yellow_pick_place_20_trimmed_v1` |
| Split | 16 training episodes, 4 evaluation episodes |
| Number of frames in training data | 12,720 |
| Input | 1 RGB image of the workspace + 6-element joint state |
| Output | 6-element action |
| Image backbone | ResNet-18, with ImageNet pre-trained weights |
| Training steps | 10,000 |
| Batch size | 2 |
| Learning rate | `1e-5` |
| Numerical precision | FP32 (`use_amp=false`) |
| `chunk_size` / `n_action_steps` | 100 / 100 |
| Temporal ensemble | Not used |
| Evaluation interval | 2,000 steps |
| Checkpoint interval | 5,000 steps |
| Seed | 42 |

Training concluded in approximately 36 minutes and 29 seconds, with an exit code of 0.

#### Offline Evaluation

| Step | eval_loss |
|---:|---:|
| 2,000 | 0.4850 |
| 4,000 | 0.4688 |
| 6,000 | 0.3989 |
| 8,000 | **0.3944** |
| 10,000 | 0.4118 |

The minimum evaluation loss occurred at 8,000 steps. However, due to the current checkpoint configuration, only the models at 5,000 and 10,000 steps were saved; the model from 8,000 steps was not retained. A model trained for 10,000 steps was used for the evaluation on the actual hardware.

```text
act_16train_4eval_fp32_20261113_161537/checkpoints/010000/pretrained_model
*Note: This file is not stored here due to its large size.
```

For the next iteration, we will implement a mechanism to save checkpoints at the time of evaluation—or to save the model that yields the lowest evaluation loss. Note that evaluation loss and the success rate on the actual hardware are treated as separate metrics.

#### Evaluation Progress on Actual Hardware

We began with brief operational checks, verifying the approach, grasping, transporting, and placement phases. Observed issues included misaligned grasps, the robot failing to move from the starting position, and instances where, even if a grasp was successful, the transport phase could not be completed within the time limit.

As lighting conditions and starting poses varied between trials, it is not possible to isolate a single definitive cause for the failures.

After readjusting the starting pose, one 45-second trial resulted in a failed grasp; the robot moved toward the red container, then re-approached the workpiece, at which point the time limit was reached. In the subsequent trial, the program's time limit was extended to 60 seconds, and the task was successfully completed. We do not conclude that the model "recognized" the failed grasp based solely on the re-approach movement.

Across all evaluations involving actual robot movement, the task was successfully completed for the first time on the **10th attempt**. This count includes brief preliminary checks but excludes instances where the robot failed to move due to connection errors, as well as isolated tests for pose alignment or elbow movement. This was the second evaluation conducted after the final adjustment to the starting pose.

Because this evaluation took place during the development phase—with trial durations and starting conditions being adjusted along the way—these results should not be interpreted as a "10% success rate based on 10 trials under identical conditions." #### Record of a Successful Trial

| Item | Details |
|---|---|
| Trial ID | `rollout_so101_act100_current_20261113_202600` |
| Result | Successfully grasped a yellow-green workpiece and placed it into a red container ([Video of successful evaluation](video_evaluation/)) |
| Time Limit | 60 seconds |
| Target Control FPS | 30 |
| Action Steps per Re-prediction | 100 |
| Automatic Return upon Completion | Disabled |
| Recorded Frame Count | 1,706 |
| Exit Code | 0 |

Note: 30 FPS is the target setting; it does not imply that this rate was maintained throughout the entire execution. During the evaluation, warnings were triggered indicating that the control loop frequency fell below the target; the actual cycle time and camera update frequency remain under investigation.

The data from this successful trial has been backed up to the Windows system, including:

- Videos, joint states, actions, and metadata.
- Execution logs.
- The ACT model used, along with its pre-processing and post-processing configurations.
- Execution scripts and the shared camera adapter.
- A manifest file containing SHA-256 checksums for both the original and copied files.

The SHA-256 checksums for all copied files were verified to match, and the original data has been retained on the Ubuntu system.

#### Findings and Future Tasks

- **Initial success confirmed.** Reproducibility and success rate—measured through repeated evaluations under identical conditions—have not yet been assessed.
- Future evaluations will involve recording and standardizing initial joint values, workpiece positions, camera angles, and lighting conditions.
- Inconsistencies in calibration were observed repeatedly. While the restoration and accurate reloading of saved calibration values ​​were verified, further testing is required to ensure these settings are correctly maintained after power-cycling the system. - Lighting conditions differed between data collection (conducted during the day) and evaluation (conducted at night). Since this affects evaluation results, data collection and evaluation should be performed during the same time of day, or conducted in a darkroom to ensure consistent lighting conditions.
- Save the model that yields the lowest evaluation loss so that it can be used for future evaluations.

**Milestones achieved: Collected 20 demonstration samples, trained the ACT model, and successfully completed the task on the physical robot for the first time.**
