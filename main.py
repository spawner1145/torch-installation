import re
import os
import sys
import subprocess

def extract_cuda_version(nvcc_output):
    """
    从nvcc --version命令的输出中提取CUDA版本，并转换为用于构建PyTorch URL的形式。
    :param nvcc_output: str, nvcc --version命令的输出字符串。
    :return: str, 转换后的CUDA版本号，如'cu121'。
    """
    match = re.search(r'release (\d+\.\d+)', nvcc_output)
    if match:
        cuda_version = match.group(1)
        major, minor = cuda_version.split('.')
        return f'cu{major}{minor}'
    else:
        return None

def ai_req(python_path='python'):
    try:
        nvcc_output = subprocess.check_output(["nvcc", "--version"], stderr=subprocess.STDOUT).decode()
        cuda_torch_suffix = extract_cuda_version(nvcc_output)
        if cuda_torch_suffix:
            print(f"检测到CUDA版本：{cuda_torch_suffix[2:]}，正在安装支持CUDA的PyTorch...")
        else:
            print("未能检测到CUDA版本，假设系统中未安装CUDA。")
    except Exception as e:
        print(f"未能检测到CUDA版本或nvcc未安装，假设系统中未安装CUDA。错误信息：{e}")
        cuda_torch_suffix = None
    
    try:
        os.system(f"\"{python_path}\" -m pip install opencv-python-headless")

        if cuda_torch_suffix:
            os.system(f"\"{python_path}\" -m pip install torch torchvision torchaudio --index-url=https://download.pytorch.org/whl/{cuda_torch_suffix}")
        else:
            print("未检测到CUDA或CUDA版本不受支持，正在安装仅CPU版本的PyTorch...")
            os.system(f"\"{python_path}\" -m pip install torch torchvision torchaudio")

    except subprocess.CalledProcessError as e:
        print(f"安装PyTorch时出错：{e}")
        sys.exit(1)
        return

    print("ai相关库安装成功完成")
    return

if __name__ == "__main__":
    python_path = 'python'
    ai_req(python_path)
