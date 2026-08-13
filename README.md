# Object Tracking with OpenCV

A Python project demonstrating single-object and multi-object tracking using OpenCV's legacy tracker API (`cv2.legacy`). Supports tracking on a video file or a **live phone camera feed** streamed over Wi-Fi.



---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Single Object Tracking](#single-object-tracking)
  - [Multiple Object Tracking](#multiple-object-tracking)
  - [Live Tracking via Phone Camera](#live-tracking-via-phone-camera)
- [Choosing a Tracker Algorithm](#choosing-a-tracker-algorithm)
- [Controls](#controls)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Single-object tracking** (`ObjectTracking.py`) — select one region of interest (ROI) on the first frame and track it through the rest of the video.
- **Multi-object tracking** (`Multiple_Object_Tracking.py`) — select multiple ROIs and track all of them simultaneously using `cv2.legacy.MultiTracker`.
- **Pluggable tracker algorithms** — switch between BOOSTING, MIL, KCF, TLD, MEDIANFLOW, MOSSE, and CSRT with a single variable.
- **Live camera support** — point the video source at an IP Webcam stream from your Android phone instead of a local file, for real-time tracking.

---

## Project Structure

```
object-tracking/
├── ObjectTracking.py            # Single object tracker
├── Multiple_Object_Tracking.py  # Multi object tracker
├── race.mp4                     # Sample input video
├── track/                       # Python virtual environment (not committed)
├── docs/
│   └── images/                  # Screenshots referenced in this README
└── README.md
```

---

## Prerequisites

- Python 3.9–3.12 recommended (OpenCV's contrib wheels may lag behind the very latest Python releases).
- A webcam or video file, OR an Android phone with the **IP Webcam** app for live tracking.
- Both your phone and computer on the **same Wi-Fi network** if using live camera mode.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/PrinceVerma04/object-tracking.git
   cd object-tracking
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv track
   source track/bin/activate       # Linux / macOS
   track\Scripts\activate          # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install opencv-contrib-python numpy
   ```

   > `cv2.legacy.*` trackers (BOOSTING, MIL, KCF, TLD, MEDIANFLOW, MOSSE, CSRT) only ship in **`opencv-contrib-python`**, not the plain `opencv-python` package.

---

## Usage

### Single Object Tracking

Run:

```bash
python ObjectTracking.py
```

1. The first frame of the video opens in a window.
2. **Drag a box** around the object you want to track.
3. Press **Enter** or **Space** to confirm the selection (press `c` to cancel and redraw).

![ROI selection](docs/images/roi-selection.png)
*Replace with a screenshot of the ROI selection window (`cv2.selectROI`).*

4. Tracking starts automatically — a colored rectangle follows the object frame by frame, with the tracker name displayed on screen.

![Tracking in progress](docs/images/tracking-in-progress.png)
*Replace with a screenshot of the video mid-track, showing the bounding box and tracker label.*

5. If tracking is lost, `"Tracking Failure"` is displayed in red.
6. Press **ESC** to quit.

### Multiple Object Tracking

Run:

```bash
python Multiple_Object_Tracking.py
```

1. The first frame opens for ROI selection.
2. Draw a box around an object, then:
   - Press **any key** to select another object.
   - Press **`Q`** once you're done selecting, to start tracking.
3. All selected objects are tracked simultaneously, each with its own colored bounding box.

![Multi-object tracking](docs/images/multi-object-tracking.png)
*Replace with a screenshot showing multiple bounding boxes on different objects.*

4. Press **ESC** to quit.

### Live Tracking via Phone Camera

You can track objects live using your phone's camera instead of a video file, using the **IP Webcam** Android app.

1. **Install IP Webcam** from the Play Store on your Android phone.
2. **Connect your phone to the same Wi-Fi network** as your computer.
3. Open the app and tap **"Start server"**.

![IP Webcam start screen](docs/images/ip-webcam-start.png)
*Replace with a screenshot of the IP Webcam app's start screen / running server showing the IP address.*

4. Note the URL shown on the phone's screen, e.g. `http://192.168.0.49:8080`.
5. Verify it works by opening `http://192.168.0.49:8080/video` in a browser on your computer — you should see a live MJPEG stream.
6. In `ObjectTracking.py`, point the video capture at that stream:

   ```python
   video = cv2.VideoCapture("http://192.168.0.49:8080/video")
   ```

7. Run the script as usual:

   ```bash
   python ObjectTracking.py
   ```

8. Select an ROI on the live feed — tracking now runs in real time on the phone's camera.

> **Note:** CSRT is accurate but computationally heavier, which can introduce lag on a live stream. If tracking feels sluggish, switch `tracker_type` to `"KCF"` for a faster (slightly less accurate) tracker better suited to real-time feeds.

---

## Choosing a Tracker Algorithm

Change the `tracker_type` variable near the top of `ObjectTracking.py`:

```python
tracker_type = "CSRT"
```

| Tracker    | Speed     | Accuracy  | Notes                                              |
|------------|-----------|-----------|-----------------------------------------------------|
| BOOSTING   | Fast      | Low       | Oldest algorithm, prone to drift                   |
| MIL        | Fast      | Low-Med   | Better than BOOSTING, still drifts under occlusion |
| KCF        | Fast      | Medium    | Good speed/accuracy balance, struggles with occlusion |
| TLD        | Slow      | Medium    | Can recover after losing the object, prone to false positives |
| MEDIANFLOW | Fast      | Medium    | Good for predictable, steady motion; fails on fast motion |
| MOSSE      | Very Fast | Low       | Extremely lightweight, best for real-time on limited hardware |
| CSRT       | Slow      | High      | Most accurate, handles scale/rotation changes well, best for drift-prone footage |

---

## Controls

| Key            | Action                                  |
|----------------|------------------------------------------|
| Drag mouse     | Draw ROI box during selection            |
| Enter / Space  | Confirm ROI selection                    |
| `c`            | Cancel ROI selection and redraw          |
| Any key (multi-object mode) | Confirm current ROI, select another |
| `Q`            | Finish selecting objects (multi-object mode only) |
| `ESC`          | Quit tracking window                     |

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'cv2'`** — activate the virtual environment and run `pip install opencv-contrib-python`.
- **`AttributeError: module 'cv2' has no attribute 'legacy'`** — you have plain `opencv-python` installed instead of `opencv-contrib-python`. Uninstall and reinstall the contrib package.
- **`error loading the video`** — check the video path in the script matches where `race.mp4` actually is, or that your IP Webcam URL is correct and reachable.
- **Live stream doesn't connect** — confirm both devices are on the same Wi-Fi network, the IP Webcam server is running, and the `/video` URL loads in a browser first.
- **Bounding box drifts off the object** — switch to a more accurate tracker like `CSRT`.
- **Tracking feels laggy on a live feed** — switch to a faster tracker like `KCF` or `MOSSE`.

---

## License

This project currently has no license file. Add one (e.g. MIT) if you intend for others to reuse this code.
