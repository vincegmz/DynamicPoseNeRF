import cv2
import os
from pathlib import Path
import pdb
import argparse
import numpy as np
import sys


def blurry_score_laplacian(image, threshold=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    return fm > threshold, fm

def blurry_score_frequency(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    mean_magnitude = np.mean(magnitude_spectrum)
    return mean_magnitude

def most_clear_batch_laplacian(frames):
    clearest = frames[0]
    clearest_score = 0
    for frame in frames:
        _, fm = blurry_score_laplacian(frame)
        if fm > clearest_score:
            clearest_score = fm
            clearest = frame
    return clearest

def most_clear_batch_frequency(frames):
    clearest = frames[0]
    clearest_score = 0
    for frame in frames:
        fm = blurry_score_frequency(frame)
        if fm > clearest_score:
            clearest_score = fm
            clearest = frame
    return clearest

parser = argparse.ArgumentParser(description="Process video frames.")
parser.add_argument('video_path', type=str, help="path to video file")
parser.add_argument('output_path', type=str, help="path to output images")
parser.add_argument('num_partitions', type=int, help="number of partitions")
parser.add_argument('blur_detect_method', type=str, help="choose method to detect blur")
args = parser.parse_args()

# pdb.set_trace()
cap = cv2.VideoCapture(args.video_path)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# num_partitions = 360
num_partitions = args.num_partitions
# frames_per_partition = 10
frames_per_partition = int(total_frames / num_partitions)
detect_method = args.blur_detect_method

frame_interval = max(total_frames // (num_partitions * frames_per_partition), 1)
count = 0
for i in range(num_partitions):
    partition_frames = []
    for j in range(frames_per_partition):
        ret, frame = cap.read()
        if not ret:
            break
        partition_frames.append(frame)
    if detect_method == "laplacian":
        selected_frame = most_clear_batch_laplacian(partition_frames)
    elif detect_method == "frequency":
        selected_frame = most_clear_batch_frequency(partition_frames)
    output_img = args.output_path + "/" + str(count) + ".png"
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    cv2.imwrite(output_img, selected_frame)
    count += 1
    print("batch %d finished" % i)