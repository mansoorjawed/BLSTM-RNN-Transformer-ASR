import librosa
import soundfile as sf

# Load audio file
src_file_patth = "D:/University/Data/sample/wav/common_voice_en_220779.wav"
audio, sr = librosa.load(src_file_patth, sr=None)

# Trim silence
trimmed_audio, _ = librosa.effects.trim(audio, top_db=30)
                                            # top_db is the threshold for silence

# Save the trimmed audio
dest_file_path = "D:/University/Data/sample/trimmed/common_voice_en_220779.wav"
sf.write(dest_file_path, trimmed_audio, sr)
