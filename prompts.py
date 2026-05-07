from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

first_template = """不要回答下面用户的问题，只要根据用户的输入内容来判断分类，
一共有[法律咨询，网络搜索，数据库查询，其他]4种类别。
比如：
1.如果用户输入有'网络', '搜索'等字眼，那就归类为网络搜索。
2.如果用户输入有'法', '咨询'等字眼，那就归类为法律咨询。
3.如果用户输入有'查询', '数据库'等字眼，那就归类为数据库查询。
4.如果用户输入内容不属于以上3种, 那就归类为其他。

用户的输入: {input}
最后的输出包含分类的类别和用户输入的内容, 输出格式为json, 其中, 类别的key为type, 用户输入内容的key为
input。
"""

answer_template = """
你的回复必须是结构化的，包含以下字段：
- answer: 回复的主要内容
- tool_used: 需要使用到的工具名称
- legal_refer: 引用的法律条文(如果有)
- search_results: 网络搜索结果的摘要(如果有)
- sql_result: SQL查询结果(如果有)
请根据实际情况填写这些字段。"""

lawyer_template = """
你是一位专业的法律咨询顾问,
你可以使用一个工具: search_rag(用于通过RAG检索获取一些法律条文)
如果从用户的问题中判断出用户想要一些关于法律的信息，比如"计算机软件是否有知识产权"这样带"知识"、"产权"等字眼的、使用search_rag来获取。
"""

search_template = """
你是一位网民,擅长利用网络搜索信息，
你可以使用一个工具: search_network(用于通过网络检索获取一些最新资讯)
如果从用户的问题中判断出用户想要一些最新消息或者关于未来的消息，比如"MacBook的最新型号"这样带"最新"、"目前"等字眼的、使用search_network来获取。
"""

sql_template = """
你是一位数据库工程师,擅长使用SQL查询数据库信息,
你可以使用一个工具: sql_agent(用于通过检索数据库获取信息)
如果从用户的问题中判断出用户想要从数据库查询一些人的信息，比如"张三的邮箱是什么"这样带"姓名"、"城市"、"年龄"、"邮箱"等字眼的、使用sql_agent来获取。
"""

default_template = """
你是一位健谈的网友，由于输入内容无法归类，请简洁直接回答问题，
"""

# 给每个需要加回复格式约束的template加上约束
templates = [lawyer_template, search_template, sql_template, default_template]
for i in range(len(templates)):
  templates[i] = templates[i] + answer_template
else:
 lawyer_template, search_template, sql_template, default_template = templates

# 定义各类型任务的prompt模板
PROMPTS = {
  "first_prompt": ChatPromptTemplate.from_template(first_template),
  "lawyer_prompt": ChatPromptTemplate.from_messages([
    ("system", lawyer_template),
    ("human", "{input}")
  ]),
  "search_prompt": ChatPromptTemplate.from_messages([
    ("system", search_template),
    ("human", "{input}")
  ]),
  "sql_prompt": ChatPromptTemplate.from_messages([
    ("system", sql_template),
    ("human", "{input}")
  ]),
  "default_prompt": ChatPromptTemplate.from_messages([
    ("system", default_template),
    ("human", "{input}")
  ]),
}
