
from dotenv import load_dotenv
import os
from snackstack.logger import setup_logger
import sys
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI

load_dotenv()

logger = setup_logger("config")

chat_model = "gpt-4o"
embedding_model = "text-embedding-3-small"
voice_stt_model = "whisper-1"
voice_tts_model = "tts-1"

openAI_key: str = os.getenv("openAI_key", "")

if not openAI_key or openAI_key.startswith("sk-your"):
    logger.error("Open AI key is missing")
    sys.exit(1)


langchain_llm = ChatOpenAI(api_key=openAI_key, temperature=0.3, model=chat_model)
langchain_embedding = OpenAIEmbeddings(api_key=openAI_key, model=embedding_model)
openai_client = OpenAI(api_key=openAI_key)

logger.info("OpenAI Client initiated !!")