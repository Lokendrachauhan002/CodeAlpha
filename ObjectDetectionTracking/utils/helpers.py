"""Video, association, and drawing helpers used by main.py."""
from __future__ import annotations

import cv2
import numpy as np


def open_video_source(source: int | str) -> cv2.VideoCapture:
    """Open a webcam index or file path, with helpful errors."""
    if isinstance(source, str):
        from pathlib import Path
        if not Path(source).is_file():
            raise FileNotFoundError(f"Video file not found: {source}")
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        kind = f"webcam {source}" if isinstance(source, int) else f"video '{source}'"
        raise RuntimeError(f"Could not open {kind}. Check the camera/file and permissions.")
    return capture


def _iou(one: np.ndarray, many: np.ndarray) -> np.ndarray:
    """IoU between one xyxy box and a group of xyxy boxes."""
    left_top, right_bottom = np.maximum(one[:2], many[:, :2]), np.minimum(one[2:], many[:, 2:])
    wh = np.maximum(0, right_bottom - left_top)
    intersection = wh[:, 0] * wh[:, 1]
    union = (one[2] - one[0]) * (one[3] - one[1]) + (many[:, 2] - many[:, 0]) * (many[:, 3] - many[:, 1]) - intersection
    return intersection / np.maximum(union, 1e-6)


def match_tracks_to_detections(tracks: np.ndarray, detections: np.ndarray) -> dict[int, tuple[int, float]]:
    """Attach class/confidence from the nearest overlapping detection to each track."""
    result: dict[int, tuple[int, float]] = {}
    if len(detections) == 0:
        return result
    for track in tracks:
        best = int(np.argmax(_iou(track[:4], detections[:, :4])))
        if _iou(track[:4], detections[best:best + 1, :4])[0] >= 0.1:
            result[int(track[4])] = (int(detections[best, 5]), float(detections[best, 4]))
    return result


def color_for_class(class_id: int) -> tuple[int, int, int]:
    """Create a repeatable bright BGR color for a class."""
    return ((37 * class_id + 80) % 256, (17 * class_id + 160) % 256, (29 * class_id + 220) % 256)


def draw_track(frame: np.ndarray, box: tuple[float, float, float, float], track_id: int, label: str, confidence: float, class_id: int) -> None:
    """Draw one labelled bounding box and its persistent tracking ID."""
    x1, y1, x2, y2 = map(int, box)
    color = color_for_class(class_id)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    text = f"ID {track_id} | {label} {confidence:.0%}"
    (width, height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    cv2.rectangle(frame, (x1, max(0, y1 - height - 10)), (x1 + width + 6, y1), color, -1)
    cv2.putText(frame, text, (x1 + 3, max(height + 2, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)


def draw_fps(frame: np.ndarray, fps: float) -> None:
    """Display a smoothed frames-per-second measurement."""
    cv2.putText(frame, f"FPS: {fps:.1f}", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
