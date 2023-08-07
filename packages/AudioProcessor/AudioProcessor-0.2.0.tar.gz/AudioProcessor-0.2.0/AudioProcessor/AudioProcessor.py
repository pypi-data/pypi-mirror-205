import os
import logging
import tempfile
import wave
from typing import List, Tuple, Union

import pyaudio
import pydub
import pydub.effects
import speech_recognition as sr
import webrtcvad
from gtts import gTTS


class AudioProcessor:
    def __init__(
        self,
        frame_duration_ms: int = 30,
        sample_rate: int = 16000,
        chunk_size: int = 1024,
        vad_mode: int = 2,
        log_level: int = logging.WARNING,
    ):
        """Initialize the AudioProcessor class with the given parameters."""
        if not isinstance(frame_duration_ms, int):
            raise TypeError("frame_duration_ms must be an integer")
        if frame_duration_ms < 0:
            raise ValueError("frame_duration_ms cannot be negative")
        self.frame_duration_ms = frame_duration_ms

        if not isinstance(sample_rate, int):
            raise TypeError("sample_rate must be an integer")
        if sample_rate < 0:
            raise ValueError("sample_rate cannot be negative")
        self.sample_rate = sample_rate

        if not isinstance(chunk_size, int):
            raise TypeError("chunk_size must be an integer")
        if chunk_size < 0:
            raise ValueError("chunk_size cannot be negative")
        self.chunk_size = chunk_size

        if not isinstance(vad_mode, int):
            raise TypeError("vad_mode must be an integer")
        if vad_mode < 0 or vad_mode > 3:
            raise ValueError("vad_mode must be an integer between 0 and 3")
        self.vad_mode = vad_mode

        if not isinstance(log_level, int):
            raise TypeError("log_level must be an integer")
        if log_level < 0 or log_level > 50:
            raise ValueError("log_level must be an integer between 0 and 50")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"))
        self.logger.addHandler(handler)

        self.recognizer = sr.Recognizer()
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(self.vad_mode)

        # Initialize audio interface using a context manager to ensure proper cleanup
        with pyaudio.PyAudio() as audio_interface:
            self.audio_interface = audio_interface

    def __enter__(self):
        """Initialize the audio interface and return the AudioProcessor instance."""
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the audio stream and terminate the audio interface upon exiting the context."""
        if self.audio_stream is not None:
            self.audio_stream.close()
        self.audio_interface.terminate()

    def record_audio(self, output_file_path: str) -> bool:
        """Record audio from the microphone and save it to a .wav file."""
        if not output_file_path.lower().endswith(".wav"):
            self.logger.error("Output file path must have a .wav extension")
            return False

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_file = f.name

        try:
            with sr.Microphone() as source:
                self.logger.info("Please speak now...")
                audio = self.recognizer.listen(source)

            self._save_audio_to_file(audio, temp_file)

            with wave.open(temp_file, "rb") as source_wave, \
                    wave.open(output_file_path, "wb") as output_wave:
                output_wave.setparams(source_wave.getparams())
                output_wave.writeframes(
                    source_wave.readframes(source_wave.getnframes()))

            self.logger.info(f"Saved audio file: {output_file_path}")

            os.remove(temp_file)

        except sr.RequestError as e:
            self.logger.error(
                f"Failed to record audio due to a request error: {e}", exc_info=True)
            return False
        except sr.WaitTimeoutError:
            self.logger.error(
                "No audio detected within the timeout period", exc_info=True)
            return False
        except ValueError as e:
            self.logger.error(
                f"Failed to record audio due to an invalid argument: {str(e)}", exc_info=True)
            return False
        except Exception as e:
            self.logger.error(
                f"Failed to record audio due to an unexpected error: {e}", exc_info=True)
            return False
        return True

    def _save_audio_to_file(self, audio, file_path):
        """Save a SpeechRecognition AudioData object to a file."""
        with open(file_path, 'wb') as f:
            f.write(audio.get_wav_data())

    def audio_to_text(self, audio_file_path: str, preprocess: bool = False, show_all: bool = False) -> Union[str, List[str]]:
        """Convert the given audio file to text using Google Speech Recognition."""
        if not os.path.exists(audio_file_path):
            self.logger.error(f"Error: File not found ({audio_file_path})")
            return ""

        file_ext = os.path.splitext(audio_file_path)[-1].lower()

        if file_ext not in [".wav", ".mp3", ".flac"]:
            self.logger.error(
                f"Error: unsupported audio file format ({file_ext})")
            return ""

        with sr.AudioFile(audio_file_path) as source:
            audio_text = self.recognizer.listen(source)

        return self._process_audio_text(audio_text, preprocess=preprocess, show_all=show_all)

    def _process_audio_text(self, audio_text, preprocess: bool = False, show_all: bool = False) -> Union[str, List[str]]:
        """Preprocess the audio data and send it to Google Speech Recognition."""
        if preprocess:
            frames = self._generate_frames(
                audio_text.get_raw_data(), self.sample_rate, self.frame_duration_ms)
            segments = self._collect_voiced_segments(
                frames, self.vad, self.sample_rate)
            audio_text = b"".join(segments)

        try:
            response = self.recognizer.recognize_google(
                audio_text, show_all=show_all)
            return self._parse_recognition_response(response, show_all)
        except (sr.UnknownValueError, sr.RequestError) as e:
            self.logger.error(f"Error: {e}")
            return ""

    def _parse_recognition_response(self, response, show_all: bool) -> Union[str, List[str]]:
        """Parse the response from Google Speech Recognition and return the result as text."""
        if show_all:
            text = [alternative['transcript']
                    for alternative in response['alternative']]
        else:
            text = response

        return text

    def text_to_audio(
        self,
        text: str,
        audio_file_path: str,
        lang: str = 'en',
        volume: float = 1.0,
        sample_rate: int = 44100,
        bit_depth: int = 16,
    ) -> None:
        """Convert the given text to an audio file using Google Text-to-Speech."""
        if not audio_file_path.lower().endswith(".wav"):
            self.logger.error("Output file path must have a .wav extension")
            return

        try:
            audio = gTTS(text=text, lang=lang, slow=False)
            audio = audio.get_audio_data(
                rate=sample_rate, width=bit_depth // 8, normalize=False)
            with wave.open(audio_file_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(bit_depth // 8)
                wf.setframerate(sample_rate)
                wf.writeframes(audio)

            self.logger.info(f"Saved audio file: {audio_file_path}")

        except Exception as e:
            self.logger.error(f"Error: {e}")
            return

        self._play_audio_file(audio_file_path,
                              volume=volume)

    def play_audio_file(self, audio_file_path: str, volume: float = 1.0) -> None:
        """Play a given audio file, adjusting the volume as necessary."""
        if not os.path.exists(audio_file_path):
            self.logger.error(f"Error: File not found ({audio_file_path})")
            return

        audio_segment = pydub.AudioSegment.from_wav(audio_file_path)
        audio_segment = audio_segment + (20 * (volume - 1))

        playback_temp = tempfile.NamedTemporaryFile(suffix=".wav")
        audio_segment.export(playback_temp.name, format="wav")
        playback_temp.seek(0)

        with wave.open(playback_temp.name, "rb") as audio_file:
            audio_stream = self.audio_interface.open(
                format=self.audio_interface.get_format_from_width(
                    audio_file.getsampwidth()),
                channels=audio_file.getnchannels(),
                rate=audio_file.getframerate(),
                output=True
            )

            audio_data = audio_file.readframes(self.chunk_size)
            while audio_data:
                audio_stream.write(audio_data)
                audio_data = audio_file.readframes(self.chunk_size)

            audio_stream.stop_stream()
            audio_stream.close()

        playback_temp.close()

    def _generate_frames(self, audio_data: bytes, sample_rate: int, frame_duration_ms: int) -> List[bytes]:
        """Generate frames from raw audio data for Voice Activity Detection (VAD)."""
        n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
        offset = 0
        timestamp = 0.0
        duration = float(n) / sample_rate / 2.0
        frames = []
        while offset + n < len(audio_data):
            frames.append(audio_data[offset:offset + n])
            timestamp += duration
            offset += n
        return frames

    def _collect_voiced_segments(self, frames: List[bytes], vad: webrtcvad.Vad, sample_rate: int) -> List[bytes]:
        """Collect voiced segments from the frames using Voice Activity Detection (VAD)."""
        voiced_segments = []
        for frame in frames:
            if vad.is_speech(frame, sample_rate):
                voiced_segments.append(frame)
        return voiced_segments
