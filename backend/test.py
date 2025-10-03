import cv2
import os
import shutil
from ultralytics import YOLO
import numpy as np

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model_path = "best_new.pt"
video_path = os.path.join(UPLOAD_FOLDER, "input_short.mp4")
output_video_path = os.path.join(OUTPUT_FOLDER, "output.mp4")
temp_dir = os.path.join(OUTPUT_FOLDER, "temp_frames")

fps_extract = 3

model = YOLO(model_path)

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps / fps_extract)

frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % frame_interval == 0:
        frame_path = os.path.join(temp_dir, f"frame_{saved_count:05d}.jpg")
        cv2.imwrite(frame_path, frame)
        saved_count += 1
    frame_count += 1

cap.release()
print(f" Extracted {saved_count} frames into {temp_dir}")

processed_dir = os.path.join(temp_dir, "processed")
os.makedirs(processed_dir, exist_ok=True)

for filename in sorted(os.listdir(temp_dir)):
    if not filename.endswith(".jpg"):
        continue
    frame_path = os.path.join(temp_dir, filename)
    results = model(frame_path)
    if results[0].masks is not None:
    # polygons for each detection
       for i, poly in enumerate(results[0].masks.xy):
        polygon = np.array(poly, dtype=np.int32)  # (N,2) points
        area = cv2.contourArea(polygon)
        frame_yolo = results[0].plot()   # YOLO's drawn image

        cv2.putText(frame_yolo, "Custom text", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        print(f"Polygon {i+1} → Area: {area:.2f} pixels²")
    else:
        print("No polygons detected")
    
    cv2.imwrite(os.path.join(processed_dir, filename), frame_yolo)

print(f" Processed frames saved into {processed_dir}")

first_frame = cv2.imread(os.path.join(processed_dir, sorted(os.listdir(processed_dir))[0]))
height, width, _ = first_frame.shape

out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps_extract, (width, height))

for filename in sorted(os.listdir(processed_dir)):
    frame_path = os.path.join(processed_dir, filename)
    frame = cv2.imread(frame_path)
    out.write(frame)

out.release()
print(f" Output video saved as {output_video_path}")
