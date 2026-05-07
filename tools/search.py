import os
from dotenv import load_dotenv

from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()  # 从项目根目录加载 .env

_tavily_client = None

# 初始化tavily客户端
def get_tavily_client():
  global _tavily_client

  if _tavily_client is None:
   _tavily_client = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

  return _tavily_client

# 定义给agent使用的网络检索方法
@tool("search_network", description = "根据问题利用工具进行网络检索。")
def search_network(query, max_results = 2):

    try:
      client = get_tavily_client()
      res = client.search(query, max_results = max_results)
      
      # 提取搜索结果
      results = res.get('results', [])

      if not results:
        return "调用了search_network, 但什么也没查到。"
      
      # 整理搜索结果
      formatted = []
      for i, resp in enumerate(results, 1):
        title = resp.get("title", "无标题")
        url = resp.get("url", "")
        content = resp.get("content", "").strip()

        if len(content) > 100:
          content = content[:100] + "..."

        formatted.append(f"{i}. {title}\n 链接: {url}\n 摘要: {content}")
    
      result_text = "\n\n".join(formatted)

      return result_text

    except Exception as e:
      err_msg = f"调用search_network发生错误: {str(e)}"
      return err_msg
