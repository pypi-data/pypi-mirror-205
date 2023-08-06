#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : Question2Answer
# @Time         : 2023/4/21 12:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import types
from meutils.pipe import *
from meutils.decorators import clear_cuda_cache

from chatllm.utils import DEVICE, load_llm4chat


class ChatBase(object):

    def __init__(self, chat_func=None, prompt_template=None,
                 role='你扮演的角色是ChatLLM智能机器人🤖，由Betterme二次开发'):
        self.chat_func = chat_func
        self.prompt_template = prompt_template if prompt_template else self.default_document_prompt
        self.role = role

        #
        self.history = []
        self.knowledge_base = None

    def __call__(self, **kwargs):
        return self.qa(**kwargs)

    def qa(self, query, knowledge_base='请自由回答', **kwargs):
        """可重写"""
        return self._qa(query, knowledge_base, **kwargs)

    def set_chat_kwargs(self, **kwargs):
        self.chat_func = partial(self.chat_func, **kwargs)

    @clear_cuda_cache
    def _qa(self, query, knowledge_base='', max_turns=1):
        self.knowledge_base = knowledge_base if knowledge_base.strip() else '请自由回答'

        query = self.prompt_template.format(context=self.knowledge_base, question=query, role=self.role)

        _history = self.history[-(max_turns - 1):] if max_turns > 1 else []
        result = self.chat_func(query=query, history=_history)

        if isinstance(result, types.GeneratorType):
            return self._stream(result)
        else:  # list(self._stream(result)) 想办法合并
            response, history = result
            # self.history_ = history  # 历史所有
            self.history += [[None, response]]  # 置空知识
            return result  # response, history

    def _stream(self, result):  # yield > return
        response = None
        bar = tqdm(result, ascii=True)  # ncols
        for response, history in bar:
            bar.set_description(response)
            yield response, history
        # self.history_ = history  # 历史所有
        self.history += [[None, response]]  # 置空知识

    def load_llm4chat(self, model_name_or_path="THUDM/chatglm-6b", device=DEVICE, stream=True, **kwargs):
        assert not self.chat_func, "overwrite chat_func"
        self.chat_func = load_llm4chat(model_name_or_path, device, stream, **kwargs)

    @property
    def default_document_prompt(self):
        prompt_template = """
            {role} 基于以下已知信息，简洁和专业的来回答问题。
            如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的信息"，不允许在答案中添加编造成分，答案请使用中文。
            已知信息: {context}
            问题: {question}
            """.strip()

        return prompt_template


if __name__ == '__main__':
    from chatllm.applications import ChatBase

    qa = ChatBase()
    qa.load_llm4chat(model_name_or_path="/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm")

    for i, _ in qa(query='周杰伦是谁', knowledge_base='周杰伦是傻子'):
        pass

    for i, _ in qa(query='你是谁', knowledge_base='自由回答'):
        pass
