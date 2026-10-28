
# 準備 2028/10/23-27

## 2026/10/23:SO-ARM101、購入を申込

## 2026/10/27:SO-ARM101、到着
<table>
  <tr>
    <td align="center">
      <img src="images/20261027_SO-ARM101.jpg" width="33%">
      <br><b> SO-ARM101 </b>
    </td>
  </tr>
</table>

## Hugging Face コミュニティ
https://huggingface.co/docs/lerobot/so101

## 「テレオペレーション」の準備
リーダーを動かすとフォロワーが追従する「テレオペレーション」の準備を行う

### 1. ロボットのUSB接続をUbuntuに渡すための usbipd-win を導入
　・WindowsのPowerShellで、以下を実行してください。<br>
 　　　`winget install --interactive --exact dorssel.usbipd-win`
　・PowerShellを閉じて開き直し、次を実行してください。<br>
 　　　`usbipd --version`
　・バージョン(5.3.0-54+Branch.master.Sha.aa.....)が表示されたら、usbipd-winの導入は成功です。

### 2. リーダーのUSB接続を識別



 
 
