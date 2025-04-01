import streamlit as st
import numpy as np
import librosa
import soundfile as sf

st.title("🎙️ クラウド版 声変わりマシン")

# ===== ファイルアップロード =====
uploaded_file = st.file_uploader("音声ファイルをアップロードしてください", type=["wav", "mp3"])

if uploaded_file is not None:
    # 音声読み込み
    y, sr = librosa.load(uploaded_file, sr=None)
    st.audio(uploaded_file)

    # 加工設定
    pitch_shift = st.slider("ピッチ変更 (半音)", -12, 12, 5)
    echo_strength = st.slider("エコー強度", 0.0, 1.0, 0.5)
    speed_rate = st.slider("速度倍率", 0.5, 2.0, 1.0)

    # 加工ボタン
    if st.button("加工して再生"):
        # ピッチ変更
        y_shift = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_shift)

        # エコー追加
        delay = int(0.3 * sr)
        echo = np.zeros(len(y_shift) + delay)
        echo[:len(y_shift)] += y_shift
        echo[delay:] += y_shift * echo_strength

        # 速度変更
        processed = librosa.effects.time_stretch(echo, speed_rate)

        # 再生
        st.audio(sf.write("processed.wav", processed, sr), format="audio/wav")

        st.success("✅ 加工完了しました！")