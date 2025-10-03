import cv2
import os
import shutil
from ultralytics import YOLO

model_path = "best _new.pt"
video_path = r"D:\projects\ct-hackathon-2025\backend\uploads\input.mp4"
output_video_path = r"D:\projects\ct-hackathon-2025\backend\outputs\output.mp4"
temp_dir = r"D:\projects\ct-hackathon-2025\backend\temp_frames"

fps_extract = 6

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
print(f"✅ Extracted {saved_count} frames into {temp_dir}")

processed_dir = os.path.join(temp_dir, "processed")
os.makedirs(processed_dir, exist_ok=True)

for i, filename in enumerate(sorted(os.listdir(temp_dir))):
    if not filename.endswith(".jpg"):
        continue
    frame_path = os.path.join(temp_dir, filename)
    results = model(frame_path)
    results[0].save(filename=os.path.join(processed_dir, filename))

print(f"✅ Processed frames saved into {processed_dir}")

first_frame = cv2.imread(os.path.join(processed_dir, sorted(os.listdir(processed_dir))[0]))
height, width, _ = first_frame.shape

out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps_extract, (width, height))

for filename in sorted(os.listdir(processed_dir)):
    frame_path = os.path.join(processed_dir, filename)
    frame = cv2.imread(frame_path)
    out.write(frame)

out.release()
print(f"🎥 Output video saved as {output_video_path}")
