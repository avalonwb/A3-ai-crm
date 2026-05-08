import os
from typing import Optional

import bs4
from langchain_community.document_loaders import (
  Docx2txtLoader,
  PyMuPDFLoader,
  TextLoader,
  WebBaseLoader,
)

# 加载不同类型的文档
def load_documents(
  doc_path: str,
  doc_type: str = 'txt',
  url_class: Optional[tuple[str]] = None,
):
  """
  按类型加载文档: web / pdf / txt / docx。
  - web: url_class 为 (class1, class2)；值为空则整页抓取。
  - 其余类型需传入存在的 doc_path。
  """
  if not doc_path:
    raise FileNotFoundError(f"未提供文档保存的路径：{doc_path}")

  if doc_type != 'web' and not os.path.exists(doc_path):
    raise FileNotFoundError(f"文档不存在: {doc_path}")

  try:
    if doc_type == "web":
      if not url_class:
        raise ValueError("doc_type 为 web 时必须提供 url_class")
      
      loader = WebBaseLoader(
        web_path = (doc_path,),
        # 使用到的解析器
        bs_kwargs = dict(
          # 使用beautifulSoup4解析器
          parse_only = bs4.SoupStrainer(
            # 爬取特定class的内容
            class_ = url_class
          )
        )
      )

    elif doc_type == "pdf":
      loader = PyMuPDFLoader(doc_path)

    elif doc_type == "txt":
      loader = TextLoader(doc_path, encoding="utf-8")

    elif doc_type == "docx":
      loader = Docx2txtLoader(doc_path)

    else:
      raise ValueError(f"不支持的文档格式: {doc_type}")

    return loader.load()

  except Exception as e:
    print(f"RAG加载文档时发生错误: {str(e)}")
    return None

