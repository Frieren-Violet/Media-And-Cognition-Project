import json
from typing import Dict, Any
from utils_model import call_llm
import os
from dotenv import load_dotenv


# 系统提示词，描述大模型的背景和任务
SYSTEM_PROMPT = """
你是一个智能机械臂控制助手，负责根据用户的自然语言指令，识别物体的位置并规划机械臂的运动轨迹。

## 任务描述
你将接收：
1. 物体识别结果：通过YOLO模型识别到的物体及其三维空间坐标（x, y, z）
2. 垃圾桶坐标信息：各个垃圾桶的三维坐标
3. 用户指令：用户的自然语言描述，例如"把小猫放到红色垃圾桶里"

## 输出要求
你必须严格输出一个JSON格式的字符串，包含以下字段：
- "start": 一个三维数组，表示起始物体的三维坐标 [x, y, z]
- "end": 一个三维数组，表示目标位置的三维坐标 [x, y, z]

## 注意事项
1. 严格输出JSON格式，不要包含任何其他文本或解释
2. 从物体识别结果中找到用户提到的起始物体
3. 从垃圾桶坐标信息中找到用户提到的目标垃圾桶
4. 如果无法识别物体或垃圾桶，返回坐标为 [0, 0, 0]
5. 保持数值精度，不要四舍五入
"""


class RoboticArmAgent:
    """机械臂智能代理类"""
    
    def __init__(self, api_key: str, base_url: str, model: str = "GLM-4.6"):
        """
        初始化机械臂代理
        
        Args:
            api_key: API密钥
            base_url: API基础URL
            model: 使用的模型名称
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    def process_instruction(
        self,
        detected_objects: Dict[str, list],
        trash_bins: Dict[str, list],
        user_instruction: str
    ) -> Dict[str, list]:
        """
        处理用户指令，生成机械臂运动轨迹
        
        Args:
            detected_objects: 检测到的物体及其坐标，格式为 {"物体名称": [x, y, z], ...}
            trash_bins: 垃圾桶的坐标信息，格式为 {"垃圾桶名称": [x, y, z], ...}
            user_instruction: 用户的自然语言指令，例如"把小猫放到红色垃圾桶里"
            
        Returns:
            包含start和end坐标的字典，格式为 {"start": [x, y, z], "end": [x, y, z]}
        """
        # 构建用户提示词（包含系统提示词）
        user_prompt = f"""{SYSTEM_PROMPT}

## 输入数据

### 物体识别结果
```json
{json.dumps(detected_objects, ensure_ascii=False, indent=2)}
```

### 垃圾桶坐标信息
```json
{json.dumps(trash_bins, ensure_ascii=False, indent=2)}
```

### 用户指令
"{user_instruction}"

请根据以上信息，输出机械臂的起始位置和目标位置坐标。
"""
        
        # 调用大语言模型
        response = call_llm(
            prompt=user_prompt,
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model
        )
        
        print(f"模型原始响应: {response}")
        
        try:
            # 尝试解析JSON响应
            result = json.loads(response)
            
            # 验证返回格式
            if not isinstance(result, dict):
                raise ValueError("返回值不是字典格式")
            
            if "start" not in result or "end" not in result:
                raise ValueError("缺少必需的start或end字段")
            
            if not isinstance(result["start"], list) or not isinstance(result["end"], list):
                raise ValueError("start或end不是列表格式")
            
            if len(result["start"]) != 3 or len(result["end"]) != 3:
                raise ValueError("start或end坐标不完整，需要3个值")
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            print(f"原始响应: {response}")
            return {"start": [0, 0, 0], "end": [0, 0, 0]}
        except ValueError as e:
            print(f"格式验证失败: {e}")
            return {"start": [0, 0, 0], "end": [0, 0, 0]}


# 示例使用
if __name__ == "__main__":
    # 配置API信息
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("PARATERA_BASE_URL")
    
    if not api_key:
        raise ValueError("请在 .env 文件中配置 OPENAI_API_KEY")
    
    # 创建代理实例
    agent = RoboticArmAgent(api_key=api_key, base_url=base_url)
    
    # 示例数据：检测到的物体
    detected_objects = {
        "小猫": [10.5, 20.3, 15.2],
        "杯子": [5.2, 8.7, 12.1],
        "书本": [15.8, 18.2, 14.5]
    }
    
    # 示例数据：垃圾桶坐标
    trash_bins = {
        "红色垃圾桶": [30.5, 25.3, 10.0],
        "蓝色垃圾桶": [35.2, 28.7, 10.0],
        "绿色垃圾桶": [40.8, 22.2, 10.0]
    }
    
    # 用户指令
    user_instruction = "把小猫放到红色垃圾桶里"
    
    # 处理指令
    print(f"用户指令: {user_instruction}")
    print(f"检测到的物体: {detected_objects}")
    print(f"垃圾桶坐标: {trash_bins}")
    print("\n正在处理...")
    
    result = agent.process_instruction(
        detected_objects=detected_objects,
        trash_bins=trash_bins,
        user_instruction=user_instruction
    )
    
    print("\n处理结果:")
    print(f"起始位置 (start): {result['start']}")
    print(f"目标位置 (end): {result['end']}")
