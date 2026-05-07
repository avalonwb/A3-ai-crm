# 定义agent结构化响应数据
from dataclasses import dataclass

from pydantic import BaseModel, field_validator

@dataclass
class ResponseFormat:
  # 回答的内容
  answer: str
  # 本次回复需要使用的工具名称
  tool_used: str | None = None
  # 引用的法律条文
  legal_refer: str | None = None
  # 网络搜索结果
  search_results: str | None = None
  # SQL查询结果
  sql_result: str | None = None

# 聊天请求体
class ChatRequest(BaseModel):
  query: str
  
  @field_validator('query')
  @classmethod
  def validate_query(cls, v):
    # 检查是否为空字符串或None
    if not v:
      raise ValueError('查询内容不能为空')
    # 确保是字符串类型
    if not isinstance(v, str):
      raise ValueError('查询内容必须是字符串类型')
    # 去除首尾空白字符
    return v.strip()

# 聊天响应体
class ChatResponse(BaseModel):
  session_id: str
  answer: str
  tool_used: str | None = None
  legal_refer: str | None = None
  search_results: str | None = None
  sql_result: str | None = None

# 添加向量数据库请求体
class AddRagRequest(BaseModel):
  doc_path: str
  doc_type: str | None = None

  @field_validator('doc_path')
  @classmethod
  def validate_query(cls, v):
    # 检查是否为空字符串或None
    if not v:
      raise ValueError('查询内容不能为空')
    # 确保是字符串类型
    if not isinstance(v, str):
      raise ValueError('查询内容必须是字符串类型')
    # 去除首尾空白字符
    return v.strip()

# 添加向量数据库响应体
class AddRagResponse(BaseModel):
  status: str | None = None
  length: str | None = None
