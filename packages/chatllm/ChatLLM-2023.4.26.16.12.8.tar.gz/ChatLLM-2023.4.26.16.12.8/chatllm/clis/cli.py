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
def run_chatpdf():
    main = get_resolve_path('../webui/chatpdf.py', __file__)
    os.system(f'streamlit run {main}')


if __name__ == '__main__':
    cli()
