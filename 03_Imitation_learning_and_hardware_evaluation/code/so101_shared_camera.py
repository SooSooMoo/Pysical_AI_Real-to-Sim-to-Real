"""LeRobot camera adapter for the existing Windows atomic JPEG publisher."""
from dataclasses import dataclass
from pathlib import Path
import os
import time

import cv2
import numpy as np

from lerobot.cameras.camera import Camera
from lerobot.cameras.configs import CameraConfig


@CameraConfig.register_subclass("so101_shared_jpeg")
@dataclass(kw_only=True)
class SharedJpegCameraConfig(CameraConfig):
    path: str = "latest.jpg"
    fps: int = 5
    width: int = 640
    height: int = 480


class SharedJpegCamera(Camera):
    def __init__(self, config: SharedJpegCameraConfig):
        super().__init__(config)
        self.path = Path(config.path)
        self._connected = False
        self._last_stamp = None
        self._observed_stamp = None
        self._observed_at = None
        self._rgb = None

    @property
    def is_connected(self):
        return self._connected

    @staticmethod
    def find_cameras():
        return []

    def connect(self, warmup=True):
        if self._connected:
            raise RuntimeError("Camera already connected")
        # Require a change after connecting, not just a leftover JPEG.
        self._last_stamp = self.path.stat().st_mtime_ns if self.path.exists() else None
        self._connected = True
        try:
            self.async_read(timeout_ms=2000)
        except Exception:
            self._connected = False
            raise

    def _load(self, max_age_ms=1000):
        # Read metadata and bytes from the same open file across atomic replacements.
        with self.path.open("rb") as handle:
            stat = os.fstat(handle.fileno())
            if stat.st_mtime_ns != self._observed_stamp:
                data = handle.read()
                bgr = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
                if bgr is None:
                    raise OSError("Cannot decode shared JPEG")
                if bgr.shape != (self.height, self.width, 3):
                    raise ValueError(f"Expected {self.width}x{self.height} RGB, got {bgr.shape}")
                self._rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                self._observed_stamp = stat.st_mtime_ns
                self._observed_at = time.monotonic()
        # Compare elapsed time only on the receiving host, never Windows wall time.
        if time.monotonic() - self._observed_at > max_age_ms / 1000:
            raise TimeoutError(f"Shared JPEG has not updated for {max_age_ms} ms")
        return self._observed_stamp, self._rgb

    def async_read(self, timeout_ms=200):
        if not self.is_connected:
            raise RuntimeError("Camera is not connected")
        deadline = time.monotonic() + timeout_ms / 1000
        last_error = None
        while True:
            try:
                stamp, rgb = self._load()
                if stamp != self._last_stamp:
                    self._last_stamp = stamp
                    return rgb
            except (OSError, TimeoutError) as exc:
                last_error = exc
            if time.monotonic() >= deadline:
                raise TimeoutError("No fresh camera frame; check the Windows publisher") from last_error
            time.sleep(0.005)

    def read(self):
        return self.async_read()

    def read_latest(self, max_age_ms=1000):
        if not self.is_connected:
            raise RuntimeError("Camera is not connected")
        return self._load(max_age_ms)[1]

    def disconnect(self):
        self._connected = False
        self._last_stamp = None
        self._observed_stamp = None
        self._observed_at = None
        self._rgb = None


def check_camera():
    from lerobot.cameras.utils import make_cameras_from_configs

    camera = make_cameras_from_configs({"workspace": SharedJpegCameraConfig()})["workspace"]
    print("Checking read_latest at 30 Hz for 30 seconds (no robot connection)...", flush=True)
    with camera:
        start = time.monotonic()
        stamps = set()
        for index in range(900):
            frame = camera.read_latest()
            stamps.add(camera._observed_stamp)
            if frame.dtype != np.uint8 or frame.shape != (480, 640, 3):
                raise RuntimeError(f"Unexpected frame: {frame.shape}, {frame.dtype}")
            time.sleep(max(0, start + (index + 1) / 30 - time.monotonic()))
        elapsed = time.monotonic() - start
        print(f"PASS: 900 reads / {elapsed:.1f} seconds; {len(stamps)} distinct frames")
        print(f"Read rate: {900 / elapsed:.1f} Hz; shape: {frame.shape}; dtype: {frame.dtype}")
    print("No robot was connected. No dataset was recorded or uploaded.")


