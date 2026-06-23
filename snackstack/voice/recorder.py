
from __future__ import annotations

from snackstack.logger import setup_logger
import os
import sounddevice as sd
import soundfile as sf
import io
import numpy as np
import time
import tempfile
from uuid import uuid4
from typing import Tuple
from snackstack.config import openai_client, voice_stt_model

logger = setup_logger("voice recorder")

class VoiceRecorder:
    def __init__(self, duration: int=5, countdown: bool=True, sample_rate: int=16000) -> None:
        self.duration=duration
        self.countdown=countdown
        self.sample_rate=sample_rate

    def recorder(self) -> np.ndarray:

        if self.countdown:
            for i in range(3, 0, -1):
                logger.info("Recording starts in %ds", i)
                time.sleep(1)
        
        logger.info("Recording for %d s — speak now!", self.duration)

        audio = sd.rec(
            int(self.duration*self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32"
        )

        sd.wait()
        logger.info("Recording complete")
        return audio
    
    def transcribe(self, audio, language: str="en") -> str:
        buf = io.BytesIO()

        sf.write(buf, audio, self.sample_rate, format="WAV")
        buf.seek(0)
        buf.name = "recording.wav"

        try:
            result = openai_client.audio.transcriptions.create(
                model=voice_stt_model, file=buf, language=language
            )
            logger.debug("Transcription: %r", result.text)
            return result.text
        except Exception as e:
            logger.exception("Whisper transcription failed")
            return ""
        
    def record_transcribe_and_save(self) -> Tuple[str, str]:

        audio = self.recorder()
        wav_path = os.path.join(tempfile.gettempdir(), f"rec_{uuid4().hex[:8]}.wav")
        # sf.write(wav_path, audio, samplerate=self.sample_rate)
        text = self.transcribe(audio)
        return wav_path, text
    