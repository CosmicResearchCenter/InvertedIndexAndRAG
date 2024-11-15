# 提取文档的抽象实体
entity_abstract_prompt = """
请详细提取出给定文本中所有实体的英文标签，仅需提供标签名称，不必包含具体实体。
########################################################
注意下面是已经提取过的实体标签，请不要输出下面的实体标签:
{{entity_label_list}}
########################################################
示例文本:
星海市的市长李建国在任职期间与多家企业和非营利组织保持着紧密联系。
示例输出:
Province,Position,Occupation,Person,Enterprise,Organization
########################################################
给定文本:
{{text}}
########################################################
输出:
"""


# 提取文档的具体实体对象
entity_extraction_prompt = """
请根据以下提供的实体标签和文本内容，提取所有未包含在已提取列表中的实体节点，并按照指定的JSON格式输出。
########################################################
输出要求：
1.输出格式为纯JSON文本，不要包含Markdown语法。
2.需要的JSON格式：
[
{"label":"实体标签","attribute":{"key":"value"}}
]
注意：
•不要生成Markdown形式的JSON输出。
•请确保不重复提取已提供的实体节点。
错误输出:
```json
[
{"label":"实体标签","attribute":{"key":"value"}}
]
```
########################################################
示例:
示例实体标签:
People,School,Skill,Hobby
示例文本:
小明出生于2000年一月五日，高中毕业于京海市第一中学，大学毕业于清华大学。他在大学里喜欢上了他们班的小美，但是被他们班另一个同学小王追上了小美。小明喜欢打篮球，摄影。他有许多技能，比如修电脑、会写代码。
########################################################
示例输出:
[
{"label":"People","attribute":{"name":"小明","both":"2022-01-05"}},
{"label":"People","attribute":{"name":"小美"}},
{"label":"People","attribute":{"name":"小王"}},
{"label":"School","attribute":{"name":"清华大学","level":"大学"}},
{"label":"School","attribute":{"name":"京海市第一中学","level":"高中"}},
{"label":"Hobby","attribute":{"name":"打篮球"}},
{"label":"Hobby","attribute":{"name":"摄影"}},
{"label":"Skill","attribute":{"name":"修电脑"}},
{"label":"Skill","attribute":{"name":"写代码"}},
]
########################################################
输入信息：
已提取的实体节点（避免重复提取）：
{{entity_list}}
########################################################
给定实体标签:
{{entity_label_list}}
########################################################
现在是给定文本:
{{text}}
########################################################
输出结果（纯JSON格式）:
"""

# 建立文档中实体对象之间的关系
entity_relation_prompt = """
基于以下提供的实体列表和文本段落，识别并提取实体之间的关系，支持知识图谱的构建。
########################################################
输出要求：
1.输出格式为纯JSON文本，不要包含Markdown语法。
2.需要的JSON格式：正确输出格式:
[
    {"name1":"实体名","entity_label1":"实体标签","relation":"relation","name2":"实体名","entity_label2":"实体标签"}
]
注意：
•不要生成Markdown形式的JSON输出。
•请确保不重复提取已提供的实体节点。
错误输出格式:
```json
[
    {"name1":"实体名","entity_label1":"实体标签","relation":"关系","name2":"实体名","entity_label2":"实体标签"}
]
```
########################################################
示例实体:
[
{"label":"People","attribute":{"name":"小明","both":"2022-01-05"}},
{"label":"People","attribute":{"name":"小美"}},
{"label":"People","attribute":{"name":"小王"}},
{"label":"School","attribute":{"name":"清华大学","level":"大学"}},
{"label":"School","attribute":{"name":"京海市第一中学","level":"高中"}},
{"label":"Hobby","attribute":{"name":"打篮球"}},
{"label":"Hobby","attribute":{"name":"摄影"}},
{"label":"Skill","attribute":{"name":"修电脑"}},
{"label":"Skill","attribute":{"name":"写代码"}},
]
########################################################
示例文本:
小明出生于2000年一月五日，高中毕业于京海市第一中学，大学毕业于清华大学。他在大学里喜欢上了他们班的小美，但是被他们班另一个同学小王追上了小美。小明喜欢打篮球，摄影。他有许多技能，比如修电脑、会写代码。
########################################################
示例输出:
[
    {"name1":"小明","entity_label1":"People","relation":"喜欢","name2":"小美","entity_label2":"People"},
    {"name1":"小明","entity_label1":"People","relation":"同班同学","name2":"小美","entity_label2":"People"},
    {"name1":"小王","entity_label1":"People","relation":"追求","name2":"小美","entity_label2":"People"},
    {"name1":"小明","entity_label1":"People","relation":"喜欢","name2":"打篮球","entity_label2":"Hobby"},
    {"name1":"小明","entity_label1":"People","relation":"喜欢","name2":"摄影","entity_label2":"Hobby"},
    {"name1":"小明","entity_label1":"People","relation":"拥有技能","name2":"修电脑","entity_label2":"Skill"},
    {"name1":"小明","entity_label1":"People","relation":"拥有技能","name2":"写代码","entity_label2":"Skill"},
    {"name1":"小明","entity_label1":"People","relation":"高中毕业","name2":"京海市第一中学","entity_label2":"School"},
    {"name1":"小明","entity_label1":"People","relation":"大学毕业","name2":"清华大学","entity_label2":"School"}
]
########################################################
输入信息：
已提取的实体节点关系（避免重复提取）：
########################################################
{{entity_relation_list}}
########################################################
给定实体:
{{entity_list}}
########################################################
待提取的文本:
{{text}}
########################################################
输出结果（纯JSON格式）:
"""

# from jinja2 import Template

# class PromptTemplate:
#     def __init__(self, template: str,input_variables):
#         self.template = Template(template)
#         self.input_variables = input_variables
#     def render(self, **kwargs) -> str:
#         return self.template.render(**kwargs)

# p = PromptTemplate(entity_relation_prompt,['entity_list','text'])
# print(p.render(entity_label_list="Person,Organization",text="星海市的市长李建国在任职期间与多家企业和非营利组织保持着紧密联系。"))  
# # print(p)