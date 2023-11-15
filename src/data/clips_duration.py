import os
import csv

# path to the file with duration of all the audio clips
DURATION_FILE = "D:/University/cv-corpus/en/clip_durations.tsv"
durationDict = {}

with open(DURATION_FILE, newline='', encoding='utf-8') as file:

    # Create a CSV reader object, specifying the delimiter as a tab character
    reader = csv.reader(file, delimiter='\t')
    next(reader)

    # Used to store names of all the clips that are indian or pakistani
    clip_file_names = set();

    # Iterate through each row in the TSV file to get all the names
    for row in reader:
        durationDict[row[0]] = int(row[1])

# path to the source with all the audio clips.
sourceDirPath = "D:/University/cv-corpus/en/ind_pak_clips/"
# Get a list of all files in the directory
filesInDir = os.listdir(sourceDirPath)

count = 0
msTotalTime = 0
for file in filesInDir:
    msTotalTime = msTotalTime + durationDict[file]
    count += 1

sTotalTime = msTotalTime / 1000
mTotalTime = sTotalTime / 60
hTotalTime = mTotalTime / 60
print(f"""
Number of files: {count}
ms: {msTotalTime:.0f}
sec: {sTotalTime:.0f}
mins: {mTotalTime:.0f}
hrs: {hTotalTime:.0f} 
""")
