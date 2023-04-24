import os
import random
import shutil
import json

# Set the paths to your image folder and the output folder for the train, test, and validation data.
# Replace these with your own paths.
image_folder_path = '/home/minzhe_guo/Documents/GitHub/D-NeRF/out'
output_folder_path = '/home/minzhe_guo/Documents/GitHub/D-NeRF/data/dance'

# Set the percentage split for the train, test, and validation data.
train_percent = 0.8
test_percent = 0.1
val_percent = 0.1

# Create the output folder and subfolders.
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

train_folder_path = os.path.join(output_folder_path, "train")
if not os.path.exists(train_folder_path):
    os.makedirs(train_folder_path)

test_folder_path = os.path.join(output_folder_path, "test")
if not os.path.exists(test_folder_path):
    os.makedirs(test_folder_path)

val_folder_path = os.path.join(output_folder_path, "validation")
if not os.path.exists(val_folder_path):
    os.makedirs(val_folder_path)

transform_path = os.path.join(output_folder_path, 'transforms.json')
transform_train = json.load(open(os.path.join(output_folder_path, 'transforms_train.json'),'r'))
transform_test = json.load(open(os.path.join(output_folder_path, 'transforms_test.json'),'r'))
transform_val = json.load(open(os.path.join(output_folder_path, 'transforms_val.json'),'r'))
transform_in = json.load(open(transform_path, 'r'))
frames = transform_in['frames']
image_files = []
for frame in frames:
   image_files.append(os.path.join(output_folder_path, frame['file_path'][2:]))
num_images = len(image_files)
num_train = int(num_images * train_percent)
num_test = int(num_images * test_percent)
num_val = num_images - num_train - num_test


# transform_train = transform_in.copy()
# transform_train['frames'] = transform_in['frames'][:num_train]
# for ele in transform_train['frames']:
#     ele['file_path'] = ele['file_path'][:-4].replace('images', 'train')
# with open(os.path.join(output_folder_path, 'transforms_train.json'), 'w') as f:
#     json.dump(transform_train, f,indent=4)

# transform_test = transform_in.copy()
# transform_test['frames'] = transform_in['frames'][num_train:num_train+num_test]
# for ele in transform_test['frames']:
#     ele['file_path'] = ele['file_path'][:-4].replace('images', 'test')
# with open(os.path.join(output_folder_path, 'transforms_test.json'), 'w') as f:
#     json.dump(transform_test, f,indent=4)

# transform_val = transform_in.copy()
# transform_val['frames'] = transform_in['frames'][num_train+num_test:]
# for ele in transform_val['frames']:
#     ele['file_path'] = ele['file_path'][:-4].replace('images', 'val')
# with open(os.path.join(output_folder_path, 'transforms_val.json'), 'w') as f:
#     json.dump(transform_val, f,indent=4)

for ele in transform_train['frames']:
    image_name = ele['file_path'][-4:]+'.png'
    image = os.path.join(image_folder_path,image_name)
    shutil.copy(image, train_folder_path)

for ele in transform_test['frames']:
    image_name = ele['file_path'][-4:]+'.png'
    image = os.path.join(image_folder_path, image_name)
    shutil.copy(image, test_folder_path)

for ele in transform_val['frames']:
    image_name = ele['file_path'][-4:]+'.png'
    image = os.path.join(image_folder_path, image_name)
    shutil.copy(image, val_folder_path)
