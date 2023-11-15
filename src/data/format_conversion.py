import os
import time
from pydub import AudioSegment
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor


def convert_file(file, src_dir_path, dest_dir_path):
    """
    Helper function that, given an MP3 file, this function
    converts and saves the file in wav format

    :param file: name of the audio file
    :param src_dir_path: path to source directory with all original mp3 files
    :param dest_dir_path: path to destiantion folder for converted files
    """
    if file.endswith(".mp3"):
        output_file_path = os.path.join(dest_dir_path, os.path.splitext(file)[0]
                                        + ".wav")
        audio = AudioSegment.from_file(os.path.join(src_dir_path, file))
        audio.set_frame_rate(16000).export(output_file_path, format="wav")


def make_wav_from_mp3(src_dir_path, dest_dir_path):
    """
    This function converts file from MP3 to wav
    :param src_dir_path: path to source directory with all original mp3 files
    :param dest_dir_path: path to destiantion folder for converted files
    :return: None
    """
    files = os.listdir(src_dir_path)

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    # Using ProcessPoolExecutor to parallelize the task
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(convert_file,
                                   file,
                                   src_dir_path,
                                   dest_dir_path
                                   )
                   for file in files]
        count = 0
        for future in concurrent.futures.as_completed(futures):
            future.result()
            count += 1
            if count % 1000 == 0:
                print(f"count: {count}")

# note start time for calcualting total time to cahnge format
start_time = time.perf_counter()

# path to file that need to be changed
src_dir_path = "D:/University/Data/cv-corpus/en/ind_pak_clips_mp3"
# path of the changed files
dest_dir_path = "D:/University/Data/cv-corpus/en/ind_pak_clips_wav/"

# change from mp3 to wav
make_wav_from_mp3(src_dir_path, dest_dir_path)

# Calculate the elapsed time
end_time = time.perf_counter()
elapsed_time = end_time - start_time

print(f"The code block took {elapsed_time} seconds to run.")
