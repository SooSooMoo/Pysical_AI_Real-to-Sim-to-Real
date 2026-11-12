# SO-101 Project Roadmap

**Status as of November 3, 2026:** The follower tracks the leader on all six joints. The next session, on or after November 4, will cover USB camera setup and video verification. Later dates have not been set.

**Goal:** Use demonstrations collected on the physical robot to train and refine a policy in simulation, then test it on the physical robot.

| Phase | Task | Steps and completion criteria | Status |
| --- | --- | --- | --- |
| 1. [SO-101 hardware setup](01_SO-101_hardware_setup/README_ENG.md)  | 1-1 Prepare the PC | Set up Ubuntu and LeRobot. Verify USB connectivity and serial port permissions. | Complete |
| 1. SO-101 hardware setup | 1-2 Prepare both arms | Clamp both bases to the table. Check wiring, power supplies, and motor communication. Save the calibration data for each arm. | Complete |
| 1. SO-101 hardware setup | 1-3 Test teleoperation | Move the black leader arm and confirm that the white follower tracks all six joints. | Complete |
| 2. [Demonstration data collection](02_Demonstration_data_collection/README_ENG.md) | 2-1 Connect the camera and check the video| Connect the supplied USB camera and view its feed in Ubuntu. Mount it so the white follower’s gripper and the target object are both visible in the frame. | Complete |
| 2. Demonstration data collection | **2-2 Choose a task and record a trial** <br> **"MimicAndCapture"** | For example, move a block from point A to point B. Record one demonstration and check the video, joint positions, and commands. | **Complete** |
| 2. Demonstration data collection | **2-3 Collect demonstrations** | Repeat the task and assemble the successful demonstrations into a training dataset. | **Start** |
| 3. Imitation learning and hardware evaluation | 3-1 Check the training environment | Verify GPU operation in PyTorch, then choose between the local PC and an external GPU for training. | Planned |
| 3. Imitation learning and hardware evaluation | 3-2 Train and evaluate a policy | Train on the demonstrations. Run the same task on the white follower, count successful trials, and record common failure patterns. | Planned |
| 4. Real-to-Sim | 4-1 Recreate the workspace | Reproduce the dimensions and placement of the white follower, table, target object, and camera in simulation. | Planned |
| 4. Real-to-Sim | 4-2 Compare simulated and physical motion | Replay the recorded motion on the simulated arm. Compare the gripper tip’s path and the object’s motion with the physical recording. | Planned |
| 5. Sim-to-Real | 5-1 Train and refine the policy in simulation | Vary conditions such as object position and lighting while training and evaluating the policy on the same task. | Planned |
| 5. Sim-to-Real | 5-2 Validate on hardware | Test the refined policy on the white follower and compare its success rate with the baseline from Phase 3. | Planned |

"MimicAndCapture": Mimic and Capture — the “Hello World” of robot data collection.Follow the motion. Record the scene. Save the data.I came up with the name.
