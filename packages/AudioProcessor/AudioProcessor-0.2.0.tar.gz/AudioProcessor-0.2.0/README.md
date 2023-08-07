AudioProcessor
==============

AudioProcessor is a Python library that provides a simple interface to perform various audio processing tasks such as recording, voice-to-text conversion, text-to-voice conversion, and audio playback.

Installation
------------

To use AudioProcessor, make sure you have the following packages installed:

*   pyaudio
*   pydub
*   pydub.effects
*   speech\_recognition
*   webrtcvad
*   gtts

You can install these packages using pip:

`pip install pyaudio pydub speechrecognition webrtcvad gtts`

Usage
-----

To use AudioProcessor, simply import the `AudioProcessor` class and create an instance:

`from audio_processor import AudioProcessor  processor = AudioProcessor()`

### Recording audio

To record audio, use the `record_audio` method:

`processor.record_audio("output_file.wav")`

This method records audio from the microphone and saves it to a .wav file.

### Voice-to-text conversion

To convert an audio file to text, use the `audio_to_text` method:

`text = processor.audio_to_text("input_file.wav")`

### Text-to-voice conversion

To convert text to an audio file, use the `text_to_audio` method:

`processor.text_to_audio("Hello world!", "output_file.wav")`

### Audio playback

To play an audio file, use the `play_audio_file` method:

`processor.play_audio_file("input_file.wav")`

Class Parameters
----------------

The `AudioProcessor` class can be initialized with the following parameters:

*   `frame_duration_ms`: (int) Frame duration in milliseconds for Voice Activity Detection (default: 30)
*   `sample_rate`: (int) Sample rate of the audio in Hz (default: 16000)
*   `chunk_size`: (int) Chunk size for audio playback (default: 1024)
*   `vad_mode`: (int) Voice Activity Detection mode, an integer between 0 and 3 (default: 2)
*   `log_level`: (int) Logging level, an integer between 0 and 50 (default: logging.WARNING)

License
-------

This project is licensed under the MIT License.