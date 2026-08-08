"""A small, reusable wrapper around the Ultralytics YOLOv8 detector."""
from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
from ultralytics import YOLO


class YOLODetector:
    """Loads YOLO once and converts its predictions into SORT-friendly arrays."""

    WEIGHTS_URL = "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt"

    def __init__(self, model_path: Path, confidence: float = 0.40) -> None:
        self.model_path = model_path
        self.confidence = confidence
        self._download_weights_if_needed()
        try:
            self.model = YOLO(str(self.model_path))
        except Exception as error:
            raise RuntimeError(f"Could not load YOLO model '{self.model_path}': {error}") from error
        self.names = self.model.names

    def _download_weights_if_needed(self) -> None:
        """Download the small official YOLOv8 model on first use."""
        if self.model_path.is_file():
            return
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"YOLO weights were not found. Downloading to {self.model_path} ...")
        try:
            urlretrieve(self.WEIGHTS_URL, self.model_path)
        except Exception as error:
            raise FileNotFoundError(
                f"Missing model and download failed. Download yolov8n.pt manually into '{self.model_path.parent}'."
            ) from error

    def detect(self, frame: np.ndarray) -> np.ndarray:
        """Return [x1, y1, x2, y2, confidence, class_id] per retained detection."""
        result = self.model.predict(frame, conf=self.confidence, verbose=False)[0]
        if result.boxes is None or len(result.boxes) == 0:
            return np.empty((0, 6), dtype=np.float32)
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy().reshape(-1, 1)
        class_ids = result.boxes.cls.cpu().numpy().reshape(-1, 1)
        return np.hstack((boxes, confidences, class_ids)).astype(np.float32)

    def class_name(self, class_id: int) -> str:
        """Safely look up a COCO class name."""
        return str(self.names.get(class_id, f"class-{class_id}"))
