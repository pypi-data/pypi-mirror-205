#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatpdf
# @Time         : 2023/4/25 17:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import streamlit as st
from meutils.pipe import *
from meutils.office_automation.pdf import extract_text
from appzoo.streamlit_app.utils import display_pdf, reply4input

from chatllm.applications import ChatBase


st.set_page_config(page_title='🔥ChatPDF', layout='wide', initial_sidebar_state='collapsed')


class Conf(BaseConfig):
    embedding = 'shibing624/text2vec-base-chinese'


conf = Conf()

for k, v in conf:  # 更新配置
    setattr(conf, k, st.sidebar.text_input(label=k, value=v))

file = st.sidebar.file_uploader("上传PDF", type=['pdf'])
text = ''
bytearray = None
if file:
    bytearray = file.read()
    text = extract_text(stream=bytearray)

tabs = st.tabs(['ChatPDF', 'PDF文件预览'])

with tabs[0]:
    if file:
        container = st.container()  # 占位符
        text = st.text_area(label="用户输入", height=100, placeholder="请在这儿输入您的问题")

        if st.button("发送", key="predict"):
            with st.spinner("AI正在思考，请稍等........"):
                history = st.session_state.get('state')
                st.session_state["state"] = reply4input(text, history, container=container)
                print(st.session_state['state'])

with tabs[1]:
    if file:
        base64_pdf = base64.b64encode(bytearray).decode('utf-8')
        display_pdf(base64_pdf)
    else:
        st.warning('### 请先上传PDF')
