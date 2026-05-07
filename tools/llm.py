import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings

load_dotenv()  # 从项目根目录加载 .env

def get_llm():
  # 初始化llm模型
  llm = ChatOpenAI(
    model = os.getenv("QWEN3_MODEL"),
    api_key = os.getenv("QWEN3_API_KEY"),
    base_url = os.getenv("QWEN3_API_URL"),
    temperature = float(os.getenv("QWEN3_MODEL_TEMPERATURE", "0")),
    timeout = int(os.getenv("QWEN3_TIMEOUT", "30")),
    max_retries = int(os.getenv("QWEN3_MAX_RETRIES", "3")),
  )

  return llm

def get_embeding():
  # 初始化embeding模型
  embeddings = DashScopeEmbeddings(
    model = os.getenv("QWEN3_EMBEDING_MODEL"),
    dashscope_api_key = os.getenv("QWEN3_API_KEY"),
  )

  return embeddings
