![image](https://img.shields.io/pypi/v/llm4gpt.svg) ![image](https://img.shields.io/travis/yuanjie-ai/llm4gpt.svg) ![image](https://readthedocs.org/projects/llm4gpt/badge/?version=latest)



<h1 align = "center">🔥ChatLLM🔥</h1>

---

# Install

```python
pip install -U llm4gpt
```

# [Docs](https://jie-yuan.github.io/ChatLLM/)

# Usages

```python
from chatllm.applications import ChatBase

qa = ChatBase()
qa.load_llm4chat(model_name_or_path="MODEL")

for i, _ in qa(query='周杰伦是谁', knowledge_base='周杰伦是傻子'):
    pass
# 根据已知信息无法回答该问题，因为周杰伦是中国内地流行歌手、演员、音乐制作人、导演，
# 是具有一定的知名度和专业能力的人物，没有提供足够的信息无法判断他是傻子。
```

---

# TODO

- [ ] 增加UI

- [x] 增加本地知识库组件

- [ ] 增加互联网搜索组件

- [ ] 增加知识图谱组件

- [ ] 增加微调模块

- [ ] 增加流式输出



