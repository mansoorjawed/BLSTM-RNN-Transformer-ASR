import os
import csv
from scipy.io import wavfile
import numpy as np

def framing(signal, frameDuration, sampleRate):
    frameLen = int(frameDuration * sampleRate)
    frames = []
    for start in range(0, len(signal), frameLen):
        frame = signal[start:start + frameLen]
        if len(frame) == frameLen:
            frames.append(frame)
    return np.array(frames)

def calculateZcr(frames):
    zcr = np.zeros(frames.shape[0])
    for i, frame in enumerate(frames):
        # Count the zero crossings
        zcr[i] = np.sum(np.abs(np.diff(np.sign(frame)))) / 2
    return zcr

# Read WAV file
# TODO: no hardcoding singular file paths

audio_data_path = "D:/University/Data/audio_data.tsv"
file_names = []
with open(audio_data_path, newline='', encoding='utf-8') as file:
    # Create a CSV reader object, specifying the delimiter as a tab character
    reader = csv.reader(file, delimiter='\t')
    next(reader)

    for row in reader:
        file_names.append(row[0])

print(len(file_names))

output_dir = "D:/University/Data/zcr"
count = 0

for file in file_names:
    inputAudioFile = file
    sampleRate, signal = wavfile.read(inputAudioFile)
    # Normalize the signal
    signal = signal / np.abs(np.max(signal)).astype(float)

    # Do framing
    frameDuration = 0.025  # 20ms per frame
    frames = framing(signal, frameDuration, sampleRate)

    # Calculate ZCR for all frames
    zcrValues = calculateZcr(frames)

    # Calculate rate and normalize
    zcrRate = zcrValues / frames.shape[1]
    zcrRateNormalized = zcrRate / np.max(zcrRate)

    # Create a ZCR waveform for plotting
    zcrWave = np.repeat(zcrRateNormalized, frames.shape[1])

    # # Plot the ZCR with Signal
    # t = np.linspace(0, len(signal) / sampleRate, len(signal))
    # t1 = np.linspace(0, len(zcrWave) / sampleRate, len(zcrWave))
    #
    # plt.figure(figsize=(8, 4))
    # plt.plot(t, signal, label='Signal')
    # plt.plot(t1, zcrWave, 'r', linewidth=2, label='ZCR')
    # plt.xlabel('Time [s]')
    # plt.ylabel('Amplitude / ZCR')
    # plt.legend()
    # plt.title('Signal and its ZCR')
    # plt.show()

    # Silence Removal
    silenceThreshold = 0.04

    nonSilenceIndices = zcrRateNormalized > silenceThreshold
    framesWithoutSilence = frames[nonSilenceIndices]

    # Reconstruct signal from frames without silence
    dataReconstructed = np.hstack(framesWithoutSilence)
    # calculate time in seconds properly
    tReconstructed = np.arange(len(dataReconstructed)) / sampleRate

    #
    # plt.figure(figsize=(8, 4))
    # plt.plot(t, signal, label='Original Signal')
    # plt.plot(tReconstructed, dataReconstructed, 'g', label='Signal without Silence')
    # plt.xlabel('Time [s]')
    # plt.ylabel('Amplitude')
    # plt.legend()
    # plt.title('Speech without Silence')
    # plt.show()

    # Save the modified signal to a WAV file
    # TODO: no hard coding singular file paths
    output_file_path = os.path.join(output_dir + "/" + os.path.basename(file))
    wavfile.write(output_file_path, sampleRate, dataReconstructed.astype(np.float32))


    # print(f"Original Audio \n")
    # display(Audio(inputAudioFile))
    # print(f"After removing based on ZCR \n")
    # display(Audio(outputAudioFilePath))
    # print(f"Modified audio saved to {outputAudioFilePath}")

    count += 1
    if count % 1000 == 0:
        print(f"last file done: {output_file_path}\nTotal count: {count}")

print(f"last file{output_file_path}\nfinal count: {count}")