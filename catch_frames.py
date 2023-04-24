import cv2
import os
import shutil

current_dir = os.getcwd()
image_path = os.path.join(current_dir, "images")

if os.path.exists(image_path):
    shutil.rmtree(image_path)
os.mkdir(image_path)

capture = cv2.VideoCapture("InstantNGP.mp4")

# Input: 30 fps video
frame_no = 0

while (capture.isOpened()):
    ret, frame = capture.read()

    if frame_no % 15 == 0:
        target = str(os.path.join(image_path, f"{frame_no}.jpg"))
        cv2.imwrite(target, frame)

    frame_no += 1

    # Only take first 60s of the video
    if frame_no > 30 * 25:
        break

capture.release()
print("done")