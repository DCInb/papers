




import os
from openai import OpenAI

client = OpenAI(
    # 从环境变量中读取您的方舟API Key
    api_key='9014dee5-9a23-44d1-b4fb-cc59c9ad0b6b',
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    )
completion = client.chat.completions.create(
    # 将推理接入点 <Model>替换为 Model ID
    model="deepseek-r1-250120",
    messages=[
        {"role": "user", "content": "常见的十字花科植物有哪些？"}
    ]
)
print(completion.choices[0].message)