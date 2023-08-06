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
from chatllm.utils import load_llm4chat
from chatllm.applications import ChatBase

chat_func = load_llm4chat("THUDM/chatglm-6b")

qa = ChatBase(chat_func=chat_func)

for i, _ in qa(query='周杰伦是谁', knowledge_base='周杰伦是傻子'):
    print(_, flush=True)


# 解析知识库
texts = []
metadatas = []
for p in Path('data').glob('*.txt'):
    texts.append(p.read_text())
    metadatas.append({'source': p})

# 文档向量化
faissann = FaissANN(model_name_or_path="shibing624/text2vec-base-chinese")
faissann.add_texts(texts, metadatas)

# 构建pipeline
model, tokenizer = llm_load(model_name_or_path="THUDM/chatglm-6b", device='cpu')
glm = ChatLLM()
glm.chat_func = partial(model.chat, tokenizer=tokenizer)

qa = QA(glm, faiss_ann=faissann.faiss_ann)

qa.get_knowledge_based_answer('周杰伦在干吗')
qa.get_knowledge_based_answer('姚明住哪里')
```

---

# TODO

- [ ] 增加UI

- [x] 增加本地知识库组件

- [ ] 增加互联网搜索组件

- [ ] 增加知识图谱组件

- [ ] 增加微调模块

- [ ] 增加流式输出



