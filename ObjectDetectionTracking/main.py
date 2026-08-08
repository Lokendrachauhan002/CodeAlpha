"""Entry point for real-time YOLO object detection and SORT tracking."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2

from detector import YOLODetector
from tracker import Sort
from utils.helpers import (
    draw_fps,
    draw_track,
    match_tracks_to_detections,
    open_video_source,
)


def parse_args() -> argparse.Namespace:
    """Read command-line settings while keeping useful beginner-friendly defaults."""
    parser = argparse.ArgumentParser(description="YOLOv8 + SORT object tracking")
    parser.add_argument("--source", default="0", help="Camera index (0) or video-file path")
    parser.add_argument("--model", default="models/yolov8n.pt", help="Path to YOLO weights")
    parser.add_argument("--confidence", type=float, default=0.40, help="Minimum detection confidence")
    parser.add_argument("--width", type=int, default=960, help="Resize frames to this width; 0 keeps original")
    parser.add_argument("--skip-frames", type=int, default=0, help="Detect every N+1 frames (0 = every frame)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = int(args.source) if args.source.isdigit() else args.source

    try:
        detector = YOLODetector(Path(args.model), confidence=args.confidence)
        tracker = Sort(max_age=20, min_hits=2, iou_threshold=0.30)
        capture = open_video_source(source)
    except (FileNotFoundError, RuntimeError, OSError) as error:
        print(f"Startup error: {error}")
        return 1

    previous_time = time.perf_counter()
    fps = 0.0
    frame_number = 0
    last_detections = []
    window_name = "Object Detection and Tracking - press Q to quit"

    try:
        while True:
            ok, frame = capture.read()
            if not ok or frame is None or frame.size == 0:
                # A video ends normally; a camera may briefly return an empty frame.
                if isinstance(source, str):
                    print("Video ended or an empty frame was received.")
                    break
                print("Empty webcam frame received; trying the next frame.")
                continue

            if args.width > 0 and frame.shape[1] != args.width:
                height = int(frame.shape[0] * args.width / frame.shape[1])
                frame = cv2.resize(frame, (args.width, height), interpolation=cv2.INTER_LINEAR)

            # Optionally reuse recent detections to reduce GPU/CPU inference load.
            if frame_number % (args.skip_frames + 1) == 0:
                last_detections = detector.detect(frame)
            tracks = tracker.update(last_detections)
            assignments = match_tracks_to_detections(tracks, last_detections)

            for track in tracks:
                x1, y1, x2, y2, track_id = track
                class_id, confidence = assignments.get(int(track_id), (-1, 0.0))
                label = detector.class_name(class_id) if class_id >= 0 else "object"
                draw_track(frame, (x1, y1, x2, y2), int(track_id), label, confidence, class_id)

            current_time = time.perf_counter()
            instantaneous_fps = 1.0 / max(current_time - previous_time, 1e-6)
            fps = instantaneous_fps if fps == 0 else 0.9 * fps + 0.1 * instantaneous_fps
            previous_time = current_time
            draw_fps(frame, fps)
            cv2.imshow(window_name, frame)

            frame_number += 1
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break
    except KeyboardInterrupt:
        print("Stopped by keyboard interrupt.")
    finally:
        capture.release()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    sys.exit(main())
