from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver
from tools.llm import get_llm
from models import ResponseFormat
from tools.rag import search_rag
from tools.search import search_network
from tools.sql_search import search_db

llm = get_llm()

checkpointer = InMemorySaver()

agent = create_agent(
    model = llm,
    tools = [search_network, search_rag, search_db],
    # 在route按意图分发任务时带在messages里
    # system_prompt = "",
    response_format = ToolStrategy(ResponseFormat),
    checkpointer = checkpointer,
)
