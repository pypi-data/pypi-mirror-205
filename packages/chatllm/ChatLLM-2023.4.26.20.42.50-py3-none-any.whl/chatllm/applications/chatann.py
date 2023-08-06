#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ann4qa
# @Time         : 2023/4/24 18:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from chatllm.applications import ChatBase
from chatllm.embedding import SentenceEmbedding


class ChatANN(ChatBase):

    def __init__(self, backend='docarray', encode_model="nghuyong/ernie-3.0-nano-zh", **kwargs):
        """

        :param backend:
        :param encode_model:
            "nghuyong/ernie-3.0-nano-zh"
            "shibing624/text2vec-base-chinese"
            "GanymedeNil/text2vec-large-chinese"
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.backend = backend  # todo 增加更多的ann后端

        self.encode = SentenceEmbedding(encode_model).encode  # 加缓存

        # create index
        self.index = None

        # 召回结果df
        self._df = pd.DataFrame({'id': [], 'text': [], 'score': []})

    def qa(self, query, topk=3, threshold=0.66, **kwargs):
        df = self.find(query, topk, threshold)
        if len(df) == 0:
            logger.warning('召回内容为空!!!')
        knowledge_base = '\n'.join(df.text)

        return self._qa(query, knowledge_base, **kwargs)

    def find(self, query, topk=5, threshold=0.66):  # 返回df
        v = self.encode(query)[0]
        if self.backend == 'docarray':
            result = self.index.find(v, limit=topk)[:, ('id', 'text', 'scores__cosine__value')]
            df = pd.DataFrame(zip(*result))
            df.columns = ('id', 'text', 'score')
            df['score'] = 1 - df['score']
            self._df = df.query(f'score > {threshold}')
            return self._df

    def create_index(self, texts):
        self.index = self.encode(texts, show_progress_bar=True, return_document=True)


if __name__ == '__main__':

    qa = ChatANN(chat_func=None)
    qa.load_llm4chat(model_name_or_path="/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm")

    for i, _ in qa(query='1+1'):
        pass
