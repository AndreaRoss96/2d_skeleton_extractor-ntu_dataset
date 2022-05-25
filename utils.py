import os
import time

def is_already_processed(processed_lines, video_name):
  # if the video is in processed_files True --> else False
  return video_name in processed_lines


def ovh_get_file(bucket, video_path):
    # taking the file from OVH storage data
    response = bucket.objects.filter(Prefix=video_path)
    # print(list(response))

    ####### reading from s3 bucket #####
    object = bucket.Object(video_path)
    response = object.get()
    file_stream = response['Body']
    #   print("reading as a binary")
    f = file_stream.read()
    return f

def create_tmp_file(stream_file, temp_video_name, timeout = 10):
    # Checks and deletes the output file
    # You cant have a existing file or it will through an error
    if os.path.isfile(temp_video_name):
        os.remove(temp_video_name)
    # opens the file 'output.avi' which is accessible as 'out_file'
    with open(temp_video_name, "wb") as tmp_file:  # open for [w]riting as [b]inary
        tmp_file.write(stream_file)

    attempts = 0
    while attempts < timeout:
        # wait until the file is created
        # Check if the file exists.

        if os.path.isfile(temp_video_name):
            break
        print(f" attempt: {attempts}")
        # Wait 1 second before trying again.
        time.sleep(1)
        attempts += 1