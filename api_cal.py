import requests
import argparse
import os

def call_tts_api(text, speaker, output_file='output.wav', format='wav', speed=1.0, streaming=0, instruct=None):
    """调用TTS接口并下载合成的音频文件"""
    # 接口URL（假设服务运行在本地9880端口）
    url = 'http://localhost:9880/tts'
    
    # 准备请求参数
    params = {
        'text': text,
        'speaker': speaker,
        'format': format,
        'speed': speed,
        'streaming': streaming
    }
    
    # 添加可选参数
    if instruct:
        params['instruct'] = instruct
    
    try:
        # 发送GET请求（也可以使用POST，根据需要选择）
        print(f"正在请求TTS服务：text='{text}', speaker='{speaker}'")
        response = requests.get(url, params=params)
        
        # 检查响应状态
        if response.status_code == 200:
            # 保存音频文件
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"音频文件已保存到：{output_file}")
            return True
        else:
            print(f"请求失败，状态码：{response.status_code}")
            try:
                # 尝试解析JSON错误信息
                error_info = response.json()
                print(f"错误信息：{error_info}")
            except:
                print(f"响应内容：{response.text}")
            return False
    except Exception as e:
        print(f"请求异常：{e}")
        return False

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='调用TTS接口合成语音')
    parser.add_argument('--text', type=str, required=True, help='要合成的文本')
    parser.add_argument('--speaker', type=str, required=True, help='说话人/音色名称')
    parser.add_argument('--output', type=str, default='output.wav', help='输出音频文件名')
    parser.add_argument('--format', type=str, default='wav', help='音频格式，如wav, ogg等')
    parser.add_argument('--speed', type=float, default=1.0, help='语速，默认为1.0')
    parser.add_argument('--streaming', type=int, choices=[0, 1], default=0, help='是否流式输出，0为非流式，1为流式')
    parser.add_argument('--instruct', type=str, help='指示模式文本（可选）')
    
    args = parser.parse_args()
    
    # 调用TTS接口
    call_tts_api(
        text=args.text,
        speaker=args.speaker,
        output_file=args.output,
        format=args.format,
        speed=args.speed,
        streaming=args.streaming,
        instruct=args.instruct
    )

# python api_cal.py --text "你好，这是一段测试文本" --speaker "中文男" --output "test.wav"