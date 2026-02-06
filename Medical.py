import speech_recognition as sr
from pydub import AudioSegment
import math
import os

class ChunkedAudioTranscriber:
    def __init__(self, audio_path, chunk_length=30):
        self.original_path = audio_path
        self.chunk_length = chunk_length  # seconds
        self.wav_path = self._ensure_wav_format(audio_path)
        self.recognizer = sr.Recognizer()

    def _ensure_wav_format(self, path):
        if path.lower().endswith('.wav'):
            return path
        audio = AudioSegment.from_file(path)
        wav_path = "converted_audio.wav"
        audio.export(wav_path, format="wav")
        return wav_path

    def _get_audio_duration(self):
        audio = AudioSegment.from_wav(self.wav_path)
        return len(audio) / 1000  # milliseconds to seconds

    def transcribe(self):
        full_transcript = ""
        duration = self._get_audio_duration()
        total_chunks = math.ceil(duration / self.chunk_length)

        with sr.AudioFile(self.wav_path) as source:
            for i in range(total_chunks):
                start = i * self.chunk_length
                print(f"Processing chunk {i + 1}/{total_chunks} (from {start}s)...")
                try:
                    audio_data = self.recognizer.record(source, duration=self.chunk_length)
                    text = self.recognizer.recognize_google(audio_data)
                    full_transcript += f"{text}\n"
                except sr.UnknownValueError:
                    full_transcript += "[Unintelligible]\n"
                except sr.RequestError as e:
                    full_transcript += f"[Request failed: {e}]\n"
                    break

        print("\nFull Transcription:\n" + full_transcript)
        return full_transcript

if __name__ == "__main__":
    file_path = r"C:\Users\sweth\Downloads\ESL-Cardio-sample.wav" # Your uploaded file
    if os.path.exists(file_path):
        transcriber = ChunkedAudioTranscriber(file_path)
        transcriber.transcribe()
    else:
        print(f"File not found: {file_path}")
