"""Run the existing rollout, seeding motor goals from measured position at setup."""
import math
import so101_shared_camera  # register the camera adapter
from lerobot.scripts.lerobot_rollout import main
from lerobot.robots.so_follower.so_follower import SOFollower

original_configure = SOFollower.configure


def configure_from_current(self):
    if not self.bus.is_calibrated:
        raise RuntimeError('Calibration mismatch before setup')
    pose = self.bus.sync_read('Present_Position', num_retry=2)
    if set(pose) != set(self.bus.motors) or not all(math.isfinite(v) for v in pose.values()):
        raise RuntimeError('Invalid starting position')
    print('Measured starting pose (no automatic alignment):', pose, flush=True)
    # Replace stale goals before the standard configure routine enables torque.
    self.bus.sync_write('Goal_Position', pose)
    original_configure(self)


SOFollower.configure = configure_from_current

if __name__ == '__main__':
    main()
