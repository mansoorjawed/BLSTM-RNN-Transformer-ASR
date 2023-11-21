import librosa
import soundfile as sf
import os

# Load audio file
src_dir_path = "D:/University/Data/zcr/"
dest_dir_path = "D:/University/Data/trimmed/"
files_in_dir = os.listdir(src_dir_path)

count = 0
for file in files_in_dir:

    src_file_path = os.path.join(src_dir_path + file)
    audio, sr = librosa.load(src_file_path, sr=None)

    # Trim silence where top_db is the threshold for silence
    trimmed_audio, _ = librosa.effects.trim(audio, top_db=30)

    # Save the trimmed audio
    dest_file_path = os.path.join(dest_dir_path + file)
    sf.write(dest_file_path, trimmed_audio, sr)

    # print every 1000 iterations
    count += 1
    if count % 1000 == 0:
        print(f"Last file done: {dest_file_path}"
              f"\nTotal files done so far:{count}")

print(f"Last file done: {dest_file_path}\nTotal files done so far:{count}")
