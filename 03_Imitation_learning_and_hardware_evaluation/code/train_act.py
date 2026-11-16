"""Train ACT with the settings used in the 16-train / 4-eval experiment."""
import argparse
from pathlib import Path
import subprocess
from datetime import datetime

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset", type=Path, required=True, help="Directory containing meta/info.json")
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args()
    dataset = args.dataset.resolve()
    if not (dataset / "meta/info.json").is_file():
        p.error("Missing dataset meta/info.json")
    output = args.output or Path("runs") / datetime.now().strftime("act_%Y%m%d_%H%M%S")
    subprocess.run([
        "lerobot-train", f"--dataset.repo_id=local/{dataset.name}", f"--dataset.root={dataset}",
        "--dataset.eval_split=0.2", "--dataset.video_backend=pyav",
        "--policy.type=act", "--policy.device=cuda", "--policy.use_amp=false",
        "--policy.chunk_size=100", "--policy.n_action_steps=100", "--policy.push_to_hub=false",
        "--batch_size=2", "--num_workers=0", "--steps=10000", "--seed=42",
        "--eval_steps=2000", "--save_freq=5000", "--log_freq=100", "--wandb.enable=false",
        f"--output_dir={output.resolve()}"
    ], check=True)

if __name__ == "__main__":
    main()
