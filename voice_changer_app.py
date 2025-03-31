import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import librosa
import os

# ===== アプリタイトル =====
st.title("🎙️ 声変わりマシン 🎶")

# ===== UI設定 =====
duration = st.slider("録音時間（秒）", 1, 10, 3)
pitch_shift = st.slider("ピッチ変更（半音）", -12, 12, 5)
echo_strength = st.slider("エコー強度", 0.0, 1.0, 0.5)
speed_rate = st.slider("速度倍率", 0.5, 2.0, 1.0)
filename = st.text_input("保存ファイル名", "my_voice.wav")

pitch_on = st.checkbox("ピッチ変更", True)
echo_on = st.checkbox("エコー追加", True)
speed_on = st.checkbox("速度変更", False)

if st.button("🎤 録音＆加工＆再生＆保存"):
    st.write(f"🔴 {duration}秒録音中...")
    samplerate = 44100
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    st.write("✅ 録音終了")

    audio_1d = audio.flatten()
    processed = audio_1d.copy()

    if echo_on:
        delay = int(0.3 * samplerate)
        echo = np.zeros(len(processed) + delay)
        echo[:len(processed)] += processed
        echo[delay:] += processed * echo_strength
        processed = echo

    if pitch_on:
        processed = librosa.effects.pitch_shift(processed, sr=samplerate, n_steps=pitch_shift)

    if speed_on:
        processed = librosa.effects.time_stretch(processed, rate=speed_rate)

    # 再生
    st.write("🔊 加工後の音声を再生...")
    sd.play(processed, samplerate)
    sd.wait()

    # 保存
    processed_int16 = np.int16(processed * 32767)
    wav.write(filename, samplerate, processed_int16)
    st.write(f"💾 保存しました → {filename}")

# ===== 保存ファイル一覧 =====
st.write("---")
st.write("📂 保存された音声ファイル")
wav_files = [f for f in os.listdir() if f.endswith(".wav")]

if wav_files:
    selected_file = st.selectbox("再生するファイルを選択", wav_files)
    if st.button("▶️ 選んだ音声を再生"):
        rate, data = wav.read(selected_file)
        st.write(f"▶️ {selected_file} を再生中...")
        sd.play(data, rate)
        sd.wait()
else:
    st.write("（まだ保存されたファイルはありません）")