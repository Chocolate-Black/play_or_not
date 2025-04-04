# Play or Not - Steam遊戲AI推薦系統

<a name="readme-top"></a>

<div align="center">

[English](README.md) | [中文](README_CN.md) | 繁體中文

</div>

---

一個基於gradio的網頁應用，可以分析Steam遊戲並提供AI驅動的遊玩建議。

## 功能特點

- **遊戲分析**: 從Steam獲取遊戲詳情(名稱、價格、評價)
- **AI推薦**: 使用大語言模型分析遊戲好評與差評，提供遊玩建議
- **多語言支持**: 支持簡體中文、繁體中文和英文

## 系統要求

- python>=3.11

## 快速開始

### 1. 使用.bat文件(Windows)

1. (首次使用)克隆本倉庫
2. (首次使用)編輯`configs/model_configs.json`文件:
   - 添加/刪除AI模型
   - 調整模型參數
   - 配置API密鑰
   - 更多詳情: https://doc.agentscope.io/build_tutorial/monitor.html
3. (首次使用)運行`setup.bat`
4. 運行`start.bat`
5. 在瀏覽器中打開Gradio界面(默認: http://127.0.0.1:7860)
6. 輸入Steam遊戲URL(例如`https://store.steampowered.com/app/...`)
7. 選擇偏好語言、AI模型和其他參數
8. 點擊"提交"獲取AI推薦

### 2. 手動安裝

1. 克隆本倉庫

2. 創建並激活虛擬環境(conda):

   ```bash
   conda create -n "my_env" python=3.11
   conda actiavte "my_env"
   ```

3. 安裝依賴包:

   ```bash
   pip install -r requirements.txt
   ```

4. 編輯`configs/model_configs.json`

5. 啟動Web界面:

   ```bash
   python web.py
   ```

6. 在瀏覽器中打開Gradio界面(默認: http://127.0.0.1:7860)

7. 輸入Steam遊戲URL(例如`https://store.steampowered.com/app/...`)

8. 選擇偏好語言、AI模型和其他參數

9. 點擊"提交"獲取AI推薦

## 支持的大語言模型API

(更多詳情: https://doc.agentscope.io/build_tutorial/model.html)

- OpenAI(及所有OpenAI兼容模型)
- DashScope
- Gemini
- Ollama
- Yi
- LiteLLM
- ZhipuAI
- Anthropic

## 未來計劃

- [ ] 支持日語等其他語言
- [ ] 添加基於Steam願望單和預算的遊戲購買計劃功能
