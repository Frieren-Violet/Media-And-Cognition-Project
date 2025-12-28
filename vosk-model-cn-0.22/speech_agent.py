"""
speech_agent.py
语音转文本代理类
提供 speech2text 方法，按住空格键录音，松开后返回识别文本
"""

import json
import os
import threading
import time

import numpy as np
import sounddevice as sd
from pynput import keyboard
from vosk import KaldiRecognizer, Model


class SpeechAgent:
    """语音转文本代理"""

    def __init__(self, model_path="."):
        """
        初始化语音代理

        Args:
            model_path: Vosk 模型路径，默认为当前目录
        """
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.sample_rate = 16000
        self.channels = 1
        self.is_recording = False
        self.audio_chunks = []
        self.lock = threading.Lock()
        self.stream = None
        self.recognized_text = None
        self.waiting = True  # 标记是否在等待录音

    def initialize(self):
        """初始化模型"""
        if not os.path.exists(self.model_path):
            print(f"错误: 未找到模型文件，请确认路径 '{self.model_path}' 是否正确")
            return False

        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            return True
        except Exception as e:
            print(f"✗ 模型加载失败: {e}")
            return False

    def audio_callback(self, indata, frames, time_info, status):
        """音频流回调函数"""
        if self.is_recording:
            with self.lock:
                self.audio_chunks.append(indata.copy())

    def start_recording(self):
        """开始录音"""
        with self.lock:
            self.audio_chunks = []

        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="int16",
                callback=self.audio_callback,
            )
            self.stream.start()
            print("🎤 正在录音...（松开空格键结束）")
        except Exception as e:
            print(f"启动录音失败: {e}")
            self.is_recording = False

    def stop_recording(self):
        """停止录音并识别"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        with self.lock:
            if len(self.audio_chunks) == 0:
                print("未录制到音频\n")
                self.recognized_text = None
                return

            # 合并音频数据
            audio_data = np.concatenate(self.audio_chunks)
            duration = len(audio_data) / self.sample_rate

            if duration < 0.1:
                print(f"录音时间太短（{duration:.2f}秒）\n")
                self.recognized_text = None
                return

            # 转换为 bytes
            audio_bytes = audio_data.tobytes()

        # 识别
        print("正在识别...")
        text = self.recognize(audio_bytes)
        self.recognized_text = text
        self.waiting = False  # 结束等待

    def recognize(self, audio_bytes):
        """识别语音"""
        if not audio_bytes or len(audio_bytes) == 0:
            return None

        try:
            # 重置识别器，清除之前的状态
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

            # 接收音频数据
            if self.recognizer.AcceptWaveform(audio_bytes):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip()
                return text if text else None
            else:
                # 处理部分识别结果
                partial = json.loads(self.recognizer.PartialResult())
                partial_text = partial.get("partial", "").strip()
                return partial_text if partial_text else None
        except Exception as e:
            print(f"识别失败: {e}")
            return None

    def speech2text(self):
        """
        等待用户操作，按下空格键录音，松开后返回识别文本

        Returns:
            str: 识别的文本，如果识别失败返回 None
        """
        # 初始化模型（如果还没初始化）
        if self.model is None:
            if not self.initialize():
                return None

        print("按住 [空格键] 开始录音，松开后识别")

        # 重置状态
        self.waiting = True
        self.is_recording = False
        self.recognized_text = None

        # 启动键盘监听
        with keyboard.Listener(
            on_press=self.on_key_press, on_release=self.on_key_release
        ) as listener:
            # 等待录音完成
            while self.waiting and listener.is_alive():
                time.sleep(0.1)

        # 返回识别结果
        if self.recognized_text:
            print(f"识别结果: {self.recognized_text}\n")
            return self.recognized_text
        else:
            print("未识别到语音\n")
            return None

    def on_key_press(self, key):
        """按键按下事件"""
        if self.waiting and key == keyboard.Key.space:
            if not self.is_recording and self.stream is None:
                self.is_recording = True
                # 在新线程中启动录音
                threading.Thread(target=self.start_recording, daemon=True).start()

        # 返回 True 继续监听，返回 False 停止监听
        return self.waiting

    def on_key_release(self, key):
        """按键释放事件"""
        if self.waiting and key == keyboard.Key.space:
            if self.is_recording:
                self.is_recording = False
                # 在新线程中停止录音并识别
                threading.Thread(target=self.stop_recording, daemon=True).start()

        return self.waiting


def main():
    """测试函数"""
    print("=" * 60)
    print("SpeechAgent 测试")
    print("=" * 60 + "\n")

    # 创建语音代理
    agent = SpeechAgent(".")

    text = agent.speech2text()
    if text:
        print(f"返回的文本: {text}")
    else:
        print("未返回文本")


if __name__ == "__main__":
    main()
