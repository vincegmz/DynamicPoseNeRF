import cv2
import numpy as np
import json
import pdb
import math
import os
import shutil
import re


def draw_lines(img, data, name):
    # Create an empty image with dimensions (500, 500) and 3 channels

    # Define the vertex dictionary
    vertex_list = [
        (22, 23), (22, 11), (11, 24), (24, 10), (10, 9), (9, 8),# left leg
        (19, 20), (19, 14), (14, 21), (14, 13), (13, 12), (12, 8), # right leg
        (8, 1), # body
        (4, 3), (3, 2), (2, 1), # left arm
        (7, 6), (6, 5), (5, 1), # right arm
        (1, 0) # recalculated head
    ]

    # Define the colors for the lines and markers
    marker_color = (0, 255, 0)
    alpha = 0.3
    overlay = img.copy()

    # Iterate over the vertices in the dictionary
    for vertex in vertex_list:
        # print("vertex", vertex)

        line_color = tuple(np.random.randint(20, 240, 3).tolist())

        try:
            x1, y1, _ = data["part_candidates"][0][str(vertex[0])]
            x2, y2, _ = data["part_candidates"][0][str(vertex[1])]

        except:
            #  print("-------- continue --------")
             continue

        # pdb.set_trace()

        # Draw a line between the vertex and the neighbor on the image
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), line_color, thickness=15, lineType=cv2.LINE_AA)
        result = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)


    for vertex in vertex_list:
        # print("vertex", vertex)
        try:
            x1, y1, _ = data["part_candidates"][0][str(vertex[0])]
            x2, y2, _ = data["part_candidates"][0][str(vertex[1])]

        except:
            #  print("-------- continue --------")
             continue

        cv2.circle(result, (int(x1), int(y1)), radius=10, color=marker_color, thickness=-1)
        cv2.circle(result, (int(x2), int(y2)), radius=10, color=marker_color, thickness=-1)


    # Display the image
    # cv2.imshow("Result", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite("./MyDrawingOnImage/" + name + ".jpg", result)


if __name__ == '__main__':

    point_path = "./estimate_head/"
    img_path = "./images/"
    
    # ============== Display the .json ==============
    # with open(os.path.join(folder_path, "modified_120_keypoints.json"), "r") as fhand:
    #     data = fhand.read()
    # data = data.replace(", \"", ", \n\"")
    # ============== Display the .json ==============

    # ============== test ==============
    # with open(os.path.join(folder_path, "modified_120_keypoints.json")) as fhand:
    #     data = json.load(fhand)
    #     draw_lines(data, "modified_120_keypoints")
    # ============== test ==============

    output_path = "./MyDrawingOnImage/"
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)
    
    pattern = r"\d+"
    for filename in os.listdir(point_path):
        img_name = re.findall(pattern, filename)[0] + ".jpg"
        # pdb.set_trace()
        img = cv2.imread("./images/" + img_name)
        
        
        if filename.endswith(".json"):
            name, _ = os.path.splitext(filename)

            with open(os.path.join(point_path, filename)) as fhand:
                data = json.load(fhand)
            
            draw_lines(img, data, name)

    # print(data)