
# preparation 2026/10/23-11/2

## Placed an order for the SO-ARM101

## The SO-ARM101 arrived
<table>
  <tr>
    <td align="center">
      <img src="images/20261027_SO-ARM101.jpg" width="33%">
      <br><b> SO-ARM101 </b>
    </td>
  </tr>
</table>

## Hugging Face community
https://huggingface.co/docs/lerobot/so101## Preparing for "Teleoperation"
Set up "teleoperation," where a follower robot tracks the movements of a leader robot.

### 1. Install `usbipd-win` to pass the robot's USB connection to Ubuntu
・Run the following command in Windows PowerShell: <br>
　　　`winget install --interactive --exact dorssel.usbipd-win` <br>
・Close and reopen PowerShell, then run the following command: <br>
　　　`usbipd --version` <br>
・If the version (e.g., 5.3.0-54+Branch.master.Sha.aa...) is displayed, the installation of `usbipd-win` was successful. 

### 2. Leader Setup and Operational Verification
・PC detects the black control board <br>
・Access permissions successfully configured ⇒ The black control board is now accessible from Ubuntu <br>
・Ubuntu-side: Prepare the Python environment for LeRobot <br>
　　　・Install the software required for LeRobot and for communication with the SO-101 motors <br>
・Mount the leader unit onto the desk <br>
　　　・Secure the base using a clamp <br>
・Calibrate the leader unit <br>
　　　・Verify USB detection and access permissions in Ubuntu <br>
　　　・Check the communication verification function within the Feetech (servo motor manufacturer) SDK <br>
　　　・Perform calibration <br>

### 3. Follower Setup and Operational Verification
・Connect the follower’s 3-core cable to the control board <br>
・Mount the follower unit onto the desk <br>
　　　・Secure the base using a clamp <br>
・Calibrate the follower unit <br>
　　　・Verify USB detection and access permissions in Ubuntu <br>
　　　・Perform calibration <br>

### 4. Teleoperation Verification
・Connect the leader’s black control board to the PC via USB <br>
・Connect the control board of the white follower unit to a PC via USB <br>
・Initial verification of teleoperation <br>
・Verification of elbow flexion and extension (following motion): Completed <br>
