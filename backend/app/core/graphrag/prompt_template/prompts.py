# 提取文档的抽象实体
entity_abstract_prompt = """
提取给定文本中的所有实体的标签，你仅需要给出实体标签的英文名，不需要给出实体.
########################################################
注意下面是已经提取过的实体标签，请不要输出下面的实体标签:
{{entity_lable_list}}
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
请你基于给定的实体标签和文本，提取出每一个实体节点，然后按照给定的输出格式输出
########################################################
输出格式(纯json格式的文本):
[
{"lable":"实体标签","attribute":[{"key":"value"}}
]
 注意，不要是markdown的json输出，我要的是纯文本的json
错误输出:
```json
[
{"lable":"实体标签","attribute":[{"key":"value"}}
]
```
########################################################
下面是已经提取出的实体节点，请不要重复提取:
{{entity_list}}
########################################################
示例:
示例实体标签:
People,School,Skill,Hobby
示例文本:
小明出生于2000年一月五日，高中毕业于京海市第一中学，大学毕业于清华大学。他在大学里喜欢上了他们班的小美，但是被他们班另一个同学小王追上了小美。小明喜欢打篮球，摄影。他有许多技能，比如修电脑、会写代码。
########################################################
示例输出:
[
{"lable":"People","attribute":[{"name":"小明","both":"2022-01-05"}},
{"lable":"People","attribute":[{"name":"小美"}},
{"lable":"People","attribute":[{"name":"小王"}},
{"lable":"School","attribute":[{"name":"清华大学","level":"大学"}},
{"lable":"School","attribute":[{"name":"京海市第一中学","level":"高中"}},
{"lable":"Hobby","attribute":[{"name":"打篮球"}},
{"lable":"Hobby","attribute":[{"name":"摄影"}},
{"lable":"Skill","attribute":[{"name":"修电脑"}},
{"lable":"Skill","attribute":[{"name":"写代码"}},
]
########################################################
给定实体标签:
{{entity_lable_list}}
########################################################
现在是给定文本:
{{text}}
########################################################
输出:
"""

# 建立文档中实体对象之间的关系
entity_relation_prompt = """
请基于给定的实体和文本，提取并构建实体之间的关系，以支持知识图谱的构建。请遵循输出格式输出。
########################################################
输出格式(纯json格式的文本):
正确输出格式:
[
    {"name1":"实体名","entity_lable1":"实体标签","relation":"关系","name2":"实体名","entity_lable2":"实体标签"}
]
错误输出格式:
```json
[
    {"name1":"实体名","entity_lable1":"实体标签","relation":"关系","name2":"实体名","entity_lable2":"实体标签"}
]
```
########################################################
下面是已经提取出的实体节点关系，请不要重复提取:
{{entity_relation_list}}
########################################################
示例实体:
[
{"lable":"People","attribute":[{"name":"小明","both":"2022-01-05"}},
{"lable":"People","attribute":[{"name":"小美"}},
{"lable":"People","attribute":[{"name":"小王"}},
{"lable":"School","attribute":[{"name":"清华大学","level":"大学"}},
{"lable":"School","attribute":[{"name":"京海市第一中学","level":"高中"}},
{"lable":"Hobby","attribute":[{"name":"打篮球"}},
{"lable":"Hobby","attribute":[{"name":"摄影"}},
{"lable":"Skill","attribute":[{"name":"修电脑"}},
{"lable":"Skill","attribute":[{"name":"写代码"}},
]
########################################################
示例文本:
小明出生于2000年一月五日，高中毕业于京海市第一中学，大学毕业于清华大学。他在大学里喜欢上了他们班的小美，但是被他们班另一个同学小王追上了小美。小明喜欢打篮球，摄影。他有许多技能，比如修电脑、会写代码。
########################################################
示例输出:
[
    {"name1":"小明","entity_lable1":"People","relation":"喜欢","name2":"小美","entity_lable2":"People"},
    {"name1":"小明","entity_lable1":"People","relation":"同班同学","name2":"小美","entity_lable2":"People"},
    {"name1":"小王","entity_lable1":"People","relation":"追求","name2":"小美","entity_lable2":"People"},
    {"name1":"小明","entity_lable1":"People","relation":"喜欢","name2":"打篮球","entity_lable2":"Hobby"},
    {"name1":"小明","entity_lable1":"People","relation":"喜欢","name2":"摄影","entity_lable2":"Hobby"},
    {"name1":"小明","entity_lable1":"People","relation":"拥有技能","name2":"修电脑","entity_lable2":"Skill"},
    {"name1":"小明","entity_lable1":"People","relation":"拥有技能","name2":"写代码","entity_lable2":"Skill"},
    {"name1":"小明","entity_lable1":"People","relation":"高中毕业","name2":"京海市第一中学","entity_lable2":"School"},
    {"name1":"小明","entity_lable1":"People","relation":"大学毕业","name2":"清华大学","entity_lable2":"School"}
]
########################################################
给定实体:
{{entity_list}}
########################################################
给定文本:
{{text}}
########################################################
输出:
"""

# from jinja2 import Template

# class PromptTemplate:
#     def __init__(self, template: str,input_variables):
#         self.template = Template(template)
#         self.input_variables = input_variables
#     def render(self, **kwargs) -> str:
#         return self.template.render(**kwargs)

# p = PromptTemplate(entity_relation_prompt,['entity_list','text'])
# print(p.render(entity_lable_list="Person,Organization",text="星海市的市长李建国在任职期间与多家企业和非营利组织保持着紧密联系。"))  
# # print(p)