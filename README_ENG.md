# Pysical_AI_Real-to-Sim_and_Sim-to-Real

Control models, learned and verified through simulation, are translated into actions performed by an actual robot.

## Introduction
・I have previously implemented VLA (Vision-Language-Action) in simulations using Isaac Lab, and I now intend to deploy it on a physical robot.<br>
　I am currently developing a concept for Real-to-Sim and Sim-to-Real pipeline.<br>
・I have mapped out the concept into a schedule. Please review the schedule below.<br><br>

・Based on the schedule, we proceeded with the purchase of a robot arm and a camera arm—including the assembly of the latter—and established a teleoperation environment.<br>
・First of all, I decided to proceed with Pick and Place. <br>
・We teleoperated the SO-101 to collect actual machine data, created a model using imitation learning, and evaluated it on the actual machine. <br>

## Schedule

- **[English — ROADMAP_ENG.md](ROADMAP_ENG.md)**

## Actual Tasks

① [SO-101 hardware setup](01_SO-101_hardware_setup/README_ENG.md) <br>

<table>
  <tr>
    <td align="center">
      <img src="01_SO-101_hardware_setup/images/20261103_leader_and_follower.png" width="33%">
      <br><b> follower and leader </b>
    </td>
  </tr>
</table>

② [Demonstration data collection](02_Demonstration_data_collection/README_ENG.md)  <br>

<table>
  <tr>
    <td align="center">
      <img src="02_Demonstration_data_collection/images/all_character_completed.png" width="33%">
      <br><b> work environment </b>
    </td>
  </tr>
</table>

　　Performed teleoperation ( [video of the process: teleoperation.mp4](02_Demonstration_data_collection/video/) )<br>
　　and saved data from 20 successful trials<br>
　　　　⇒　[Collected video data](02_Demonstration_data_collection/datasets/video/)

③ [Imitation learning and hardware evaluation](03_Imitation_learning_and_hardware_evaluation/README_ENG.md)  <br>

　　We provided the model with video of the current operating environment and evaluated its performance on the actual hardware. <br>
　　　　⇒　[Video of successful evaluation](03_Imitation_learning_and_hardware_evaluation/video_evaluation/)

