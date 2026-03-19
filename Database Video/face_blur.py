#!/usr/bin/env python3
"""
Face Blur Script — SSWS Clinical Data Platform

Oscura i volti nei video clinici con blur ellittico multi-passaggio.
1. Rileva volti su tutti i frame, calcola traiettoria smooth
2. Applica blur ellittico
3. Ri-analizza il video blurrato: se trova ancora volti, corregge
4. Ripete finché il volto non è completamente coperto

Uso:
    python face_blur.py input.mp4
    python face_blur.py input.mp4 -o output.mp4
"""

import argparse
import subprocess
import sys
import urllib.request
from pathlib import Path

import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

SCRIPT_DIR = Path(__file__).parent
MP_MODEL_PATH = SCRIPT_DIR / "blaze_face_short_range.tflite"
MP_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite"
DNN_PROTO_PATH = SCRIPT_DIR / "deploy.prototxt"
DNN_MODEL_PATH = SCRIPT_DIR / "res10_300x300_ssd_iter_140000.caffemodel"
DNN_PROTO_URL = "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt"
DNN_MODEL_URL = "https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"


def ensure_models():
    for path, url, name in [
        (MP_MODEL_PATH, MP_MODEL_URL, "MediaPipe BlazeFace"),
        (DNN_PROTO_PATH, DNN_PROTO_URL, "OpenCV DNN prototxt"),
        (DNN_MODEL_PATH, DNN_MODEL_URL, "OpenCV DNN caffemodel"),
    ]:
        if not path.exists():
            print(f"  Scaricamento {name}...")
            urllib.request.urlretrieve(url, path)


def create_detectors(min_confidence=0.3):
    ensure_models()
    dnn_net = cv2.dnn.readNetFromCaffe(str(DNN_PROTO_PATH), str(DNN_MODEL_PATH))
    base_options = mp_python.BaseOptions(model_asset_path=str(MP_MODEL_PATH))
    options = vision.FaceDetectorOptions(
        base_options=base_options,
        min_detection_confidence=min_confidence,
    )
    mp_detector = vision.FaceDetector.create_from_options(options)
    return dnn_net, mp_detector


def detect_faces_dnn(frame, net, min_confidence=0.3):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
    )
    net.setInput(blob)
    detections = net.forward()
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > min_confidence:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype(int)
            faces.append((x1, y1, x2, y2, float(confidence)))
    return faces


def detect_faces_mediapipe(frame, mp_detector):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = mp_detector.detect(mp_image)
    faces = []
    if results.detections:
        h, w = frame.shape[:2]
        for det in results.detections:
            bbox = det.bounding_box
            faces.append((
                bbox.origin_x, bbox.origin_y,
                bbox.origin_x + bbox.width, bbox.origin_y + bbox.height,
                det.categories[0].score if det.categories else 0.5
            ))
    return faces


def best_face_near(dnn_faces, mp_faces, current_pos, max_distance=150):
    all_faces = list(dnn_faces) + list(mp_faces)
    if not all_faces:
        return None
    if current_pos is None:
        return max(all_faces, key=lambda f: f[4])
    cx_curr, cy_curr = current_pos
    nearby = []
    for face in all_faces:
        x1, y1, x2, y2, conf = face
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        dist = ((cx - cx_curr) ** 2 + (cy - cy_curr) ** 2) ** 0.5
        if dist < max_distance:
            nearby.append(face)
    if not nearby:
        return None
    return max(nearby, key=lambda f: f[4])


def scan_all_faces(cap, dnn_net, mp_detector, total_frames, min_confidence=0.3):
    """Scansiona tutto il video e restituisce le detection per ogni frame."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    detections_per_frame = {}
    current_pos = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        dnn_faces = detect_faces_dnn(frame, dnn_net, min_confidence)
        mp_faces = detect_faces_mediapipe(frame, mp_detector)
        face = best_face_near(dnn_faces, mp_faces, current_pos)

        if face is not None:
            x1, y1, x2, y2, conf = face
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            fw = x2 - x1
            fh = y2 - y1
            detections_per_frame[frame_idx] = (cx, cy, fw, fh)
            current_pos = (cx, cy)

        if frame_idx % 60 == 0:
            pct = (frame_idx / total_frames * 100) if total_frames > 0 else 0
            n = len(detections_per_frame)
            print(f"\r    Scansione: {frame_idx}/{total_frames} ({pct:.0f}%) — {n} detection",
                  end="", flush=True)

    print()
    return detections_per_frame, frame_idx


def compute_smooth_trajectory(detections, total_frames, smoothing=0.12, expand=0.15):
    """
    Calcola una traiettoria smooth dell'ellisse per ogni frame.
    Restituisce dict: frame_idx -> (cx, cy, rx, ry)
    """
    if not detections:
        return {}

    trajectory = {}
    smooth_cx = None
    smooth_cy = None
    smooth_rx = None
    smooth_ry = None

    for frame_idx in range(1, total_frames + 1):
        if frame_idx in detections:
            cx, cy, fw, fh = detections[frame_idx]
            det_rx = fw / 2 * (1 + expand * 0.5)
            det_ry = fh / 2 * (1 + expand)

            if smooth_cx is None:
                smooth_cx = cx
                smooth_cy = cy
                smooth_rx = det_rx
                smooth_ry = det_ry
            else:
                smooth_cx += smoothing * (cx - smooth_cx)
                smooth_cy += smoothing * (cy - smooth_cy)
                smooth_rx += smoothing * (det_rx - smooth_rx)
                smooth_ry += smoothing * (det_ry - smooth_ry)

        if smooth_cx is not None:
            trajectory[frame_idx] = (
                int(smooth_cx), int(smooth_cy),
                int(smooth_rx), int(smooth_ry)
            )

    return trajectory


def apply_blur(cap, writer, trajectory, total_frames, blur_strength=99):
    """Applica il blur ellittico seguendo la traiettoria pre-calcolata."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    kernel = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
    frame_idx = 0
    masked = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        if frame_idx in trajectory:
            cx, cy, rx, ry = trajectory[frame_idx]
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.ellipse(mask, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
            blurred_frame = cv2.GaussianBlur(frame, (kernel, kernel), 30)
            mask_3ch = cv2.merge([mask, mask, mask])
            frame = np.where(mask_3ch == 255, blurred_frame, frame)
            masked += 1

        writer.write(frame)

        if frame_idx % 60 == 0 or frame_idx == total_frames:
            pct = (frame_idx / total_frames * 100) if total_frames > 0 else 0
            print(f"\r    Applicazione: {frame_idx}/{total_frames} ({pct:.0f}%)",
                  end="", flush=True)

    print()
    return masked


def check_remaining_faces(video_path, dnn_net, mp_detector, min_confidence=0.3):
    """Controlla se ci sono ancora volti visibili nel video blurrato."""
    cap = cv2.VideoCapture(str(video_path))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    uncovered_frames = {}
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        # Controlla ogni 2 frame per velocità
        if frame_idx % 2 != 0:
            continue

        dnn_faces = detect_faces_dnn(frame, dnn_net, min_confidence)
        mp_faces = detect_faces_mediapipe(frame, mp_detector)
        all_faces = list(dnn_faces) + list(mp_faces)

        if all_faces:
            best = max(all_faces, key=lambda f: f[4])
            x1, y1, x2, y2, conf = best
            uncovered_frames[frame_idx] = ((x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1)

        if frame_idx % 60 == 0:
            pct = (frame_idx / total * 100) if total > 0 else 0
            print(f"\r    Verifica: {frame_idx}/{total} ({pct:.0f}%) — {len(uncovered_frames)} scoperti",
                  end="", flush=True)

    cap.release()
    print()
    return uncovered_frames


def merge_trajectories(original_traj, corrections, total_frames, smoothing=0.12, expand=0.15):
    """Unisci la traiettoria originale con le correzioni dal secondo passaggio."""
    # Aggiungi le correzioni come detection aggiuntive
    merged_detections = {}
    for frame_idx, (cx, cy, rx, ry) in original_traj.items():
        merged_detections[frame_idx] = (cx, cy, rx * 2, ry * 2)  # converti back

    for frame_idx, (cx, cy, fw, fh) in corrections.items():
        if frame_idx in merged_detections:
            # Media tra posizione attuale e correzione, con ellisse un po' più grande
            ocx, ocy, ofw, ofh = merged_detections[frame_idx]
            merged_detections[frame_idx] = (
                (ocx + cx) / 2, (ocy + cy) / 2,
                max(ofw, fw) * 1.15, max(ofh, fh) * 1.15
            )
        else:
            merged_detections[frame_idx] = (cx, cy, fw * 1.15, fh * 1.15)

    return compute_smooth_trajectory(merged_detections, total_frames, smoothing, expand)


def encode_final(temp_avi, output_path, input_path):
    """Ricodifica in MP4 e copia audio."""
    subprocess.run(
        ['ffmpeg', '-y', '-i', str(temp_avi),
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
         '-movflags', '+faststart', str(output_path)],
        capture_output=True, text=True
    )
    if temp_avi.exists():
        temp_avi.unlink()

    # Copia audio
    probe = subprocess.run(
        ['ffmpeg', '-i', str(input_path), '-hide_banner'],
        capture_output=True, text=True
    )
    if 'Audio:' in probe.stderr:
        final = output_path.parent / f"{output_path.stem}_final{output_path.suffix}"
        subprocess.run(
            ['ffmpeg', '-y', '-i', str(output_path), '-i', str(input_path),
             '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0',
             '-movflags', '+faststart', str(final)],
            capture_output=True, text=True
        )
        output_path.unlink()
        final.rename(output_path)
        return True
    return False


def process_video(input_path, output_path, min_confidence=0.3, blur_strength=99,
                  smoothing=0.12, expand=0.15, max_passes=3):
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"ERRORE: File non trovato: {input_path}")
        sys.exit(1)

    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_masked{input_path.suffix}"
    output_path = Path(output_path)

    cap = cv2.VideoCapture(str(input_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print(f"Video:  {width}x{height} @ {fps:.1f}fps, {duration:.1f}s ({total_frames} frame)")
    print(f"Max passaggi: {max_passes}")
    print()

    dnn_net, mp_detector = create_detectors(min_confidence)

    # === PASSAGGIO 1: scansione e blur iniziale ===
    print("PASSAGGIO 1: scansione volti...")
    detections, _ = scan_all_faces(cap, dnn_net, mp_detector, total_frames, min_confidence)
    print(f"    {len(detections)} frame con volti rilevati")

    trajectory = compute_smooth_trajectory(detections, total_frames, smoothing, expand)

    print("  Applicazione blur...")
    temp_avi = output_path.parent / f"{output_path.stem}_temp.avi"
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    writer = cv2.VideoWriter(str(temp_avi), fourcc, fps, (width, height))
    masked = apply_blur(cap, writer, trajectory, total_frames, blur_strength)
    writer.release()
    cap.release()

    print(f"    {masked} frame mascherati")
    print("  Ricodifica...")
    encode_final(temp_avi, output_path, input_path)

    # === PASSAGGI SUCCESSIVI: verifica e correzione ===
    for pass_num in range(2, max_passes + 1):
        print(f"\nPASSAGGIO {pass_num}: verifica volti residui...")
        uncovered = check_remaining_faces(output_path, dnn_net, mp_detector, min_confidence)

        if not uncovered:
            print(f"    Nessun volto residuo trovato. Perfetto!")
            break

        print(f"    {len(uncovered)} frame con volti ancora visibili. Correggo...")

        # Ricalcola traiettoria con le correzioni
        trajectory = merge_trajectories(trajectory, uncovered, total_frames, smoothing, expand)

        # Riapplica il blur dal video ORIGINALE (non dal blurrato)
        cap = cv2.VideoCapture(str(input_path))
        temp_avi = output_path.parent / f"{output_path.stem}_temp.avi"
        writer = cv2.VideoWriter(str(temp_avi), fourcc, fps, (width, height))
        masked = apply_blur(cap, writer, trajectory, total_frames, blur_strength)
        writer.release()
        cap.release()

        print(f"    {masked} frame mascherati")
        print("  Ricodifica...")
        encode_final(temp_avi, output_path, input_path)
    else:
        # Controlla un'ultima volta
        remaining = check_remaining_faces(output_path, dnn_net, mp_detector, min_confidence)
        if remaining:
            print(f"\n  NOTA: {len(remaining)} frame hanno ancora volti parzialmente visibili dopo {max_passes} passaggi.")

    input_size = input_path.stat().st_size / (1024 * 1024)
    output_size = output_path.stat().st_size / (1024 * 1024)

    print(f"\n  COMPLETATO!")
    print(f"  Dimensione: {input_size:.1f} MB → {output_size:.1f} MB")
    print(f"  Output:     {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Oscura volti nei video clinici — multi-passaggio con verifica"
    )
    parser.add_argument('input', help="Video di input")
    parser.add_argument('-o', '--output', help="Video di output")
    parser.add_argument('--min-confidence', type=float, default=0.3)
    parser.add_argument('--blur-strength', type=int, default=99)
    parser.add_argument('--smoothing', type=float, default=0.12)
    parser.add_argument('--expand', type=float, default=0.15)
    parser.add_argument('--max-passes', type=int, default=3,
                        help="Numero massimo di passaggi di correzione (default: 3)")

    args = parser.parse_args()
    process_video(args.input, args.output, args.min_confidence,
                  args.blur_strength, args.smoothing, args.expand, args.max_passes)


if __name__ == '__main__':
    main()
