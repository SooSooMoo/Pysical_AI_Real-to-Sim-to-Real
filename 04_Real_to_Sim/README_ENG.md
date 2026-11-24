# ④ Real-to-Sim — Recreating the SO-101 Workspace in Isaac Lab

This project recreates a pick-and-place task in Isaac Lab. The white SO-101 follower picks up a yellow workpiece and places it in a red bowl. The simulation uses `take02`, one of 20 successful demonstrations collected in Stage ②. The recorded joint positions provided the starting trajectory. The simulated transport motion was adjusted to clear the rim before releasing the workpiece.

[Project roadmap](https://github.com/SooSooMoo/Pysical_AI_Real-to-Sim-to-Real/blob/main/ROADMAP_JPN.md) · [Japanese README](./README_JPN.md)

## Runtime Environment

| Item | Environment used |
| --- | --- |
| GPU | Runpod GPU Pod with an NVIDIA GeForce RTX 4090 and 24 GB of VRAM (24,564 MiB reported by `nvidia-smi`) |
| Driver | NVIDIA 595.112.07. `nvidia-smi` reported CUDA 13.2 |
| Python libraries | PyTorch 2.11.0+cu128, torchvision 0.26.0+cu128, NumPy 2.5.5, and Gymnasium 1.2.1 |
| Simulator | Isaac Sim with an Isaac Lab development checkout. Kit startup log showed `110.1.2+production.326809.f9bf0dda.gl` |
| Paths | Isaac Lab at `/workspace/IsaacLab-develop`, bundled Python at `/isaac-sim/python.sh`, and project files at `/workspace/step10` |
| Workflow | VS Code Remote Tunnels for Runpod access. Headless runs produced MP4 and CSV files, which were downloaded through VS Code |

The driver-reported CUDA version describes driver support. The `cu128` suffix identifies the CUDA build of PyTorch. PyTorch detected CUDA and successfully ran a calculation on the RTX 4090.

### Runpod and Isaac Lab setup

1. Start a Runpod GPU Pod. The existing template used `ghcr.io/soosoomoo/isaac-sim-6.0.1-novnc:latest`. For the private GHCR image, register a GitHub token with `read:packages` under **Credentials → Registry Credentials** and select those credentials in the Pod settings. The GitHub account must have read access to the package. If the image pull returns `denied`, check the tag and token expiration date.
2. Use the Isaac Lab checkout at `/workspace/IsaacLab-develop` with Isaac Sim's bundled Python. The `6.0.1` string is part of the container image name. Exact environment reproduction requires the image digest and Isaac Lab commit ID.
3. Check the GPU, PyTorch, and simulator startup. Once the empty scene prints `[INFO]: Setup complete...`, press `Ctrl+C` to exit.

~~~bash
nvidia-smi
/isaac-sim/python.sh -c 'import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.ones(3, device="cuda") * 2)'
cd /workspace/IsaacLab-develop
./isaaclab.sh -p scripts/tutorials/00_sim/create_empty.py
~~~

With the VS Code CLI installed in the Pod, run `./code tunnel user login --provider github` to authenticate, then run `./code tunnel` to start the connection.

## 4-1 Recreating the Workspace

The reference point is the projection of the base's `shoulder_pan` axis onto the tabletop. Forward, left, and right are defined from behind the follower, looking toward the workspace.

| Object | Simulation setup |
| --- | --- |
| SO-101 | Isaac Lab's `SO101_CFG` with five arm joints and one gripper joint |
| Table | Simplified geometry with the tabletop at zero height |
| Yellow workpiece | 8.7 cm long, 4.4 cm wide, and 2.5 cm high. Positioned 21 cm forward and 4.5 cm right, with an approximately 15° in-plane rotation. Assumed mass of 30 g |
| Red bowl | 17.0 cm inner opening diameter, 17.4 cm outer opening diameter, and 6.3 cm internal depth. Positioned 22 cm forward and 12 cm left. The sides curve outward from the base to the rim. Assumed outer base diameter of 10.8 cm |
| Camera | 640×480 RGB camera. An overhead view was used to check the layout, and an oblique view was used to inspect clearance over the rim |

The real-world measurements were 22 cm forward and 8 cm right for the workpiece, and 22 cm forward and 8 cm left for the bowl. The simulated positions were adjusted after reviewing the footage and testing the grasp. The review camera uses an approximate pose.

## 4-2 Comparison with the Real Robot

### Demonstration data

`so101_yellow_pick_place_20_trimmed_v1` is a LeRobot Dataset v3.0 containing fixed-camera video, measured follower joint positions in `observation.state`, and teleoperation targets in `action`. Replay used the `observation.state` values for `take02` (`episode_index = 1`). The demonstration contains 780 frames at 30 fps and lasts 26 seconds.

The five arm joint positions were converted from degrees to radians. A provisional −90° offset was applied to `wrist_roll`. After comparing the opening direction in the real footage and the simulation, the recorded gripper values on a 0–100 scale were mapped linearly to the simulated joint range.

### Motion comparison and adjustments

1. Matching frames from real and simulated footage were used to compare approach, lift, transport, and release.
2. Gravity and collisions were enabled for the workpiece, and the recorded joint positions were used as motor targets. A close-up showed one jaw contacting the top of the workpiece before grasping, so the workpiece was shifted laterally in simulation.
3. The workpiece touched the rim at both tested bowl depths, 6.3 cm and 5.8 cm. The bowl was restored to 6.3 cm and a 5 cm upward target adjustment was applied during transport. Release was enabled once the lowest corner was at least 5 mm above the rim and all corners were inside the opening with margin.

### Results from the corrected video and CSV

| Metric | Result |
| --- | --- |
| Recording | Both the video and CSV cover 780 frames at 30 fps, or 26 seconds |
| Workpiece center height | 1.25 cm at the start and a maximum of 11.01 cm at frame 459 (15.30 s) |
| Clearance near the rim | Before release, 44 frames met both criteria. The workpiece center was less than 14.5 cm from the bowl center, and the farthest corner was at least 8.5 cm from the bowl center, measured horizontally. Across those frames, the minimum clearance of the lowest corner above the rim was 8.5 mm |
| Release enabled | Frame 490 (16.33 s). The lowest corner was 18.5 mm above the rim, and the farthest corner was 7.95 cm horizontally from the bowl center |
| Final position | The workpiece center settled 2.10 cm horizontally from the bowl center and remained stationary over the final 30 frames |

Clearance was calculated from the simulated geometry. The video shows the workpiece clearing the rim and entering the bowl. The real-world comparison is qualitative and based on footage because the real fingertip and workpiece trajectories were not measured in 3D.

## Reproducing the Trial on Runpod

Place the following files in `/workspace/step10`.

| File | Purpose |
| --- | --- |
| [scene_take02_rim_check.py](code/) | Builds the table, movable workpiece, and bowl |
| [test_take02_rim_clearance_verified.py](code/) | Runs the grasp and placement trial and saves the video and CSV |
| `take02_states.json` | Measured joint positions for the demonstration, generated from the source dataset ZIP |

If the JSON already exists, proceed to **Generate the video and CSV**.

### Export the demonstration to JSON

Upload `so101_yellow_pick_place_20_trimmed_v1.zip` to the project directory. Install `pyarrow` in the project-local `.data-deps` directory to keep the Parquet dependency separate from the simulator's environment.

### Generate the video and CSV

The command uses the system `ffmpeg` when available. Otherwise, it installs `imageio-ffmpeg` locally and uses its bundled executable.

Outputs are written to `/workspace/step10`.

- [take02_rim_clearance_corrected_lift5_depth6.3_visual_aligned_replay.mp4](results/task02/) shows the workspace and the full grasp-to-placement sequence for 4-1.
- [take02_rim_clearance_corrected_lift5_depth6.3_visual_aligned_replay.csv](results/task02/)  records the workpiece center in XYZ, clearance between its lowest corner and the rim, the maximum horizontal distance from a corner to the bowl center, the release flag, and target and measured joint angles. It provides the numerical evidence for 4-2.
