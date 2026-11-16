"""LeRobot 0.6.1. Select the physical arm and its stable USB port."""
import argparse
import subprocess

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("role", choices=["leader", "follower"])
    p.add_argument("--port", required=True)
    p.add_argument("--id", help="ID associated with the saved calibration")
    args = p.parse_args()
    group = "teleop" if args.role == "leader" else "robot"
    arm_id = args.id or ("black_leader" if args.role == "leader" else "white_follower")
    subprocess.run(["lerobot-calibrate", f"--{group}.type=so101_{args.role}",
                    f"--{group}.port={args.port}", f"--{group}.id={arm_id}"], check=True)

if __name__ == "__main__":
    main()
