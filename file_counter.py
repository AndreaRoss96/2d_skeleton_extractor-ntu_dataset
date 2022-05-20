import os 

root_path = 'C:\\Users\\Dell\\Desktop\\Leav\\2d_skeleton_extractor\\data_extracted\\final\\'
folders = os.listdir(root_path)
c=0
for folder in folders:
    if os.path.isfile(folder):
        continue
    folder_path = root_path + folder + '\\'

    for subfolder in os.listdir(folder_path):
        c += 1
        with open("already_processed.txt", "a") as text:
            text.write(subfolder + "_rgb.avi" + "\n")

print(c)

