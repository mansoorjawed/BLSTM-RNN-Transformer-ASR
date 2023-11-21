import os
import librosa
import h5py
from concurrent.futures import ProcessPoolExecutor
import numpy as np


# Function to load an audio file and extract MFCCs with CMVN applied for normalization
def process_audio(file_path):
    try:
        signal, sr = librosa.load(file_path, sr=None)
        # mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13)
        mfccs_with_energy, log_energy = mfcc_energy(signal, sr)
        mfccs_normalized = apply_cmvn(mfccs_with_energy)
        mfcc_deltas, mfcc_deltas2, \
        mfcc_energy_deltas, mfcc_energy_deltas2 \
                = delta_and_energy(mfccs_normalized, log_energy)

        combined_features = np.concatenate((mfccs_normalized,
                                           mfcc_deltas,
                                           mfcc_deltas2,
                                           mfcc_energy_deltas,
                                           mfcc_energy_deltas2
                                           ), axis=0
                                           )

        return combined_features
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def mfcc_energy(signal, sr):
    # Compute the Mel-spectrogram (for energy)
    spectrogram = librosa.feature.melspectrogram(y=signal, sr=sr)

    # Compute the log energy
    log_energy = librosa.core.power_to_db(spectrogram, ref=np.max)

    # Calculate MFCCs with the energy feature as the first coefficient
    mfccs = librosa.feature.mfcc(S=librosa.power_to_db(spectrogram), n_mfcc=13)

    return mfccs, log_energy


def delta_and_energy(mfccs, log_energy):
    # calculate first and second order derivatives
    mfcc_deltas = librosa.feature.delta(mfccs)
    mfcc_deltas2 = librosa.feature.delta(mfccs, order=2)

    # Calculate first and second derivatives of energy
    mfcc_energy_deltas = librosa.feature.delta(log_energy)
    mfcc_energy_deltas2 = librosa.feature.delta(log_energy, order=2)

    return mfcc_deltas, mfcc_deltas2, mfcc_energy_deltas, mfcc_energy_deltas2

def apply_cmvn(mfccs):
    """
    Apply CMVN to MFCCs
    :param mfccs: Numpy array of MFCCs where each column is a feature and each row is a frame.
    :return: Normalized MFCCs.
    """
    # Compute mean and std dev for each coefficient across all frames
    means = np.mean(mfccs, axis=0)
    std_devs = np.std(mfccs, axis=0)

    # Apply normalization: (mfcc - mean) / std_dev
    mfccs_normalized = (mfccs - means) / std_devs

    return mfccs_normalized


# Function to process a batch of files and save in an HDF5 file
def process_batch(batch, batch_index, audio_dir, target_dir):
    batch_data = {}
    for filename in batch:
        file_path = os.path.join(audio_dir, filename)
        mfccs_normalized = process_audio(file_path)
        if mfccs_normalized is not None:
            batch_data[filename] = mfccs_normalized

    # Save the batch data to an HDF5 file
    hdf5_filename = f"mfcc_batch_{batch_index}.hdf5"
    with h5py.File(os.path.join(target_dir, hdf5_filename), 'w') as hdf5_file:
        for filename, mfccs_normalized in batch_data.items():
            hdf5_file.create_dataset(name=filename, data=mfccs_normalized,
                                     compression='gzip')
    print(f"Batch {batch_index} saved with {len(batch_data)} files.")


def main():
    # Directory paths
    audio_dir = "D:/University/Data/trimmed"
    target_dir = "D:/University/Data/mfcc/mfcc_cmvn_delta"
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]

    # Number of files in each batch
    batch_size = 1000

    # Process the audio files in parallel and save in batches
    with ProcessPoolExecutor() as executor:
        for batch_index, i in enumerate(range(0, len(audio_files), batch_size)):
            batch = audio_files[i:i + batch_size]
            executor.submit(process_batch, batch, batch_index, audio_dir,
                            target_dir)


# This is the important part to include
if __name__ == '__main__':
    main()