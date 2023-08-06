#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/1/31 10:20 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : python meutils/clis/__init__.py
import os

from meutils.pipe import *

cli = typer.Typer(name="ChatLLM CLI")


@cli.command(help="help")  # help会覆盖docstring
def clitest(name: str = 'TEST'):
    """

    @param name: name
    @return:
    """
    typer.echo(f"Hello {name}")


@cli.command()  # help会覆盖docstring
def webui(name: str = 'chatpdf'):
    """
        chatllm-run webui --name chatpdf
    """
    main = get_resolve_path(f'../webui/{name}.py', __file__)
    os.system(f'streamlit run {main}')


@cli.command()  # help会覆盖docstring
def flask_api(host='127.0.0.1', port=8000, debug=True):
    """
        chatllm-run flask-api --host 127.0.0.1 --port 8000
    """
    from chatllm.applications import ChatBase

    qa = ChatBase()
    qa.load_llm4chat(model_name_or_path="/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm")

    from flask import Flask, Response, jsonify, request

    app = Flask(__name__)

    def gen(**input):
        for response, _ in qa(**input):
            yield f"{response}\n"

    # 流式接口路由
    @app.route('/', methods=['GET', 'POST'])
    def stream():
        input = {'query': '你是谁'}
        input.update(request.args.to_dict())
        if request.data.startswith(b'{'):
            input.update(json.loads(request.data))

        return Response(gen(**input), mimetype='text/event-stream')

    app.run(host=host, port=port, debug=debug)


#


if __name__ == '__main__':
    cli()
