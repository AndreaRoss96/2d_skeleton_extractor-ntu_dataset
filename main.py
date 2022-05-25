import os
from os.path import exists, join, basename, splitext
from botocore.exceptions import ClientError
import boto3
import ovh
import time
from utils import is_already_processed, create_tmp_file, ovh_get_file

"""
- bucket : bucket containing the data (on ovh cloud)
- processed_files : a list of video already processed (skeleton already extracted)

|
 - skeleton/video_class/video_name
|
 - already_processed.txt
|
 - main.py
 - utils.py
 - requirements.py
"""



s3 = boto3.resource('s3',
                      region_name='sbg',
                      endpoint_url='https://s3.sbg.perf.cloud.ovh.net',
                      aws_access_key_id='d72fc2728afc44a4a5fddc33dea2b8f5',
                      aws_secret_access_key='7fd2414f45b54704952b58b75a665569',)
bucket = s3.Bucket('fused-data')

processed_files = "already_processed.txt"

with open(processed_files) as file:
    processed_lines = file.readlines()
    processed_lines = [line.rstrip() for line in processed_lines]



for c, bucket_elem in enumerate(bucket.objects.all()):
    print(f"video {c+1} of 20236 ===================================>") # I think, all_objs has no len()
    video_name = bucket_elem.key 
    video_class = video_name.split(".")[0].split("_")[0][-3:]

    if any(x in video_name for x in ["/", "txt", "A114"]): # if the file's not a video or is repeated in the dataset --> jump
        print(f'jump {video_name}')
        continue
    
    if is_already_processed(processed_lines, video_name): # if the file already processed --> jump
        print(f'jump {video_name} - already processed')
        continue

    stream_f = ovh_get_file(bucket, video_name)

    temp_video = "tmp.avi"
    create_tmp_file(stream_f, temp_video)

    # Skeleton extraction
    print(f"processing {video_name}")
    class_folder = "skeleton/" + video_class + "/"
    skeleton_out = class_folder + video_name.split(".")[0][:-4]

    print(f"creating {class_folder}")
    if not os.path.isdir(class_folder) :
        os.system(f"mkdir {class_folder}")
    print(f"creating {skeleton_out}")
    os.system(f"mkdir {skeleton_out}")
    os.system(f"cd openpose && ./build/examples/openpose/openpose.bin --video {temp_video} --write_json {skeleton_out}  --display 0 --render_pose 0")
    
    with open(processed_files, "a") as p_file :
        p_file.write('\n'+ video_name)