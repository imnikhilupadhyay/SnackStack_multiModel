
from __future__ import annotations

import argparse
from snackstack.logger import setup_logger
from uuid import uuid4
import sys
from snackstack.voice.recorder import VoiceRecorder
from snackstack.voice.speaker import VoiceSpeaker
from snackstack.graph import main_graph
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command

logger = setup_logger("main")

class SnackStack:
    def __init__(self, voice: str="nova", enable_voice: bool=False):
        self.enable_voice = enable_voice
        self.thread_id = uuid4().hex

        if self.enable_voice:
            self.recorder = VoiceRecorder()
            self.speaker = VoiceSpeaker(voice=voice, speed=1.1)
            pass
        else:
            self.recorder = None
            self.speaker = None

        logger.info("Assistant ready  (voice=%s)", enable_voice)

    def query(self, text: str, input_fn=None) -> str:
        if input_fn is None:
            input_fn = lambda prompt: input(f"\nAgent ask: {prompt}\n You: ").strip()

        config = {"configurable": {"thread_id": self.thread_id}}

        logger.info("query: %s", text)

        result = main_graph.invoke(
            {
                "messages": [HumanMessage(content=text)], "user_query": text
            },
            config=config
        )

        while "__interrupt__" in result and result["__interrupt__"]:
            question = result["__interrupt__"][0].value
            logger.info("HITL interrupt: %r", question)

            if self.enable_voice and self.speaker and self.recorder:
                self.speaker.speak(question)
                _, user_answer = self.recorder.record_transcribe_and_save()
                if not user_answer:
                    user_answer = "I don't have that information"
            else:
                user_answer = input_fn(question)

            logger.info("HITL resume: user_answer=%r", user_answer)
            result = main_graph.invoke(Command(resume=user_answer), config=config)

        answer = result.get("final_answer", "")
        if not answer:
            answer = "Sorry, I wasn't able to process that. Could you try rephrasing?"
        return answer
    
    def text_loop(self) -> None:
        """Chat bot interaction loop"""

        print("\n SnackStack Assistant  (type 'quit' to exit)\n")

        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_input or user_input.lower() in ("quit", "exit", "bye"):
                print("Goodbye!")
                break
            answer = self.query(user_input)
            print(f"\nAssistant: {answer}\n")

    def voice_loop(self, max_turns: int = 10) -> None:
        
        if not self.recorder or not self.speaker:
            logger.error("Voice components are not initialised")
            return

        welcome_text = "Hello! I'm your SnackStack assistant. How can I help you today?"
        self.speaker.speak(welcome_text)

        for turn in range(1, max_turns+1):
            logger.info("--- voice turn %d / %d ---", turn, max_turns)
            _, transcript = self.recorder.record_transcribe_and_save()

            if not transcript:
                self.speaker.speak("I didn't catch that. Could you repeat?")
                continue
            
            if any(word in transcript.lower().strip() for word in [
                "goodbye",
                "bye",
                "quit",
                "exit"
            ]):
                self.speaker.speak("Goodbye! Have a great day.")
                break
            
            if any(word in transcript.lower().strip() for word in [
                "thank you",
                "thanks",
                "thanks a lot",
            ]):
                self.speaker.speak("Your welcome, Can I help you with anything else.")
                continue

            transcript += "\n Keep the response very, very short."
            print(f"\nYou: {transcript}")
            answer = self.query(transcript)
            print(f"Assistant: {answer}\n")
            self.speaker.speak(answer)




def main() -> None:
    parser = argparse.ArgumentParser(description="SnackStack Multi-Agent Voice System")
    parser.add_argument("--voice", action="store_true", help="Use microphone input + TTS output")
    parser.add_argument("--query", type=str, help="Run a single text query and exit")
    args = parser.parse_args()

    assistant = SnackStack(enable_voice=args.voice)

    if args.query:
        print(assistant.query(args.query))
    elif args.voice:
        assistant.voice_loop()
    else:
        assistant.text_loop()


if __name__ == "__main__":
    main()