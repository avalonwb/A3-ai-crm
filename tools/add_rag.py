from tools.rag import get_vectorstore, split_docs

# 手动向向量数据库中添加文档
def append_to_rag(doc_path, doc_type: str = "txt"):

  try:
    # 读取并分割文档
    chunks = split_docs(doc_path = doc_path, doc_type = doc_type)

    vectorstore = get_vectorstore()
    ids = vectorstore.add_documents(chunks)

    # 返回添加的文档条目数
    return len(ids)
  except Exception as e:
    err_msg = f"向量数据库添加文档时发生错误: {str(e)}"
    print(err_msg)
    return 0
  