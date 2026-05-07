import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.tools import tool
from tools.llm import get_llm

load_dotenv()

_sql_agent = None

# 获取SQL代理实例
def get_sql_agent():

  global _sql_agent

  if _sql_agent is None:
    db_path = os.getenv("SQL_AGENT_DB_PATH")

    dir_path = os.path.dirname(db_path)

    # 如果配了数据库路径但实际不存在则创建
    if dir_path and not os.path.exists(dir_path):
      os.makedirs(dir_path, exist_ok = True)

    # 如果数据库不存在则创建
    if not os.path.exists(db_path):
      init_example_db(db_path)

    # 链接数据库
    uri = f"sqlite:///{db_path}"
    print(f"链接数据库: {uri}")
    db = SQLDatabase.from_uri(uri)

    # 获取大模型
    llm = get_llm()

    # 初始化SQL工具包
    toolkit = SQLDatabaseToolkit(db = db, llm = llm)

    # 初始化SQL代理
    _sql_agent = create_sql_agent(
      llm,
      toolkit = toolkit,
      agent_type = "tool-calling",
      verbose = True,
    )

  return _sql_agent

# 查询数据库
def query_sql_agent(question):

  try:
    agent = get_sql_agent()

    result = agent.invoke({"input": question})
    output = result.get("output", str(result))

    return output

  except Exception as e:
    err_msg = f"SQL查询时报错: {str(e)}"
    return err_msg

# 定义工具函数，包裹SQL代理的调用
@tool("sql_agent", description = "根据问题利用SQL代理检索数据库。")
def search_db(query):
  return query_sql_agent(query)


# 生成测试表和测试数据
def init_example_db(db_path):
  import sqlite3
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  # 创建测试表并插入数据
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE,
        city TEXT
    )
  """)

  # 插入测试数据
  test_users = [
    (1, 'John Smith', 28, 'john.smith@example.com', 'Beijing'),
    (2, 'Emily Johnson', 32, 'emily.johnson@example.com', 'Shanghai'),
    (3, 'Michael Brown', 25, 'michael.brown@example.com', 'Guangzhou'),
    (4, 'Sarah Davis', 30, 'sarah.davis@example.com', 'Shenzhen'),
    (5, 'David Wilson', 27, 'david.wilson@example.com', 'Hangzhou'),
    (6, 'Lisa Miller', 35, 'lisa.miller@example.com', 'Chengdu'),
    (7, 'James Taylor', 29, 'james.taylor@example.com', 'Wuhan'),
    (8, 'Jennifer Anderson', 31, 'jennifer.anderson@example.com', 'Hottot')
  ]

  cursor.executemany("""
    INSERT OR REPLACE INTO users (id, name, age, email, city) 
    VALUES (?, ?, ?, ?, ?)
  """, test_users)

  conn.commit()
  conn.close()
