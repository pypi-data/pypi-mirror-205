from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="AudioProcessor",
    version="0.1.4",
    packages=["AudioProcessor"],
    install_requires=[
        "speechrecognition",
        "gtts",
        "pyaudio",
        "wave",
        "webrtcvad",
        "pydub",
    ],
    author="Andrew Horvath",
    author_email="drewfhorvath@gmail.com",
    description="A Python package for recording, transcribing, and converting audio",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/TheWordSmith123/Audio-Processor",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11"
    ],
)
