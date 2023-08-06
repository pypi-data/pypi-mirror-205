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

# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2"

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
    if stream and hasattr(model, 'stream_chat'):
        return partial(model.stream_chat, tokenizer=tokenizer)
    else:
        return partial(model.chat, tokenizer=tokenizer)


def load_llm(model_name_or_path="THUDM/chatglm-6b", device=DEVICE, num_gpus=1, checkpoint="chatglm_checkpoint",
             **kwargs):
    model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

    if torch.cuda.is_available() and device.lower().startswith("cuda"):
        if num_gpus == 1:  # 单卡
            model = model.half().cuda()
            # model.transformer.prefix_encoder.float()
        elif 'chatglm' in model_name_or_path:  # chatglm多卡
            num_gpus = min(num_gpus, torch.cuda.device_count())
            model = load_chatglm_on_gpus(model, model_name_or_path, num_gpus, checkpoint=checkpoint)

    else:
        model = model.float().to(device)

    return model.eval(), tokenizer


def load_chatglm_on_gpus(model, model_name_or_path, num_gpus=2, checkpoint="chatglm_checkpoint"):
    """https://github.com/THUDM/ChatGLM-6B/issues/200"""
    from accelerate import load_checkpoint_and_dispatch

    device_map = auto_configure_device_map(num_gpus)
    try:
        model = load_checkpoint_and_dispatch(model, model_name_or_path, device_map=device_map, offload_folder="offload",
                                             offload_state_dict=True).half()
    except ValueError:
        logger.info('多卡加载，第一次需要缓存模型')
        model.save_pretrained(checkpoint, max_shard_size='2GB')
        model = load_checkpoint_and_dispatch(model, checkpoint, device_map=device_map,
                                             offload_folder="offload", offload_state_dict=True).half()
    return model


def auto_configure_device_map(num_gpus: int) -> Dict[str, int]:
    # 总共占用13GB显存,28层transformer每层0.39GB左右
    # 第一层 word_embeddings和最后一层 lm_head 层各占用1.2GB左右
    num_trans_layers = 28
    vram_per_layer = 0.39
    average = 13 / num_gpus
    used = 1.2
    device_map = {
        'transformer.word_embeddings': 0,
        'transformer.final_layernorm': num_gpus - 1,
        'lm_head': num_gpus - 1
    }
    gpu_target = 0
    for i in range(num_trans_layers):
        if used > average - vram_per_layer / 2 and gpu_target < num_gpus:
            gpu_target += 1
            used = 0
        else:
            used += vram_per_layer

        device_map[f'transformer.layers.{i}'] = gpu_target
        used += 1

    return device_map


if __name__ == '__main__':
    model, tokenizer = load_llm("/CHAT_MODEL/chatglm", device='cpu')
