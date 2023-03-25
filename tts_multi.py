import tensorflow as tf

import yaml
import numpy as np
import matplotlib.pyplot as plt

import IPython.display as ipd

from tensorflow_tts.inference import AutoConfig
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

tacotron2 = TFAutoModel.from_pretrained(
    "tensorspeech/tts-tacotron2-kss-ko", name="tacotron2")

fastspeech2 = TFAutoModel.from_pretrained(
    "tensorspeech/tts-fastspeech2-kss-ko", name="fastspeech2")

mb_melgan = TFAutoModel.from_pretrained(
    "tensorspeech/tts-mb_melgan-kss-ko", name="mb_melgan")

processor = AutoProcessor.from_pretrained("tensorspeech/tts-tacotron2-kss-ko")


def do_synthesis(input_text, text2mel_model, vocoder_model, text2mel_name, vocoder_name):
    input_ids = processor.text_to_sequence(input_text)

    # text2mel part
    if text2mel_name == "TACOTRON":
        _, mel_outputs, stop_token_prediction, alignment_history = text2mel_model.inference(
            tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
            tf.convert_to_tensor([len(input_ids)], tf.int32),
            tf.convert_to_tensor([0], dtype=tf.int32)
        )
    elif text2mel_name == "FASTSPEECH2":
        mel_before, mel_outputs, duration_outputs, _, _ = text2mel_model.inference(
            tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
            speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
            speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
            f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
            energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        )
    else:
        raise ValueError(
            "Only TACOTRON, FASTSPEECH2 are supported on text2mel_name")

    # vocoder part
    if vocoder_name == "MB-MELGAN":
        audio = vocoder_model.inference(mel_outputs)[0, :, 0]
    else:
        raise ValueError("Only MB_MELGAN are supported on vocoder_name")

    if text2mel_name == "TACOTRON":
        return mel_outputs.numpy(), alignment_history.numpy(), audio.numpy()
    else:
        return mel_outputs.numpy(), audio.numpy()


def visualize_attention(alignment_history):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.set_title(f'Alignment steps')
    im = ax.imshow(
        alignment_history,
        aspect='auto',
        origin='lower',
        interpolation='none')
    fig.colorbar(im, ax=ax)
    xlabel = 'Decoder timestep'
    plt.xlabel(xlabel)
    plt.ylabel('Encoder timestep')
    plt.tight_layout()
    plt.show()
    plt.close()


def visualize_mel_spectrogram(mels):
    mels = tf.reshape(mels, [-1, 80]).numpy()
    fig = plt.figure(figsize=(10, 8))
    ax1 = fig.add_subplot(311)
    ax1.set_title(f'Predicted Mel-after-Spectrogram')
    im = ax1.imshow(np.rot90(mels), aspect='auto', interpolation='none')
    fig.colorbar(mappable=im, shrink=0.65, orientation='horizontal', ax=ax1)
    plt.show()
    plt.close()


input_text = "신은 우리의 수학 문제에는 관심이 없다. 신은 다만 경험적으로 통합할 뿐이다."

# setup window for tacotron2 if you want to try
tacotron2.setup_window(win_front=10, win_back=10)

mels, alignment_history, audios = do_synthesis(
    input_text, tacotron2, mb_melgan, "TACOTRON", "MB-MELGAN")
visualize_attention(alignment_history[0])
visualize_mel_spectrogram(mels[0])
ipd.Audio(audios, rate=22050)

# text_to_speech('<speak><say-as interpret-as=\'currency\' language=\'ko\'>프로세스와 쓰레드\n• 단일쓰레딩(Single threading) 대 멀티쓰레딩(Multi \nthreading)\n– 단일 프로세스 내에 멀티 쓰레드 실행을 지원 가능</say-as>\n5\n <say-as interpret-as=\'currency\' language=\'en-US\'>Before the Lecture…\n▪ What is “data mining”?\n– The process of discovering hidden patterns or knowledge from large data\n– Involves methods from various fields\n• Computer science (esp. databases), statistics, machine learning,</say-as> …\n5\n</speak>', "en_ko.mp3")
# ssml_to_audio('<speak><say-as interpret-as=\'currency\' language=\'ko\'>프로세스와 쓰레드\n• 단일쓰레딩(Single threading) 대 멀티쓰레딩(Multi \nthreading)\n– 단일 프로세스 내에 멀티 쓰레드 실행을 지원 가능</say-as>\n5\n <say-as interpret-as=\'currency\' language=\'en-US\'>Before the Lecture…\n▪ What is “data mining”?\n– The process of discovering hidden patterns or knowledge from large data\n– Involves methods from various fields\n• Computer science (esp. databases), statistics, machine learning,</say-as> …\n5\n</speak>', "en_ko_ssml.mp3")
# ssml_to_audio('< speak > Here are < say-as interpret-as="characters" > SSML < /say-as > samples.I can pause < break time="3s"/>.I can play a sound< audio src="https://www.example.com/MY_MP3_FILE.mp3" >didn\'t get your MP3 audio file < /audio > . I can speak in cardinals. Your number is <say-as interpret-as="cardinal" > 10 < /say-as > .Or I can speak in ordinals. You are < say-as interpret-as="ordinal" > 10 < /say-as > in line.Or I can even speak in digits. The digits for ten are < say-as interpret-as="characters" > 10 < /say-as > .I can also substitute phrases, like the < sub alias="World Wide Web Consortium" > W3C < /sub > .Finally, I can speak a paragraph with two sentences.< p > <s > This is sentence one. < /s > <s > This is sentence two. < /s > </p >< / speak >', "sample.mp3")
