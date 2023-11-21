import os
import librosa
import h5py
from concurrent.futures import ProcessPoolExecutor


# Function to load an audio file and extract MFCCs
def process_audio(file_path):
    try:
        signal, sr = librosa.load(file_path, sr=None)
        mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13)
        return mfccs
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to process a batch of files and save in an HDF5 file
def process_batch(batch, batch_index, audio_dir, target_dir):
    batch_data = {}
    for filename in batch:
        file_path = os.path.join(audio_dir, filename)
        mfccs = process_audio(file_path)
        if mfccs is not None:
            batch_data[filename] = mfccs

    # Save the batch data to an HDF5 file
    hdf5_filename = f"mfcc_batch_{batch_index}.hdf5"
    with h5py.File(os.path.join(target_dir, hdf5_filename), 'w') as hdf5_file:
        for filename, mfccs in batch_data.items():
            hdf5_file.create_dataset(name=filename, data=mfccs,
                                     compression='gzip')
    print(f"Batch {batch_index} saved with {len(batch_data)} files.")

def main():

    # Directory paths
    audio_dir = "D:/University/Data/trimmed"
    target_dir = "D:/University/Data/mfcc/mfcc"
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]

    # Number of files in each batch
    batch_size = 1000

    # Process the audio files in parallel and save in batches
    with ProcessPoolExecutor() as executor:
        for batch_index, i in enumerate(range(0, len(audio_files), batch_size)):
            batch = audio_files[i:i + batch_size]
            executor.submit(process_batch, batch, batch_index, audio_dir,
                            target_dir)


if __name__ == '__main__':
    main()