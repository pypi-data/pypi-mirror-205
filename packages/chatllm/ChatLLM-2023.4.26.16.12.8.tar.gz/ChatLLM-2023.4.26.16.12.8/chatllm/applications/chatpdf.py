#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ChatPDF
# @Time         : 2023/4/21 11:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.office_automation.pdf import extract_text, pdf2text

from chatllm.utils import textsplitter
from chatllm.applications.chatann import ChatANN


class ChatPDF(ChatANN):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_ann_index(self, file, textsplitter=textsplitter):  # todo 多篇 增加parser
        texts = extract_text(file)
        texts = textsplitter(texts)
        return super().create_ann_index(texts)


if __name__ == '__main__':
    filename = '../../data/财报.pdf'
    bytes_array = Path(filename).read_bytes()
    texts = extract_text(bytes_array)
    texts = textsplitter(texts)
    print(texts)
