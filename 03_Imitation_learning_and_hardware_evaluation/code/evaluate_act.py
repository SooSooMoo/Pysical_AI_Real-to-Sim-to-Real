"""Run one of four batches of five independently recorded ACT trials."""
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys

OPTIONS = ['--strategy.type=episodic',
 '--inference.type=sync',
 '--policy.device=cuda',
 '--policy.use_amp=false',
 '--policy.n_action_steps=100',
 '--robot.type=so101_follower',
 '--robot.id=white_follower',
 '--robot.max_relative_target={"shoulder_pan":3,"shoulder_lift":4,"elbow_flex":4,"wrist_flex":3,"wrist_roll":3,"gripper":3}',
 '--robot.disable_torque_on_disconnect=false',
 '--return_to_initial_position=false',
 '--fps=30',
 '--dataset.no_stamp=true',
 '--dataset.fps=30',
 '--dataset.num_episodes=1',
 '--dataset.episode_time_s=60',
 '--dataset.reset_time_s=0',
 '--dataset.single_task=Pick up the yellow object and place it in the red container.',
 '--dataset.push_to_hub=false',
 '--dataset.streaming_encoding=true',
 '--dataset.encoder_threads=2',
 '--dataset.rgb_encoder.vcodec=h264',
 '--dataset.rgb_encoder.preset=fast',
 '--display_data=false',
 '--play_sounds=false']

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--batch", type=int, required=True, choices=range(1, 5))
    p.add_argument("--model", required=True, type=Path)
    p.add_argument("--port", required=True)
    p.add_argument("--jpeg", required=True, type=Path, help="Continuously updated shared JPEG")
    p.add_argument("--output", type=Path, default=Path("evaluation"))
    args = p.parse_args()
    if not (args.model / "model.safetensors").is_file() or not args.jpeg.is_file():
        p.error("Check --model and the running camera publisher (--jpeg)")
    session = args.output.resolve() / datetime.now().strftime(f"batch{args.batch}_%Y%m%d_%H%M%S_%f")
    session.mkdir(parents=True)
    cameras = {"workspace": {"type": "so101_shared_jpeg", "fps": 30, "width": 640, "height": 480,
                              "path": str(args.jpeg.resolve())}}
    with (session / "results.csv").open("x", newline="", encoding="utf-8") as f:
        rows = csv.writer(f)
        rows.writerow(["batch", "trial", "dataset", "exit_code", "operator_result"])
        for trial in range(5 * args.batch - 4, 5 * args.batch + 1):
            if input(f"{trial}/20: 開始姿勢と配置を確認し、手を離してEnter（文字入力で終了）: "):
                break
            name = f"rollout_so101_{session.name}_take{trial:02d}"
            command = [sys.executable, str(Path(__file__).with_name("rollout_current_start.py")),
                       *OPTIONS, f"--robot.port={args.port}", f"--policy.path={args.model.resolve()}",
                       f"--robot.cameras={json.dumps(cameras)}", f"--dataset.repo_id=local/{name}",
                       f"--dataset.root={session / name}"]
            code = subprocess.run(command).returncode
            result = input("結果を入力（成功／失敗／中断）: ") if code == 0 else "実行エラー"
            rows.writerow([args.batch, trial, name, code, result])
            f.flush()
            if code:
                raise SystemExit(code)
    print(session)

if __name__ == "__main__":
    main()
