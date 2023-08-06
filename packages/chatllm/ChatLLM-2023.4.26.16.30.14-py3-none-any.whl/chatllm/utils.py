#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2023/4/20 12:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import torch
from transformers import AutoTokenizer, AutoModel

from meutils.pipe import *

DEVICE = (
    os.environ['DEVICE']
    if 'DEVICE' in os.environ else "cuda"
    if torch.cuda.is_available() else "mps"
    if torch.backends.mps.is_available() else "cpu"
)

# todo 多卡 https://github.com/THUDM/ChatGLM-6B#%E5%A4%9A%E5%8D%A1%E9%83%A8%E7%BD%B2

def textsplitter(text, chunk_size=512, overlap_rate=0.2, sep=''):  # 简单粗暴
    return text.lower().split() | xjoin(sep) | xgroup(chunk_size, overlap_rate)


def load_llm4chat(model_name_or_path="THUDM/chatglm-6b", device=DEVICE, stream=True, **kwargs):
    model, tokenizer = load_llm(model_name_or_path, device, **kwargs)
    if stream:
        return partial(model.stream_chat, tokenizer=tokenizer)
    else:
        return partial(model.chat, tokenizer=tokenizer)


def load_llm(model_name_or_path="THUDM/chatglm-6b", device=DEVICE, device_map: Optional[Dict[str, int]] = None,
             **kwargs):
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True, **kwargs)

    if torch.cuda.is_available() and device.lower().startswith("cuda"):
        # 根据当前设备GPU数量决定是否进行多卡部署
        num_gpus = torch.cuda.device_count()
        if num_gpus < 2 and device_map is None:
            model = model.half().cuda()
        else:
            from accelerate import dispatch_model
            # 可传入device_map自定义每张卡的部署情况
            if device_map is None:
                device_map = auto_configure_device_map(num_gpus)

            model = dispatch_model(model, device_map=device_map).half().cuda()

    else:
        model = model.float().to(device)

    return model.eval(), tokenizer


def auto_configure_device_map(num_gpus: int) -> Dict[str, int]:
    # transformer.word_embeddings 占用1层
    # transformer.final_layernorm 和 lm_head 占用1层
    # transformer.layers 占用 28 层
    # 总共30层分配到num_gpus张卡上
    num_trans_layers = 28
    per_gpu_layers = 30 / num_gpus

    # bugfix: 在linux中调用torch.embedding传入的weight,input不在同一device上,导致RuntimeError
    # windows下 model.device 会被设置成 transformer.word_embeddings.device
    # linux下 model.device 会被设置成 lm_head.device
    # 在调用chat或者stream_chat时,input_ids会被放到model.device上
    # 如果transformer.word_embeddings.device和model.device不同,则会导致RuntimeError
    # 因此这里将transformer.word_embeddings,transformer.final_layernorm,lm_head都放到第一张卡上
    device_map = {'transformer.word_embeddings': 0,
                  'transformer.final_layernorm': 0, 'lm_head': 0}

    used = 2
    gpu_target = 0
    for i in range(num_trans_layers):
        if used >= per_gpu_layers:
            gpu_target += 1
            used = 0
        assert gpu_target < num_gpus
        device_map[f'transformer.layers.{i}'] = gpu_target
        used += 1

    return device_map


if __name__ == '__main__':
    a = llm_load("/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm")
