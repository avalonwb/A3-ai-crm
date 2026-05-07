from langchain_core.output_parsers import JsonOutputParser
from tools.llm import get_llm
from prompts import PROMPTS

llm = get_llm()

# 1. 意图识别的chain
chain_classify = PROMPTS['first_prompt'] | llm | JsonOutputParser()
