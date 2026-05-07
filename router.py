from langchain_core.runnables import RouterRunnable, RunnableLambda

from prompts import PROMPTS

# 动态路由的chain
def route(input):
  print(f"用户问题为：{input['input']}\n识别意图为: <{input['type']}>, 加载对应提示词模板...")

  # 意图识别：根据llm入口的输出来判断属于哪方面的任务
  if '法律咨询' in input['type']:
    return {"key": 'law', "input": input['input']}
  elif '网络搜索' in input['type']:
    return {"key": 'search', "input": input['input']}
  elif '数据库' in input['type']:
    return {"key": 'sql', "input": input['input']}
  else:
    return {"key": 'default', "input": input['input']}

# 路由节点
route_runnable = RunnableLambda(route)

# 创建中间数据转换节点，把router输出的str转成dict
router_transfer = RunnableLambda(lambda input: {"input": input})

# 路由调度节点
router = RouterRunnable(runnables={ # 所有意图类型任务的字典
  "law": router_transfer | PROMPTS['lawyer_prompt'],
  "search": router_transfer | PROMPTS['search_prompt'],
  "sql": router_transfer | PROMPTS['sql_prompt'],
  "default": router_transfer | PROMPTS['default_prompt']
})

chain_router =  route_runnable | router
