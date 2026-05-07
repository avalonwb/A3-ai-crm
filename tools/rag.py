from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.tools import tool

from tools.llm import get_embeding
from tools.load_docs import load_documents

# 本地法律条文文档路径
LAW_DOC_PATH = Path(__file__).parent.parent / "data" / "中华人民共和国知识产权法.txt"

# Chroma本地目录
CHROMA_DIR = Path(__file__).resolve().parent.parent / "db" / "chroma_db"

# 可选，多专题时分集合用
COLLECTION_NAME = "ip_law"

_vectorstore = None

def get_vectorstore():
  global _vectorstore

  if _vectorstore is None:
    # 初始化Chroma
    embeddings = get_embeding()
    _vectorstore = Chroma(
      persist_directory = str(CHROMA_DIR),
      embedding_function = embeddings,
      collection_name = COLLECTION_NAME,
    )

  return _vectorstore

# 加载并分割文档
def split_docs(doc_path):
  # 加载文档
  documents = load_documents(doc_path = doc_path)

  # 分割文档
  text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n", "，", "。", " "]
  )

  chunks = text_spliter.split_documents(documents)
  return chunks

# 文档内容向量化并存入数据库
def add_vector():
    # 得到分割后的文档内容
    chunks = split_docs(LAW_DOC_PATH)

    # 存入Chroma数据库
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

# 定义给agent使用的RAG检索方法
@tool("search_rag", description = "根据问题利用RAG进行检索。")
def search_rag(query, top = 3):
  # 把问题转换成向量
  embeddings = get_embeding()
  query_vector = embeddings.embed_query(query)
  
  # 用问题向量与RAG库里的向量进行比对，挑选出最接近的答案
  vectorstore = get_vectorstore()
  docs = vectorstore.similarity_search_by_vector(query_vector, k = top)

  if not docs:
    return "知识库中未找到与问题相关的片段。"

  return "\n\n---\n\n".join(d.page_content for d in docs)
