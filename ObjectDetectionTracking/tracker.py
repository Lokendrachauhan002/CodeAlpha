"""Dependency-light SORT tracker (Kalman filter plus IoU/Hungarian matching)."""
from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment


def iou_batch(boxes_a: np.ndarray, boxes_b: np.ndarray) -> np.ndarray:
    """Compute intersection-over-union for every pair of xyxy boxes."""
    if len(boxes_a) == 0 or len(boxes_b) == 0:
        return np.empty((len(boxes_a), len(boxes_b)))
    left_top = np.maximum(boxes_a[:, None, :2], boxes_b[None, :, :2])
    right_bottom = np.minimum(boxes_a[:, None, 2:], boxes_b[None, :, 2:])
    wh = np.maximum(0.0, right_bottom - left_top)
    intersection = wh[:, :, 0] * wh[:, :, 1]
    area_a = np.maximum(0.0, boxes_a[:, 2] - boxes_a[:, 0]) * np.maximum(0.0, boxes_a[:, 3] - boxes_a[:, 1])
    area_b = np.maximum(0.0, boxes_b[:, 2] - boxes_b[:, 0]) * np.maximum(0.0, boxes_b[:, 3] - boxes_b[:, 1])
    return intersection / np.maximum(area_a[:, None] + area_b[None, :] - intersection, 1e-6)


def xyxy_to_z(box: np.ndarray) -> np.ndarray:
    """Convert xyxy into SORT's [center-x, center-y, area, aspect-ratio] state."""
    width, height = box[2] - box[0], box[3] - box[1]
    return np.array([(box[0] + box[2]) / 2, (box[1] + box[3]) / 2, width * height, width / max(height, 1e-6)])


def x_to_xyxy(state: np.ndarray) -> np.ndarray:
    """Convert a SORT state back to xyxy coordinates."""
    width = np.sqrt(max(state[2] * state[3], 0.0))
    height = state[2] / max(width, 1e-6)
    return np.array([state[0] - width / 2, state[1] - height / 2, state[0] + width / 2, state[1] + height / 2])


class KalmanBoxTracker:
    """Tracks one object using a constant-velocity Kalman filter."""

    next_id = 1

    def __init__(self, box: np.ndarray) -> None:
        self.id = KalmanBoxTracker.next_id
        KalmanBoxTracker.next_id += 1
        self.x = np.zeros(7)  # position: cx, cy, area, ratio; then three velocities
        self.x[:4] = xyxy_to_z(box)
        self.P = np.eye(7) * 10.0
        self.P[4:, 4:] *= 100.0
        self.F = np.eye(7)
        self.F[0, 4] = self.F[1, 5] = self.F[2, 6] = 1.0
        self.H = np.zeros((4, 7)); self.H[:4, :4] = np.eye(4)
        self.R = np.eye(4); self.R[2:, 2:] *= 10.0
        self.Q = np.eye(7) * 0.01; self.Q[4:, 4:] *= 0.1
        self.time_since_update = 0
        self.hits = 1

    def predict(self) -> np.ndarray:
        if self.x[2] + self.x[6] <= 0:  # avoid a negative predicted area
            self.x[6] = 0
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        self.time_since_update += 1
        return x_to_xyxy(self.x)

    def update(self, box: np.ndarray) -> None:
        measurement = xyxy_to_z(box)
        innovation = measurement - self.H @ self.x
        covariance = self.H @ self.P @ self.H.T + self.R
        gain = self.P @ self.H.T @ np.linalg.inv(covariance)
        self.x += gain @ innovation
        self.P = (np.eye(7) - gain @ self.H) @ self.P
        self.time_since_update = 0
        self.hits += 1

    def state_box(self) -> np.ndarray:
        return x_to_xyxy(self.x)


class Sort:
    """Associate detections by IoU and return confirmed [xyxy, tracking_id] tracks."""

    def __init__(self, max_age: int = 20, min_hits: int = 2, iou_threshold: float = 0.3) -> None:
        self.max_age, self.min_hits, self.iou_threshold = max_age, min_hits, iou_threshold
        self.trackers: list[KalmanBoxTracker] = []

    def update(self, detections: np.ndarray) -> np.ndarray:
        """Update tracker state from an Nx6 detector array and return Nx5 tracks."""
        detections = np.asarray(detections, dtype=float)
        detection_boxes = detections[:, :4] if len(detections) else np.empty((0, 4))
        predicted_boxes = np.array([tracker.predict() for tracker in self.trackers]) if self.trackers else np.empty((0, 4))
        overlaps = iou_batch(predicted_boxes, detection_boxes)
        row_indices, col_indices = linear_sum_assignment(-overlaps) if overlaps.size else (np.array([], dtype=int), np.array([], dtype=int))
        matches = [(r, c) for r, c in zip(row_indices, col_indices) if overlaps[r, c] >= self.iou_threshold]
        matched_tracks, matched_detections = {r for r, _ in matches}, {c for _, c in matches}
        for track_index, detection_index in matches:
            self.trackers[track_index].update(detection_boxes[detection_index])
        for detection_index in set(range(len(detection_boxes))) - matched_detections:
            self.trackers.append(KalmanBoxTracker(detection_boxes[detection_index]))
        self.trackers = [tracker for tracker in self.trackers if tracker.time_since_update <= self.max_age]
        visible = [np.r_[tracker.state_box(), tracker.id] for tracker in self.trackers if tracker.hits >= self.min_hits and tracker.time_since_update == 0]
        return np.asarray(visible, dtype=float).reshape(-1, 5) if visible else np.empty((0, 5))
