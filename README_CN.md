# Play or Not - Steam游戏AI推荐系统

<a name="readme-top"></a>

<div align="center">

[English](README.md) | 中文 | [繁體中文](README_CN_TW.md)

</div>

---

一个基于gradio的网页应用，可以分析Steam游戏并提供AI驱动的游玩建议。

## 功能特点

- **游戏分析**: 从Steam获取游戏详情(名称、价格、评价)
- **AI推荐**: 使用大语言模型分析游戏好评与差评，提供游玩建议
- **多语言支持**: 支持简体中文、繁体中文和英文

## 系统要求

- python>=3.11

## 快速开始

### 1. 使用.bat文件(Windows)

1. (首次使用)克隆本仓库
2. (首次使用)编辑`configs/model_configs.json`文件:
   - 添加/删除AI模型
   - 调整模型参数
   - 配置API密钥
   - 更多详情: https://doc.agentscope.io/build_tutorial/monitor.html
3. (首次使用)运行`setup.bat`
4. 运行`start.bat`
5. 在浏览器中打开Gradio界面(默认: http://127.0.0.1:7860)
6. 输入Steam游戏URL(例如`https://store.steampowered.com/app/...`)
7. 选择偏好语言、AI模型和其他参数
8. 点击"提交"获取AI推荐

### 2. 手动安装

1. 克隆本仓库

2. 创建并激活虚拟环境(conda):

   ```bash
   conda create -n "my_env" python=3.11
   conda actiavte "my_env"
   ```

3. 安装依赖包:

   ```bash
   pip install -r requirements.txt
   ```

4. 编辑`configs/model_configs.json`

5. 启动Web界面:

   ```bash
   python web.py
   ```

6. 在浏览器中打开Gradio界面(默认: http://127.0.0.1:7860)

7. 输入Steam游戏URL(例如`https://store.steampowered.com/app/...`)

8. 选择偏好语言、AI模型和其他参数

9. 点击"提交"获取AI推荐

## 支持的大语言模型API

(更多详情: https://doc.agentscope.io/build_tutorial/model.html)

- OpenAI(及所有OpenAI兼容模型)
- DashScope
- Gemini
- Ollama
- Yi
- LiteLLM
- ZhipuAI
- Anthropic

## 未来计划

- [ ] 支持日语等其他语言
- [ ] 添加基于Steam愿望单和预算的游戏购买计划功能
