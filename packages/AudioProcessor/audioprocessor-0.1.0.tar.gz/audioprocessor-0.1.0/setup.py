from setuptools import setup, find_packages

setup(
    name="audioprocessor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "speech_recognition",
        "gtts",
        "pyaudio",
        "wave",
        "webrtcvad",
        "pydub",
    ],
    author="Andrew Horvath",
    author_email="drewfhorvath@gmail.com",
    description="A Python package for recording, transcribing, and converting audio",
    url="https://github.com/TheWordSmith123/Audio-Processor",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11"
    ],
)
