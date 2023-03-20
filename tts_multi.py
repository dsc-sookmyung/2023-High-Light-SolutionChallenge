from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./tts_api_key.json"


def text_to_speech(text, fileName):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        # alternative_language_codes=["en"]
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    # fileName = "./audio_output/sample" + str(i) + "_" + str(j) + ".mp3"
    with open(fileName, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file ' + fileName)


def ssml_to_audio(ssml_text, outfile):
    # Generates SSML text from plaintext.
    #
    # Given a string of SSML text and an output file name, this function
    # calls the Text-to-Speech API. The API returns a synthetic audio
    # version of the text, formatted according to the SSML commands. This
    # function saves the synthetic audio to the designated output file.
    #
    # Args:
    # ssml_text: string of SSML text
    # outfile: string name of file under which to save audio output
    #
    # Returns:
    # nothing

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Selects the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Writes the synthetic audio to the output file.
    with open(outfile, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + outfile)


print("Waiting for operation to complete...")
text_to_speech('<speak><say-as interpret-as=\'currency\' language=\'ko\'>프로세스와 쓰레드\n• 단일쓰레딩(Single threading) 대 멀티쓰레딩(Multi \nthreading)\n– 단일 프로세스 내에 멀티 쓰레드 실행을 지원 가능</say-as>\n5\n <say-as interpret-as=\'currency\' language=\'en-US\'>Before the Lecture…\n▪ What is “data mining”?\n– The process of discovering hidden patterns or knowledge from large data\n– Involves methods from various fields\n• Computer science (esp. databases), statistics, machine learning,</say-as> …\n5\n</speak>', "en_ko.mp3")
ssml_to_audio('<speak><say-as interpret-as=\'currency\' language=\'ko\'>프로세스와 쓰레드\n• 단일쓰레딩(Single threading) 대 멀티쓰레딩(Multi \nthreading)\n– 단일 프로세스 내에 멀티 쓰레드 실행을 지원 가능</say-as>\n5\n <say-as interpret-as=\'currency\' language=\'en-US\'>Before the Lecture…\n▪ What is “data mining”?\n– The process of discovering hidden patterns or knowledge from large data\n– Involves methods from various fields\n• Computer science (esp. databases), statistics, machine learning,</say-as> …\n5\n</speak>', "en_ko_ssml.mp3")
ssml_to_audio('< speak > Here are < say-as interpret-as="characters" > SSML < /say-as > samples.I can pause < break time="3s"/>.I can play a sound< audio src="https://www.example.com/MY_MP3_FILE.mp3" >didn\'t get your MP3 audio file < /audio > . I can speak in cardinals. Your number is <say-as interpret-as="cardinal" > 10 < /say-as > .Or I can speak in ordinals. You are < say-as interpret-as="ordinal" > 10 < /say-as > in line.Or I can even speak in digits. The digits for ten are < say-as interpret-as="characters" > 10 < /say-as > .I can also substitute phrases, like the < sub alias="World Wide Web Consortium" > W3C < /sub > .Finally, I can speak a paragraph with two sentences.< p > <s > This is sentence one. < /s > <s > This is sentence two. < /s > </p >< / speak >', "sample.mp3")
