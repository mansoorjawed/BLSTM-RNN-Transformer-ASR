import csv
import os
import shutil

# File path to the validated.tsv for all the vaidated files in CV
VALIDATED_FILE_PATH = "D:/University/cv-corpus/en/validated.tsv"
TARGET_ACCENT_PAK = "pak"
TARGET_ACCENT_IND = "ind"

# TODO: new validated file that includes only the names of the relevant
#  pakistani and indian files and info related to them

with open(VALIDATED_FILE_PATH, newline='', encoding='utf-8') as file:
    # Create a CSV reader object, specifying the delimiter as a tab character
    reader = csv.reader(file, delimiter='\t')

    # Used to store names of all the clips that are indian or pakistani
    clip_file_names = set();
    count = 0
    # Iterate through each row in the TSV file
    for row in reader:

        # Check if the value in the 'accents' column matches the target value
        # for the accents. The 'accents' column is the 8th column (index 7)
        if (TARGET_ACCENT_PAK.lower() in row[7].lower()) or \
                (TARGET_ACCENT_IND.lower() in row[7].lower()):
            # Add the clip name to array (Col 2, index 1) if match is successful
            clip_file_names.add(row[1].lower())
            count = count + 1
    print(f"{count} number of files in Validated tsv")


print("\n\n")
# Define the directory path for all clips
source_dir_path = "D:/University/cv-corpus/en/clips/"
# Get a list of all files in the directory
files_in_dir = os.listdir(source_dir_path)

# path to store data in, if doesn't exist then make one
destDirPath = "D:/University/cv-corpus/en/ind_pak_clips/"
if not os.path.exists(destDirPath):
    os.makedirs(destDirPath)

count = 0
# Find and copy clips that are pakistani or Indian
for clipName in files_in_dir:
    if (clipName.lower() in clip_file_names):
        # file path of the source directory copy clips from
        VALIDATED_FILE_PATH = os.path.join(source_dir_path, clipName)
        # directory to paste file into
        destPath = os.path.join(destDirPath, clipName)

        # when files are found, increase count
        count = count + 1
        #Copy file to a new folder: ind_pak_data
        shutil.copy2(VALIDATED_FILE_PATH, destPath)

    if (count % 1000 == 0):
        print(f"Number of files done: {count}")

print(f"Copied {count} number of files")

