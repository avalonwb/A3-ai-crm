import os
from typing import Any, Dict, Optional

from bs4 import SoupStrainer
from langchain_community.document_loaders import (
  Docx2txtLoader,
  PyMuPDFLoader,
  TextLoader,
  WebBaseLoader,
)

# 把「网页分支里 url_class 字典的值」统一成 BeautifulSoup SoupStrainer 能接受的 class_ 形态。
def _normalize_css_classes(classes: Any) -> tuple:
  if isinstance(classes, str):
    return (classes,)
  return tuple(classes)


# 加载不同类型的文档
def load_documents(
  doc_path: str,
  doc_type: str = 'txt',
  url_class: Optional[Dict[str, Any]] = None,
):
  """
  按类型加载文档: web / pdf / txt / docx。
  - web: url_class 为 {url: css_class 或 [class1, class2]}；值为空则整页抓取。
  - 其余类型需传入存在的 doc_path。
  """
  if not doc_path:
    raise FileNotFoundError(f"未提供文档保存的路径：{doc_path}")

  if not os.path.exists(doc_path):
    raise FileNotFoundError(f"文档不存在: {doc_path}")

  try:
    if doc_type == "web":
      if not url_class:
        raise ValueError("doc_type 为 web 时必须提供 url_class")
      documents = []
      for url, classes in url_class.items():
        if classes:
          class_tuple = _normalize_css_classes(classes)
          loader = WebBaseLoader(
            web_paths=[url],
            bs_kwargs={"parse_only": SoupStrainer(class_=class_tuple)},
          )
        else:
          loader = WebBaseLoader(web_paths=[url])
        documents.extend(loader.load())
        return documents

    if doc_type == "pdf":
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
