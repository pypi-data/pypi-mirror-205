import speech_recognition as sr
from gtts import gTTS
import pyaudio
import wave
import webrtcvad
import os
import tempfile
import pydub

class AudioProcessor:
    def __init__(self, frame_duration_ms=30, sample_rate=16000, chunk_size=1024, vad_mode=2):
        self.frame_duration_ms = frame_duration_ms
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.vad_mode = vad_mode
        self.recognizer = sr.Recognizer()
        self.audio_interface = pyaudio.PyAudio()
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(vad_mode)

    def record_audio(self, output_file_path):
        """Record audio from the microphone and save it to a .wav file."""
        # Check if the output_file_path has a .wav extension
        if not output_file_path.lower().endswith('.wav'):
            print("Error: Output file path must have a .wav extension")
            return
        temp_file = tempfile.mktemp(".wav")
        with sr.Microphone() as source:
            print("Please speak now...")
            audio = self.recognizer.listen(source)

        self._save_audio_to_file(audio, temp_file)

        # Convert the temporary file to the desired output format
        with wave.open(temp_file, 'rb') as source_wave, \
             wave.open(output_file_path, 'wb') as output_wave:
            output_wave.setparams(source_wave.getparams())
            output_wave.writeframes(source_wave.readframes(source_wave.getnframes()))

        print(f"Saved audio file: {output_file_path}")
        os.remove(temp_file)

    def _save_audio_to_file(self, audio, file_path):
        """Save the audio data to a .wav file."""
        with open(file_path, "wb") as f:
            f.write(audio.get_wav_data())

    def audio_to_text(self, audio_file_path, **kwargs):
        """Transcribe an audio file."""
        if not os.path.exists(audio_file_path):
            print(f"Error: File not found ({audio_file_path})")
            return ""
        file_ext = audio_file_path.split(".")[-1].lower()

        if file_ext not in ["wav", "mp3", "flac"]:
            print("Error: unsupported audio file format ({})".format(file_ext))
            return ""

        with sr.AudioFile(audio_file_path) as source:
            audio_text = self.recognizer.listen(source)

        return self._process_audio_text(audio_text, **kwargs)

    def _process_audio_text(self, audio_text, **kwargs):
        """Process the audio_text and return the transcribed text."""
        preprocess = kwargs.get("preprocess", False)
        if preprocess:
            frames = self._generate_frames(audio_text.get_raw_data(), self.sample_rate, self.frame_duration_ms)
            segments = self._collect_voiced_segments(frames, self.vad, self.sample_rate)
            audio_text = b"".join(segments)

        show_all = kwargs.get("show_all", False)
        try:
            response = self.recognizer.recognize_google(audio_text, show_all=show_all)
            return self._parse_recognition_response(response, show_all)
        except (sr.UnknownValueError, sr.RequestError) as e:
            print("Error: {}".format(e))
            return ""

    def _parse_recognition_response(self, response, show_all):
        """Parse the response from the speech recognizer."""
        if show_all:
            text = [alternative['transcript'] for alternative in response['alternative']]
            confidence = [alternative['confidence'] for alternative in response['alternative']]
            print("Recognized text: {}".format(text))
            print("Confidence scores: {}".format(confidence))
        else:
            text = response
            print("Recognized text: {}".format(text))

        return text

    def _process_recognized_audio(self, audio):
        """Process the recognized audio and return the transcribed text."""
        try:
            text = self.recognizer.recognize_google(audio)
            print("Recognized text: {}".format(text))
        except sr.UnknownValueError as e:
            print("Error: UnknownValueError - {}".format(e))
            text = ""
        except sr.RequestError as e:
            print("Error: RequestError - {}".format(e))
            text = ""

        return text

    def text_to_audio(self, text, audio_file_path, lang='en', volume=1.0, sample_rate=44100, bit_depth=16):
        """Convert text to an audio file and play it."""
        # Check if the output_file_path has a .wav extension
        if not audio_file_path.lower().endswith('.wav'):
            print("Error: Output file path must have a .wav extension")
            return
        try:
            audio = gTTS(text=text, lang=lang, slow=False)
            audio = audio.get_audio_data(rate=sample_rate, 
                                        # multiply by 2 since the bit depth is in bytes and there are 2 bytes per sample for WAV files
                                        width=bit_depth*2,  
                                        normalize=False)
            with wave.open(audio_file_path, 'wb') as wf:
                wf.setnchannels(1)  # mono audio
                wf.setsampwidth(bit_depth)  # bit depth in bytes
                wf.setframerate(sample_rate)
                wf.writeframes(audio)
            print(f"Saved audio file: {audio_file_path}")
        except Exception as e:
            print(f"Error: {e}")
            return

        self._play_audio_file(audio_file_path, volume, normalize=True)

    def _play_audio_file(self, audio_file_path, volume=1.0, normalize=False):
        """Play the audio file with the specified volume and optional normalization."""
        if not os.path.exists(audio_file_path):
            print(f"Error: File not found ({audio_file_path})")
            return
        try:
            with wave.open(audio_file_path, 'rb') as wf:
                stream = self.audio_interface.open(format=self.audio_interface.get_format_from_width(wf.getsampwidth()),
                                                    channels=wf.getnchannels(),
                                                    rate=wf.getframerate(),
                                                    output=True)
                # Read and play the audio file in chunks
                data = wf.readframes(self.chunk_size)
                while data:
                    adjusted_data = bytearray()
                    for i in range(0, len(data), 2):
                        audio_sample = int.from_bytes(data[i:i + 2], byteorder='little')
                        audio_sample = int(audio_sample * volume)
                        audio_sample = min(max(audio_sample, -32768), 32767)
                        adjusted_data += audio_sample.to_bytes(2, byteorder='little')
                    if normalize:
                        audio_segment = pydub.AudioSegment(data=adjusted_data, sample_width=wf.getsampwidth(),
                                                        frame_rate=wf.getframerate(), channels=wf.getnchannels())
                        normalized_audio_segment = pydub.effects.normalize(audio_segment)
                        normalized_data = normalized_audio_segment.raw_data
                        stream.write(normalized_data)
                    else:
                        stream.write(bytes(adjusted_data))  # Convert bytearray to bytes
                    data = wf.readframes(self.chunk_size)

                # Close the stream
                stream.stop_stream()
                stream.close()
        except Exception as e:
            print(f"Error: {e}")


    def _generate_frames(self, audio, sample_rate, frame_duration_ms):
        frame_duration_s = frame_duration_ms / 1000
        frame_size = int(frame_duration_s * sample_rate)
        offset = 0
        while offset < len(audio):
            yield audio[offset:offset + frame_size]
            offset += frame_size


    def _collect_voiced_segments(self, frames, vad, sample_rate, ratio=2):
        voiced_frames = [frame for frame in frames if vad.is_speech(frame.tobytes(), sample_rate)]

        segments = []
        start = 0
        while start < len(voiced_frames):
            end = start + 1
            while end < len(voiced_frames) and end - start < ratio:
                segment = b"".join(voiced_frames[start:end])
                segments.append(segment)
                end += 1
            start = end

        return segments

# def main():
#     audio_processor = AudioProcessor()

#     # Test 1: Record audio from the microphone and save it to a .wav file
#     print("\nTest 1: Record audio from the microphone and save it to a .wav file")
#     output_audio_file_path = "recorded_audio.wav"
#     audio_processor.record_audio(output_audio_file_path)

#     # Test 2: Transcribe an audio file
#     print("\nTest 2: Transcribe an audio file")
#     audio_file_path = "Audio.wav"
#     transcribed_text = audio_processor.audio_to_text(audio_file_path)
#     print("Transcribed text: {}".format(transcribed_text))

#     # Test 3: Text to audio and play it
#     print("\nTest 3: Text to audio and play it")
#     text = "This is a test for text to audio conversion."
#     output_audio_file_path = "output_audio.wav"
#     audio_processor.text_to_audio(text, output_audio_file_path)

# if __name__ == "__main__":
#     main()
