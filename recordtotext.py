import sounddevice as sd
from scipy.io.wavfile import write
import openai
import os

# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")  # ここにあなたのAPIキーを入力してください

def record_audio(filename, duration, fs=16000):
    print("録音を開始します...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # 録音が完了するまで待機
    write(filename, fs, recording)

def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text']
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    audio_file = "input.wav"
    record_duration = 10  # 録音時間（秒）
    
    # 録音
    record_audio(audio_file, record_duration)
    
    # 文字起こし
    transcription = transcribe_audio(audio_file)
    if transcription:
        print("文字起こし結果:")
        print(transcription)
