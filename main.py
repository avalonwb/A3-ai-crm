from fastapi import Body, FastAPI
# 导入 CORS 中间件
from fastapi.middleware.cors import CORSMiddleware

from agent import agent as chat_agent
from classify import chain_classify
from router import chain_router
from models import AddRagRequest, AddRagResponse, ChatRequest, ChatResponse
from tools.add_rag import append_to_rag

import uuid

app = FastAPI(title = "ai_crm")

# 添加 CORS 中间件
app.add_middleware(
  CORSMiddleware,
  allow_origins = ["127.0.0.1"],  # 测试用，只允许本地请求
  allow_credentials = True,
  allow_methods = ["*"],  # 允许所有 HTTP 方法，包括 OPTIONS
  allow_headers = ["*"],  # 允许所有请求头
)

# 入口请求
@app.post("/question")
async def chat(chat_req: ChatRequest = Body()):
  print(f"chat_req.query: {chat_req.query}")
  # Body已完成参数校验, 生成一个随机的 session_id
  session_id = str(uuid.uuid4())

  # 意图识别和路由导航链
  chain = chain_classify | chain_router | chat_agent
  res = chain.invoke(
    {"input": chat_req.query}, 
    config={"configurable": {"thread_id": session_id}}
  )

  # 提取结构化响应数据
  structured = res.get('structured_response')
  printout(structured)

  # 返回Json数据
  return ChatResponse(
    session_id = session_id,
    answer = structured.answer if structured else "",
    tool_used = structured.tool_used if structured else None,
    legal_refer = structured.legal_refer if structured else None,
    search_results = structured.search_results if structured else None,
    sql_result = structured.sql_result if structured else None
  )

# 向量数据库更新接口，文档一定要放在该项目根目录下的data文件夹里
@app.post("/addDocManual")
async def chat(req_body: AddRagRequest = Body()):
  # Body已完成参数校验, 调用添加文档接口
  doc_count = append_to_rag(req_body.doc_path, req_body.doc_type)

  # 根据文档数量直接决定状态
  status = "OK" if doc_count > 0 else "Failed"
  
  # 返回Json数据
  return AddRagResponse(
    status = status,
    length = str(doc_count)
  )

# 打印结果函数
def printout(structured):
  if structured: 
    print(f"Agent回复: {structured.answer}")
    if structured.tool_used:
     print(f"Agent使用的工具: {structured.tool_used}")
    if structured.legal_refer:
     print(f"Agent查询的法律条文: {structured.legal_refer}")
    if structured.search_results:
     print(f"Agent搜索网络的结果: {structured.search_results}")
    if structured.sql_result:
     print(f"Agent查询数据库结果: {structured.sql_result}")

if __name__ == "__main__":
  # 本地测试代码
  chain = chain_classify | chain_router | chat_agent

  while True:
    question = input("请输出你的问题: ")

    if not question:
      continue
    elif question == "1":
      # 测试问题1： 测试网络搜索工具调用
      res = chain.invoke({"input": '去网络上搜索一下最新的MacBook Pro的价格是?'}, config={"configurable": {"thread_id": "great-gatsby-lc"}})
      printout(res.get('structured_response'))
      
    elif question == "2":
      # 测试问题2：测试RAG调用
      res = chain.invoke({"input": '知识产权法中定义的作品有哪些？'}, config={"configurable": {"thread_id": "great-gatsby-lc"}})
      printout(res.get('structured_response'))

    elif question == "3":
      # 测试问题3：测试数据库查询调用
      res = chain.invoke({"input": '去数据库中查下Emily Johnson住在哪座城市?'}, config={"configurable": {"thread_id": "great-gatsby-lc"}})
      printout(res.get('structured_response'))

    elif question == "4":
      # 测试问题4：测试普通聊天
      res = chain.invoke({"input": '你好, 你今天心情怎么样？'}, config={"configurable": {"thread_id": "great-gatsby-lc"}})
      printout(res.get('structured_response'))

    elif question == "q":
      # 退出
      print("测试完毕，退出程序...")
      break

    else:
      # 自由输入
      res = chain.invoke({"input": question}, config={"configurable": {"thread_id": "great-gatsby-lc"}})
      printout(res.get('structured_response'))
      