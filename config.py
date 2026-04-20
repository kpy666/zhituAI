# -*- coding: utf-8 -*-
"""
API配置文件
"""

API_KEY = "274cb82566e9418b9d2edabaf78992d9.b6cVWW72q8c4TMmU"

LLM_PROVIDER = "glm-5"

API_CONFIGS = {
    "glm": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4"
    },
    "glm-5": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4-flash"
    },
    "qwen": {
        "base_url": "https://dashscope.aliyuncs.com/api/v1",
        "model": "qwen-turbo"
    },
    "ernie": {
        "base_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1",
        "model": "ernie-bot"
    }
}
