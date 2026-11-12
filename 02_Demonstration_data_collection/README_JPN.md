
# SO-101実演データの収集　　2026/11/5-11/11

## カメラアーム、カメラ設置パーツ、購入を申込

## カメラアーム、カメラ設置パーツ等、到着
<table>
  <tr>
    <td align="center">
      <img src="images/camera_arm_parts.jfif" width="33%">
      <br><b> カメラアーム、カメラ設置パーツ等 </b>
    </td>
  </tr>
</table>

## カメラアーム、組み立て
<table>
  <tr>
    <td align="center">
      <img src="images/arm_camera_setting_completed_1.png" width="33%">
      <br><b> 組み立て後、全体 </b>
    </td>
    <td align="center">
      <img src="images/arm_camera_setting_completed_2.png" width="33%">
      <br><b> 組み立て後、カメラ部 </b>
    </td>
  </tr>
</table>

## 作業環境、完成
<table>
  <tr>
    <td align="center">
      <img src="images/all_character_completed.png" width="33%">
      <br><b> 作業環境 </b>
    </td>
  </tr>
</table>

## 02-1. カメラの接続・映像確認 
付属USBカメラを接続。Ubuntuで白い爪と作業対象が同じ画面に映る位置に固定する。

### A. Windows用の撮影環境を作る
　・Windows用Pythonを準備 / 撮影環境を作る / Windowsでライブ映像を表示する / Ubuntuへの映像受け渡しを確認する <br>

### B. カメラの仮置き・撮影位置の決定
　・白い爪と作業対象(ワークと入れ物)が同じ画面に映る位置に固定する。

<table>
  <tr>
    <td align="center">
      <img src="images/image_from_camera.jpg" width="33%">
      <br><b> カメラからの画像 </b>
    </td>
  </tr>
</table>
      
## 02-2. 作業を決めて試し撮り 
例：ブロックをA地点からB地点へ移す。1回記録し、映像・関節位置・操作指令を確認する。

### A. 作業内容
　・黒いリーダーで白いフォロワーを操作し、黄緑のワークをつかみ、持ち上げて赤い入れ物へ移し、爪を開いて置く。 <br>

### B. 動作確認・調整
　- 記録前にリーダーとフォロワーの姿勢を近づけ、追従を確認した。 <br>
　- 肩・肘の上方向への追従が止まる症状に対し、現在位置から目標位置までの差の制限を調整した。 <br>
　- 肩の上下・肘は4度、その他の関節は設定値3で試行し、ワークを入れ物へ置くまでの動作を確認した。 <br>
　- 制御・記録の設定は30fpsとした。 <br>
　- 終了時の脱力による落下を防ぐため、プログラム終了後もフォロワーの保持トルクを残す設定を使用した。電源を切る際は、アームを支えてから切る。 <br>

 
 
 
