import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from IPython.display import Audio

def framing(signal, frame_duration, sample_rate):
    """
    This function does the framing for all the audio files

    :param signal: is the raw audio single
    :param frame_duration: the size of the frame
    :param sample_rate: sample rate to calculate frames
    :return: the array with all the frames
    """
    frame_len = int(frame_duration * sample_rate)
    frames = []
    for start in range(0, len(signal), frame_len):
        frame = signal[start:start + frame_len]
        if len(frame) == frame_len:
            frames.append(frame)
    return np.array(frames)

def calculate_zcr(frames):
    """
    Caclaulte the zero crossing rate given the frames

    :param frames: the frames for which to caculate zcr
    :return: calculated zcr of the frame
    """
    zcr = np.zeros(frames.shape[0])
    for i, frame in enumerate(frames):
        # Count the zero crossings
        zcr[i] = np.sum(np.abs(np.diff(np.sign(frame)))) / 2
    return zcr

# Read WAV file
# TODO: no hardcoding singular file paths
src_file_path = "D:/University/Data/sample/wav/common_voice_en_276997.wav"
sample_rate, signal = wavfile.read(src_file_path)
# Normalize the signal
signal = signal / np.abs(np.max(signal)).astype(float)

# Do framing
frame_duration = 0.020  # 20ms per frame
frames = framing(signal, frame_duration, sample_rate)

# Calculate ZCR for all frames
zcr_values = calculate_zcr(frames)

# Calculate rate and normalize
zcr_rate = zcr_values / frames.shape[1]
zcr_rate_normalized = zcr_rate / np.max(zcr_rate)

# Create a ZCR waveform for plotting
zcr_wave = np.repeat(zcr_rate_normalized, frames.shape[1])

# Plot the ZCR with Signal
t = np.linspace(0, len(signal) / sample_rate, len(signal))
t1 = np.linspace(0, len(zcr_wave) / sample_rate, len(zcr_wave))

plt.figure(figsize=(12, 6))
plt.plot(t, signal, label='Signal')
plt.plot(t1, zcr_wave, 'r', linewidth=2, label='ZCR')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude / ZCR')
plt.legend()
plt.title('Signal and its ZCR')
plt.show()

# Silence Removal
silence_threshold = 0.04
non_silence_indices = zcr_rate_normalized > silence_threshold
frames_without_silence = frames[non_silence_indices]

# Reconstruct signal from frames without silence
data_reconstructed = np.hstack(frames_without_silence)

plt.figure(figsize=(12, 6))
plt.plot(signal, label='Original Signal')
plt.plot(data_reconstructed, 'g', label='Signal without Silence')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Speech without Silence')
plt.show()

# Save the modified signal to a WAV file
# TODO: no hard coding singular file paths
output_filename = 'D:/University/Data/sample/zcr/common_voice_en_276997.wav'
wavfile.write(output_filename,
              sample_rate,
              data_reconstructed.astype(np.float32)
              )

print(f"Modified audio saved to {output_filename}")
