
# SO-101 Demonstration data collection　　2026/11/5-11/13

## Request to purchase camera arms and camera mounting components

## Camera arm, camera mounting components, etc., have arrived.
<table>
  <tr>
    <td align="center">
      <img src="images/camera_arm_parts.jfif" width="33%">
      <br><b> Camera arm, camera mounting components, etc </b>
    </td>
  </tr>
</table>

## Camera arm assembly
<table>
  <tr>
    <td align="center">
      <img src="images/arm_camera_setting_completed_1.png" width="33%">
      <br><b> Overall view after assembly </b>
    </td>
    <td align="center">
      <img src="images/arm_camera_setting_completed_2.png" width="33%">
      <br><b> Camera section after assembly </b>
    </td>
  </tr>
</table>

## work environment, completed
<table>
  <tr>
    <td align="center">
      <img src="images/all_character_completed.png" width="33%">
      <br><b> work environment </b>
    </td>
  </tr>
</table>


## 02-1. Connect the camera and check the video
Connect the supplied USB camera and view its feed in Ubuntu. Mount it so the white follower’s gripper and the target object are both visible in the frame.

### A. Setting up a recording/capture environment for Windows
　・Setting up Python for Windows / Preparing the filming environment / Displaying live video on Windows / Verifying video transmission to Ubuntu <br>

### B. Temporarily placing the camera and determining the shooting position
　・Position the white grippers so that they and the objects being handled (the workpiece and its container) are both visible within the same field of view.
<table>
  <tr>
    <td align="center">
      <img src="images/image_from_camera.jpg" width="33%">
      <br><b> Image from the camera </b>
    </td>
  </tr>
</table>

## 02-2. Defining the Task and Performing a Test Run
Example: Moving a block from point A to point B. Record the process once, then review the video, joint positions, and control commands.

### A. Task Description
・Use the "leader" (black unit) to operate the "follower" (white unit) to grasp a yellow-green workpiece, lift it, move it to a red container, and release it by opening the gripper. <br>

### B. Motion Verification and Adjustment
- Before recording, the poses of the leader and follower were aligned to ensure proper tracking. <br>
- To address an issue where the shoulder and elbow would stop tracking during upward movement, the limit on the difference between the current position and the target position was adjusted. <br>
- The system was tested with a setting of 4 degrees for the shoulder (vertical) and elbow joints, and a setting of 3 for all other joints; the full sequence—up to placing the workpiece into the container—was verified. <br>
- Control and recording were set to 30 fps. <br>
- To prevent the workpiece from dropping due to a loss of holding torque when the program ends, the system was configured to maintain holding torque in the follower even after the program concludes. <br>
Always support the arm before powering off the system. <br>

### C. Test Run Results
・In the trial run `retry04`, the task of placing the yellow-green workpiece into the red container was successfully completed. Both the recording process and the video encoding finished without errors. <br>

| Item | Record Details |
| --- | --- |
| Dataset Name | `so101_yellow_pick_place_retry04_20261112_154246` |
| Number of Episodes | 1 |
| Recording Duration Setting | 60 seconds |
| Number of Saved Frames | 1,789 |
| Dataset Target FPS | 30 |
| Video | 640 × 480, MP4 (AV1 format) |
| Joint Positions | `observation.state`: 6 joints |
| Control Commands | `action`: 6 joints |
| Numerical Data | Parquet format |
| Storage Location During Collection | Local PC (no automatic upload) |

The recording setup involved capturing footage on a Windows machine and reading the images from a shared folder on an Ubuntu system. Preliminary testing indicated an image update rate of approximately 8.1 frames per second; consequently, the 30 fps saved video contains repeated frames.

### D. Saved Files

- Numerical Data: `data/chunk-000/file-000.parquet`
- Video: `videos/observation.images.workspace/chunk-000/file-000.mp4` --->  [Video](video/so101_retry04.mp4)
- Metadata: `meta/info.json`

### E. Verification Results and Future Improvements

- The joint position and control command data each consist of 1,789 rows × 6 joints; it was confirmed that there are no `NaN` or infinite values. All 1,789 frames of the video were successfully retrieved, and the number of frames matches the numerical data. <br>
- Visual inspection confirmed the absence of black bars, missing image segments, or prolonged freezes in the video. <br>
・At the moment of grasping, the contact between the gripper fingers and the workpiece is obscured by the follower itself, making it impossible to directly observe this contact via the video feed.<br>
For now, this footage will be saved as a result of the trial run; however, the camera position will be adjusted in future sessions to ensure the grasping action remains visible for the purpose of collecting demonstrations for machine learning.<br>

## 02-3. Collecting Demonstration Data
Repeat and record the same task, then compile successful demonstration data for training purposes.

Using the SO-101 "leader" unit, we collected demonstrations in which the "follower" unit performed the task: "grasp a yellow-green workpiece, lift it, transport it to a red container, and place it inside." <br>
We selected 20 successful demonstrations to create a dataset for imitation learning. <br>

#### Collection Method

- We used a white "follower" unit and a black "leader" unit, reusing previously saved calibration settings.
- The workspace was filmed by a single camera positioned opposite the robots.
- After adjusting the field of view through test recordings, we proceeded with data collection using consistent camera angles and control settings.
- Data was collected in four batches of 5 demonstrations each.
- Each demonstration began when the operator pressed the "Enter" key; after the data was saved, the outcome (success or failure) was recorded. Before each subsequent demonstration, the yellow-green workpiece and the robotic arm were reset to their initial positions.
- The 8th demonstration was re-recorded; the original 8th attempt was discarded, and the re-recorded data was used instead.

| Item | Details |
|---|---|
| Number of demonstrations used | 20 episodes ([datasets/video/](datasets/video/)) |
| Camera images | 640 × 480, RGB |
| Recording frame rate (FPS) | 30 |
| Numerical data | `observation.state` and `action` (6 elements each) |
| Target joints | Base rotation, shoulder, elbow, wrist pitch, wrist roll, gripper |
| Data format | LeRobot Dataset v3.0 |

#### Data Inspection and Integration

Numerical data and video recordings were inspected after every 5 demonstrations; the re-recorded 8th demonstration was also verified.

- Ensured that the number of rows in the metadata matches the number of rows in the numerical data.
- Verified that `observation.state` and `action` each consist of 6 elements and contain no NaN (Not a Number) or infinite values. - Frame numbers must be sequential, starting from 0; timestamps must be monotonically increasing and consistent with the specified frame rate (FPS).
- The video file must be readable in its entirety, with a resolution of 640 × 480.
- The number of frames in the video must match the number of frames in the numerical data.

The post-task waiting periods for each demonstration were processed, and the data—without altering the original source files—was integrated into a new training dataset. The source data comprised a total of 20,650 frames; following processing and integration, this resulted in 20 episodes containing 15,540 frames.

After integration, it was verified that the numerical data remained intact and that the frame counts in the videos matched the data. Note that because the videos were re-encoded using the H.264 codec, they are not byte-for-byte identical to the original video files.

This validation process confirms the integrity of the file structure, numerical data, and timestamps; it does not guarantee that every image is unique, nor does it certify the precision of real-time synchronization between the camera feed and the joint data.

**Result: 20 successful demonstrations have been incorporated, and the preparation of the training dataset is complete.**

