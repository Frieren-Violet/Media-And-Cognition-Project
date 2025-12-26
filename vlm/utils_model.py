import openai
import base64
from typing import Optional
import os
from dotenv import load_dotenv


def encode_image_to_base64(image_path: str) -> str:
    """
    将本地图片文件编码为base64格式
    
    Args:
        image_path: 图片文件的本地路径
        
    Returns:
        图片的base64编码字符串
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def call_vlm(prompt: str, api_key: str, base_url: str, image_path: Optional[str] = None, model: str = "GLM-4.5V") -> str:
    """
    调用大语言模型API进行视觉理解
    
    Args:
        prompt: 发送给模型的文本提示词
        api_key: API密钥
        base_url: API的基础URL
        image_path: 图片文件的本地路径（可选）。如果提供，图片会被编码为base64格式发送
        model: 要使用的模型ID，默认为"GLM-4.5V"
        
    注意事项：
        - 如果调用图片，请使用支持视觉的模型，如：GLM-4.5V, GLM-4V, GLM-4V-Flash, Qwen2.5-VL-7B-Instruct等
        - 请根据您的API权限选择合适的模型ID
        
    Returns:
        模型的响应内容
    """
    # 创建客户端实例
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    # 构建消息内容
    content = []
    
    # 如果提供了图片路径，添加图片内容
    if image_path:
        base64_image = encode_image_to_base64(image_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    
    # 添加文本提示词
    content.append({
        "type": "text",
        "text": prompt
    })
    
    # 构建完整的消息
    messages = [{
        "role": "user",
        "content": content
    }]
    
    # 调用API
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    # 返回模型的响应内容
    return response.choices[0].message.content


def call_llm(prompt: str, api_key: str, base_url: str, model: str = "GLM-4.6") -> str:
    """
    调用大语言模型API进行文本生成
    
    Args:
        prompt: 发送给模型的文本提示词
        api_key: API密钥
        base_url: API的基础URL
        model: 要使用的模型ID，默认为"GLM-4"
        
    注意事项：
        - 这是一个纯文本模型调用函数，不支持图片输入
        - 推荐使用的文本模型包括：GLM-4, GLM-3-Turbo, Qwen2.5-7B-Instruct等
        - 请根据您的API权限选择合适的模型ID
        
    Returns:
        模型的响应内容
    """
    # 创建客户端实例
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # 构建消息
    messages = [{
        "role": "user",
        "content": prompt
    }]
    
    # 调用API
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    # 返回模型的响应内容
    return response.choices[0].message.content


# 示例使用
if __name__ == "__main__":
    # API配置
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("PARATERA_BASE_URL")
    
    if not api_key:
        raise ValueError("请在 .env 文件中配置 OPENAI_API_KEY")

    # 示例1：仅文本（使用call_llm）
    print("示例1：纯文本LLM调用")
    response = call_llm("介绍一下清华大学电子系的媒体与认知课程", api_key, base_url)
    print(response)
    
    # # 示例2：图片+文本（使用call_vlm，需要提供真实的图片路径）
    # print("\n示例2：图片+文本VLM调用")
    # response = call_vlm("请描述这张图片的内容", api_key, base_url, image_path="./lan.png")
    # print(response)
