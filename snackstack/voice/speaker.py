
from __future__ import annotations

from snackstack.logger import setup_logger
import os
import sounddevice as sd
import soundfile as sf
from uuid import uuid4
from snackstack.config import openai_client, voice_tts_model

logger = setup_logger("Voice Speaker")

class VoiceSpeaker:
    def __init__(self, voice: str="nova", speed: float=1.0) -> None:
        self.voice = voice
        self.speed = speed
        self._out_dir = os.getcwd()

    def synthesise(self, text: str) -> str:
        out_path = os.path.join(self._out_dir, f"tts_{uuid4().hex[:8]}.mp3")

        try:
            with openai_client.audio.speech.with_streaming_response.create(
                model=voice_tts_model,
                voice=self.voice,
                input=text,
                speed=self.speed
            ) as response:
                response.stream_to_file(out_path)

            return out_path
        except Exception:
            logger.exception("TTS synthesis failed !!")
            return ""
        
    def play(self, audio_file: str):
        try:
            data, sr = sf.read(audio_file)
            sd.play(data, sr)
            sd.wait()
        except Exception:
            logger.exception("Audio playback failed !!")

    def speak(self, text: str, auto_play: bool=True) -> str:
        logger.info("Agent says: %s", text[:120])
        path = self.synthesise(text)
        
        if auto_play and path:
            self.play(path)
        
        return path
    