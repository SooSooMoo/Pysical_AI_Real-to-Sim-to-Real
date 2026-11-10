
# 準備 2026/10/23-11/3

## SO-101、購入を申込

## SO-101、到着
<table>
  <tr>
    <td align="center">
      <img src="images/20261027_SO-ARM101.jpg" width="33%">
      <br><b> SO-101 </b>
    </td>
  </tr>
</table>

### Hugging Face コミュニティ
     https://huggingface.co/docs/lerobot/so101

## 01-1 PC環境の準備
Ubuntu・LeRobotを準備し、USB接続とアクセス権を確認する。

### A. ロボットのUSB接続をUbuntuに渡すための usbipd-win を導入
　・WindowsのPowerShellで、以下を実行してください。<br>
 　　　`winget install --interactive --exact dorssel.usbipd-win` <br>
　・PowerShellを閉じて開き直し、次を実行してください。<br>
 　　　`usbipd --version` <br>
　・バージョン(5.3.0-54+Branch.master.Sha.aa.....)が表示されたら、usbipd-winの導入は成功です。

## 01-2 両アームの準備 
リーダーを動かすとフォロワーが追従する「テレオペレーション」の準備を行う

### A. リーダーの設定・動作確認
　・黒い基板をPCが認識 <br>
　・アクセス権の設定も成功 ⇒ Ubuntuから黒い基板を扱える状態 <br>
　・Ubuntu側：LeRobot用のPython環境を準備 <br>
 　　　　　・LeRobot本体とSO-101のモーター通信に必要なソフトを入れる <br>
　・机にリーダーを設置する <br>
 　　　　　・台座をクランプで止める <br>
　・リーダーのキャリブレーション <br>
 　　　　　・UbuntuでのUSB認識とアクセス権の確認 <br>
 　　　　　・Feetech(サーボモーターのメーカー)のSDKの通信確認機能を確認 <br>
 　　　　　・キャリブレーション <br>

### B. フォロワーの設定・動作確認
　・フォロワーの3芯線を制御基板につなぐ <br>
　・机にフォロワーを設置する <br>
　　　　　・台座をクランプで止める <br>
　・フォロワーのキャリブレーション <br>
 　　　　　・UbuntuでのUSB認識とアクセス権の確認 <br>
 　　　　　・キャリブレーション <br>

<table>
  <tr>
    <td align="center">
      <img src="images/20261103_leader_and_follower.png" width="33%">
      <br><b> follower and leader </b>
    </td>
  </tr>
</table>

### 4. テレオペレーションの確認
　・黒いリーダーの制御基板を、USBでPCにつなぐ <br>
　・白いフォロワーの制御基板を、USBでPCにつなぐ <br>
　・テレオペレーションの初回確認　<br>
 　　　　　・[爪(指)の開閉]の追従確認：完了 <br>
 　　　　　・[手首の曲げ伸ばし]の追従確認：完了 <br>
 　　　　　・[手首のひねり]の追従確認：完了 <br>
 　　　　　・[肘の曲げ伸ばし]の追従確認：完了 <br>
 　　　　　・[肩の上げ下げ]の追従確認：完了 <br>
　　　　　　　　　肩の追従不良発生：対応済み(原因：フォロワーのキャリブレーションのミス) <br>
 　　　　　・[肩の左右回転]の追従確認：完了 <br>

## カメラの接続・映像確認

### 1. Windows用の撮影環境を作る
　・Windows用Pythonを準備 / 撮影環境を作る / Windowsでライブ映像を表示する / Ubuntuへの映像受け渡しを確認する <br>

### 2. カメラの仮置き・撮影位置の決定
      
 
 
 
