![image](https://img.shields.io/pypi/v/llm4gpt.svg) ![image](https://img.shields.io/travis/yuanjie-ai/llm4gpt.svg) ![image](https://readthedocs.org/projects/llm4gpt/badge/?version=latest)

<h1 align = "center">🔥ChatLLM🔥</h1>

# Install

```shell
pip install -U chatllm
```

# [Docs](https://jie-yuan.github.io/ChatLLM/)

# Usages

```python
from chatllm.applications import ChatBase

qa = ChatBase()
qa.load_llm4chat(model_name_or_path="THUDM/chatglm-6b")

for i, _ in qa(query='周杰伦是谁', knowledge_base='周杰伦是傻子'):
    pass
# 根据已知信息无法回答该问题，因为周杰伦是中国内地流行歌手、演员、音乐制作人、导演，
# 是具有一定的知名度和专业能力的人物，没有提供足够的信息无法判断他是傻子。
```

<details markdown="1">
  <summary>Click to ChatPDF</summary>

```python
from chatllm.applications.chatpdf import ChatPDF

qa = ChatPDF(encode_model='nghuyong/ernie-3.0-nano-zh')
qa.load_llm4chat(model_name_or_path="THUDM/chatglm-6b")
for i, _ in qa(query='东北证券主营业务'):
    pass
# 根据已知信息，东北证券的主营业务为证券业务。公司作为证券公司，主要从事证券经纪、证券投资咨询、与证券交易、
# 证券投资活动有关的财务顾问、证券承销与保荐、证券自营、融资融券、证券投资基金代销和代销金融产品待业务。
```

![向量召回结果](data/imgs/chatpdf_ann_df.png)

</details>

---

<details markdown="1">
  <summary>Click to TODO</summary

- [ ] 增加UI

- [ ] 增加ChatPDF

- [x] 增加本地知识库组件

- [ ] 增加互联网搜索组件

- [ ] 增加知识图谱组件

- [ ] 增加微调模块

- [x] 增加流式输出

- [ ] 增加http接口

- [ ] 增加grpc接口

</details>


---

[ChatGLM-6B Mac 本地部署实操记录](https://www.yuque.com/arvinxx/llm/chatglm-6b-deployment-on-mac)

