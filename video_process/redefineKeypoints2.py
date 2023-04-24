import json
import math
import os

# def getBackHeadPose(keypoints):
#     l, r, l_id, r_id = None, None, -1, -1
#     highest_y, thresh = -1, 0.01
#     lx, ly, lid = 0,0,"16"
#     rx, ry, rid = 0,0,"17"
#     lx, ly, score = keypoints[lid]
#     rx, ry, score = keypoints[rid]
#     new_x = (rx+lx) / 2
#     keypoints[lid] = []
#     keypoints[rid] = [new_x, ry, score]
def point_partition(ptlist):
    bathches = []
    batch_size = 3
    for i in range(0, len(ptlist), batch_size):
        batch = ptlist[i:i+batch_size]
        bathches.append(batch)
    return bathches

def compute_distance(pt1, pt2):
    # Return distance between pt1 and pt2
    x1, y1 = pt1[0], pt1[1]
    x2, y2 = pt2[0], pt2[1]
    
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def nearest_point(target, ptlist):
    # Given a target coordinate, return the nearest point in ptlist
    result_x, result_y = 0, 0
    min_distance = float('inf')
    
    for point in ptlist:
        point = maximum_confidence(point)
        distance = compute_distance(target, point)
        if distance < min_distance:
            min_distance = distance
            result_x = point[0]
            result_y = point[1]

    return result_x, result_y

def find_middle_point(pt1, pt2):
    # Given two points, find middle point between them
    result_x = (pt1[0] + pt2[0]) / 2
    result_y = (pt1[1] + pt2[1]) / 2
    return result_x, result_y

def maximum_confidence(ptlist):
    # Given a list, return the max confidence point
    if not ptlist:
        return []
    batches = point_partition(ptlist)
    sorted_list = sorted(batches, key=lambda x: -x[2])

    return sorted_list[0]
    
    

def getBackHeadPose(file):
    # Given a json file, find the head points as 0, and delete 15-18 points
    keypoints = file["part_candidates"][0]
    exist_0 = len(keypoints["0"]) != 0
    exist_15 = len(keypoints["15"]) != 15
    exist_16 = len(keypoints["16"]) != 16
    exist_17 = len(keypoints["17"]) != 17
    exist_18 = len(keypoints["18"]) != 18
    point_list = [keypoints["0"], keypoints["15"], keypoints["16"], keypoints["17"], keypoints["18"]]
    head_point = [0, 0, 0]
    target_point = keypoints["1"]
    
    # All points exist, camera at front
    if exist_0 and exist_15 and exist_16 and exist_17 and exist_18:
        print("all exists =======================================")
        head_point = maximum_confidence(keypoints["0"])
    # Only one of 17 or 18 exists -> find nearest one
    elif not exist_17 or not exist_18:
        print("17 or 18 exists ======================================")
        x, y = nearest_point(maximum_confidence(target_point), point_list)
        head_point = [x, y, 1]
    # Both 17 and 18 exist -> find middle point
    elif exist_17 and exist_18:
        print("both 17 and 18 exists ======================================")
        x, y = find_middle_point(maximum_confidence(keypoints["17"]), maximum_confidence(keypoints["18"]))
        head_point = [x, y, 1]
        
    print("origin head: ", keypoints["0"])
    print("estimate head: ", head_point)
    print("\n")
    
    # Set head point
    keypoints["0"] = head_point
    
    # Delete 15-18
    keypoints["15"] = []
    keypoints["16"] = []
    keypoints["17"] = []
    keypoints["18"] = []
    
    for key, point in keypoints.items():
        keypoints[key] = maximum_confidence(point)
    
    
    return file

path_to_folder = "./json"
path_to_save = "./estimate_head"

for filename in os.listdir(path_to_folder):
    print(filename)
    if filename.endswith(".json"):
        with open(os.path.join(path_to_folder, filename), "r") as f:
            data = json.load(f)
            processed_data = getBackHeadPose(data)
        with open(os.path.join(path_to_save, "modified_" + filename), "w") as f:
            json.dump(processed_data, f)