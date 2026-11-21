# ④ Real-to-Sim — SO-101の作業環境をIsaac Labで再現

白いSO-101フォロワーが黄色いワークをつかみ、赤いおわんに入れる作業をIsaac Labで再現した。ロードマップ②で収集した成功実演20件のうち、`take02` を使用した。仮想環境では、実演の関節データをもとにワークを把持し、縁を越える搬送軌道に調整してから、おわんの中に投入した。

[SO-101全体ロードマップ](https://github.com/SooSooMoo/Pysical_AI_Real-to-Sim-to-Real/blob/main/ROADMAP_JPN.md)

## 実行環境

| 項目 | 使用した環境 |
| --- | --- |
| GPU環境 | Runpod GPU Pod、NVIDIA GeForce RTX 4090、VRAM 24 GB（`nvidia-smi` では24,564 MiB） |
| ドライバー | NVIDIA 595.112.07。 `nvidia-smi` のCUDA表示は13.2 |
| Pythonライブラリ | PyTorch 2.11.0+cu128、torchvision 0.26.0+cu128、NumPy 2.5.5、Gymnasium 1.2.1 |
| シミュレーション | Isaac Sim上でIsaac Labの開発版チェックアウトを使用。Kitの起動ログは `110.1.2+production.326809.f9bf0dda.gl` |
| 実行パス | Isaac Labは `/workspace/IsaacLab-develop`、Isaac Sim付属Pythonは `/isaac-sim/python.sh`、作業フォルダーは `/workspace/step10` |
| 作業方法 | VS Code Remote TunnelsでRunpodに接続。カメラ付きのヘッドレス実行でMP4とCSVを保存し、VS Codeから手元へダウンロード |

ドライバーが表示するCUDA対応バージョンと、PyTorchのビルドが使用するCUDAバージョンは別の項目。RunpodではCUDAが利用可能で、RTX 4090上でPyTorchの計算が成功した。

### RunpodとIsaac Labの準備

1. RunpodでGPU Podを起動する。今回使用した既存テンプレートのコンテナイメージは `ghcr.io/soosoomoo/isaac-sim-6.0.1-novnc:latest`。GHCR上のPrivateイメージを使う場合は、読み取り権限のあるGitHubアカウントの `read:packages` 付きトークンをRunpodの **Credentials → Registry Credentials** に登録し、Podの設定で選択する。イメージ取得時に `denied` が出る場合は、タグとトークンの有効期限を確認する。
2. Pod内でIsaac Labのチェックアウトを `/workspace/IsaacLab-develop` に用意し、Isaac Sim付属Pythonで動く既存環境を使う。イメージ名に含まれる `6.0.1` はコンテナの識別名。厳密に環境を再現する場合は、イメージのdigestとIsaac LabのコミットIDを記録する。
3. GPU、PyTorch、Isaac Labの起動を確認する。空シーンで `[INFO]: Setup complete...` が出たら、確認後に `Ctrl+C` で終了する。

```bash
nvidia-smi
/isaac-sim/python.sh -c 'import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.ones(3, device="cuda") * 2)'
cd /workspace/IsaacLab-develop
./isaaclab.sh -p scripts/tutorials/00_sim/create_empty.py
```

Runpod内でVS Code CLIが準備済みなら、`./code tunnel user login --provider github` で認証し、`./code tunnel` で接続を開始できる。

## 4-1 作業環境の再現

台座の `shoulder_pan` 回転軸を天板に投影した点を測定の基準とした。前後左右は、フォロワーの背後から作業スペースを見た向きで表す。

| 対象 | 仮想シーンの設定 |
| --- | --- |
| SO-101 | Isaac Labの `SO101_CFG`。腕5関節とグリッパー1関節 |
| 机 | 天板を高さ0とする簡易形状 |
| 黄色いワーク | 長さ8.7 cm、幅4.4 cm、高さ2.5 cm。前21 cm・右4.5 cm、平面内で約15°傾けて配置。質量は仮に30 g |
| 赤いおわん | 内径17.0 cm、外径17.4 cm、深さ6.3 cm。前22 cm・左12 cm。底から縁へ丸く広がる形状で、底の外径は仮に10.8 cm |
| カメラ | 640×480の確認用RGBカメラ。上方視点で配置を確認し、投入試験は縁が見える斜め視点で撮影 |

ワークとおわんの位置は、実機で測った前22 cm・右8 cmと前22 cm・左8 cmを出発点とし、映像比較と仮想環境での把持試験で調整した。確認用カメラの位置と向きは仮設定。

## 4-2 実機との比較

### 実演データ

`so101_yellow_pick_place_20_trimmed_v1` は、固定カメラの動画、フォロワーの関節実測値 `observation.state`、テレオペ操作の目標値 `action` を含むLeRobot Dataset v3.0。再生には `take02`（`episode_index = 1`）の `observation.state` を使用した。780フレーム、30 fps、26秒の実演である。

腕5関節は度からラジアンに変換し、手首の回転 `wrist_roll` に暫定で−90°を適用した。グリッパーの0〜100の記録値は、実機映像と仮想モデルで開閉方向を確認したうえで、仮想モデルの可動範囲に線形で割り当てた。

### 動きの比較と調整

1. 実機映像と仮想側の同じフレームを比較し、ワークへの接近、持ち上げ、おわんへの搬送、解放を確認した。
2. ワークに重力と衝突を設定し、実測関節位置をモーターの目標値として与えた。把持前の拡大映像では片方の爪がワークの上面に当たっていたため、ワークの横位置を調整した。
3. おわんの縁との接触に対し、深さ6.3 cmと5.8 cmを比較した。両条件で接触が見えたため、深さを6.3 cmに戻し、搬送時の持ち上げを目標で5 cm補正した。ワークの下端が縁より5 mm以上高く、全ての角が開口部内に余裕を持って収まる位置で解放を許可した。

### 修正版の動画とCSVで確認した結果

| 指標 | 結果 |
| --- | --- |
| 記録 | 動画とCSVともに780フレーム、30 fps、26秒 |
| ワーク中心の高さ | 開始時1.25 cm、最大11.01 cm（フレーム459、15.30秒） |
| 縁付近での通過 | 解放前に、ワーク中心がおわん中心から14.5 cm未満で、最外角が開口部の内半径8.5 cm以上にある44フレームを抽出。その区間で、最も低い角は縁より最小8.5 mm上 |
| 解放を許可 | フレーム490（16.33秒）。ワークの最も低い角は縁より18.5 mm上、最外角はおわん中心から7.95 cm |
| 投入後 | ワーク中心はおわんの中心から水平に2.10 cm。最後の30フレームで位置は静止 |

縁付近のすき間は仮想シーンの幾何に基づく算出値。動画でも、ワークが縁を越えておわんに入る様子を確認した。実機側の爪先やワークの3次元位置は計測していないため、実機との比較は映像による定性的な確認まで。

## Runpodでの再実行

以下のファイルを `/workspace/step10` に置く。

| ファイル | 内容 |
| --- | --- |
| [scene_take02_rim_check.py](./scene_take02_rim_check.py) | 机、動くワーク、おわんを配置 |
| [test_take02_rim_clearance_verified.py](./test_take02_rim_clearance_verified.py) | 把持から投入までを実行し、動画とCSVを保存 |
| `take02_states.json` | 実演の関節実測値。元データZIPから下記の手順で生成可能 |

JSONが準備済みなら、次の「動画とCSVの生成」へ進む。

### 実演からJSONを生成

`so101_yellow_pick_place_20_trimmed_v1.zip` を作業フォルダーに転送する。動画再生用のPythonと切り離して依存関係を扱うため、Parquet読み出し用の `pyarrow` をプロジェクト内の `.data-deps` に入れる。

```bash
cd /workspace/step10
unzip -n so101_yellow_pick_place_20_trimmed_v1.zip
/isaac-sim/python.sh -m pip install --target "$PWD/.data-deps" pyarrow
PYTHONPATH="$PWD/.data-deps${PYTHONPATH:+:$PYTHONPATH}" /isaac-sim/python.sh - <<'PY'
import json
from pathlib import Path
import pyarrow.parquet as pq

root = Path("so101_yellow_pick_place_20_trimmed_v1")
info = json.loads((root / "meta/info.json").read_text(encoding="utf-8"))
table = pq.read_table(
    root / "data/chunk-000/file-000.parquet",
    columns=["frame_index", "timestamp", "observation.state"],
    filters=[("episode_index", "=", 1)],
)
frames = sorted(table.to_pylist(), key=lambda row: row["frame_index"])
assert len(frames) == 780
names = info["features"]["observation.state"]["names"]
payload = {
    "episode_index": 1,
    "fps": info["fps"],
    "joint_names": names,
    "units": ["range_0_100" if name == "gripper.pos" else "deg" for name in names],
    "frames": frames,
}
Path("take02_states.json").write_text(
    json.dumps(payload, allow_nan=False), encoding="utf-8"
)
PY
```

### 動画とCSVの生成

FFmpegが見つからない場合は、`imageio-ffmpeg` に同梱される実行ファイルを使う。以下のコマンドは、システムの `ffmpeg` を優先し、見つからなければ作業フォルダーに `imageio-ffmpeg` を入れる。

```bash
cd /workspace/IsaacLab-develop
if ! FFMPEG_BIN=$(command -v ffmpeg); then
  DEPS=/workspace/step10/.video-deps
  /isaac-sim/python.sh -m pip install --target "$DEPS" --no-deps --only-binary=:all: imageio-ffmpeg &&
  FFMPEG_BIN=$(PYTHONPATH="$DEPS${PYTHONPATH:+:$PYTHONPATH}" \
    /isaac-sim/python.sh -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')
fi
if [ -n "$FFMPEG_BIN" ]; then
  ./isaaclab.sh -p /workspace/step10/test_take02_rim_clearance_verified.py \
    --ffmpeg "$FFMPEG_BIN" --bowl-depth-cm 6.3 --lift-cm 5
fi
```

成果物は `/workspace/step10` に保存される。

- [take02_rim_clearance_corrected_lift5_depth6.3.mp4](results/task02/) は4-1の作業環境と、把持から投入までの動画。
- [take02_rim_clearance_corrected_lift5_depth6.3.csv](results/task02/) はワーク中心のXYZ、最下端と縁の高低差、おわん中心から最外角までの距離、解放の許可、各関節の目標角と実測角の時系列。4-2の数値結果の根拠。
