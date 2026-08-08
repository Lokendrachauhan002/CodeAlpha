# Object Detection and Tracking

A beginner-friendly real-time computer-vision application. It detects COCO objects with YOLOv8 and keeps a stable ID for each visible object using SORT (Simple Online and Realtime Tracking).

## Features

- Webcam (`--source 0`) and video-file input
- YOLOv8 object classes, confidence scores, coloured bounding boxes, and FPS
- SORT tracking IDs, Kalman prediction, IoU matching, and graceful error handling
- Press **Q** to close; `Ctrl+C` is handled safely

## Project layout

```text
ObjectDetectionTracking/
├── main.py                 # application loop
├── detector.py             # YOLO loading and inference
├── tracker.py              # self-contained SORT implementation
├── requirements.txt
├── sample_video.mp4        # replace the included text placeholder with an MP4
├── models/yolov8n.pt       # downloaded automatically on first run
└── utils/helpers.py        # display/video helper functions
```

`sample_video.mp4` is a small text placeholder because a real video is a large binary asset and is not included in source code. Download any legal MP4 (or record one), replace that file, and run the video command below.

## Installation (Windows / VS Code)

1. Install [Python 3.10 or newer](https://www.python.org/downloads/) and tick **Add Python to PATH**.
2. In VS Code, open the `ObjectDetectionTracking` folder and open its terminal.
3. Create and activate an isolated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Run from the project folder:

```powershell
python main.py --source 0
python main.py --source sample_video.mp4
```

The app downloads the official lightweight `yolov8n.pt` to `models/` on its first run. If offline, download YOLOv8 Nano weights manually from the [Ultralytics assets release](https://github.com/ultralytics/assets/releases) and save them as `models/yolov8n.pt`. SORT is implemented in `tracker.py`; no separate, unmaintained SORT package is needed.

Useful options:

```powershell
python main.py --source 1 --confidence 0.5 --width 640
python main.py --source my_video.mp4 --skip-frames 1
```

## Expected output

A window shows each object as a coloured rectangle, for example `ID 4 | person 92%`, and `FPS: 28.6` in the upper-left. The same walking person should retain ID 4 while it remains visible. IDs increase for newly created tracks; they are not class IDs.

## How the program works

1. `main.py` uses `cv2.VideoCapture` to read one BGR image frame at a time.
2. `detector.py` sends that frame to YOLO. YOLO returns box corners `(x1, y1, x2, y2)`, a class number, and confidence. Low-confidence results are filtered by `--confidence`.
3. `tracker.py` predicts existing boxes with a Kalman filter, calculates IoU between predictions and new detections, and uses the Hungarian algorithm to choose one-to-one matches. A matching track retains its ID; an unmatched detection starts a new ID.
4. `helpers.py` matches each output track back to its detection for the class/confidence and draws labels, rectangles, and FPS with OpenCV.

## Source-code explanation

Every source line has an adjacent docstring or comment where a non-obvious action occurs. Read the files in this order:

- `main.py`: parses command-line inputs, opens the model/video, loops over frames, optionally resizes/skips inference, calls detector and tracker, calculates an exponentially smoothed FPS, displays the frame, and releases resources in `finally`.
- `detector.py`: `YOLODetector.__init__` checks/downloads weights and loads YOLO once. `detect` transforms Ultralytics tensors into an `N x 6` NumPy array `[x1,y1,x2,y2,confidence,class_id]`. `class_name` converts COCO's numeric class into readable text.
- `tracker.py`: conversion functions translate between box corners and Kalman state. `KalmanBoxTracker` predicts movement and corrects it with a matched observation. `Sort.update` computes IoU, Hungarian matches, creates/removes tracks, and exposes confirmed `[x1,y1,x2,y2,id]` rows.
- `utils/helpers.py`: validates input, calculates track/detection overlap, selects repeatable colours, then uses `cv2.rectangle` and `cv2.putText` to render boxes and labels.

## Error handling

The app reports unavailable webcam/video input, missing model/download errors, model load errors, empty frames, and `Ctrl+C`. A video ending is treated as normal. Close other apps using the camera if the webcam cannot open.

## Performance tips

- Use `yolov8n.pt` (already selected) or a smaller input width such as `--width 640`.
- Install a CUDA-compatible PyTorch build and use an NVIDIA GPU; Ultralytics will select it when available.
- Resize frames before inference, use `--skip-frames 1` or more for slow hardware, and reduce webcam resolution in camera settings.
- For offline processing, batch frames/images where latency is less important. Real-time webcam display normally favours one frame at a time.

## Optional enhancements

| Enhancement | Practical approach |
|---|---|
| Person/vehicle count | Maintain a set of unique track IDs whose class is person/car/bus/truck. |
| Line crossing | Store each track centre from the prior frame; count when it moves across a defined line. |
| Speed estimation | Calibrate pixels to metres with a known scene distance, then divide displacement by elapsed time. |
| Face detection/recognition | Add a face detector; recognition additionally needs consent, secure embeddings, and a labelled database. |
| License plates | Run a plate detector/OCR model on vehicle crops and protect collected data. |
| Record video | Create `cv2.VideoWriter` after reading frame dimensions and call `writer.write(frame)`. |
| CSV counts | Write timestamps, ID, class, and crossing/count event through Python's `csv` module. |
| GUI | Put capture/inference in a worker thread and render frames in Tkinter/PyQt without blocking its event loop. |

See [the project report](docs/PROJECT_REPORT.md) and [30+ viva questions](docs/VIVA_QUESTIONS.md).
