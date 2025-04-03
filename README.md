# Play or Not - Steam Game AI Recommendation

A gradio web application that analyzes Steam games and provides AI-powered recommendations on whether to play them or not.

## Features

- **Game Analysis**: Fetches game details (name, price, reviews) from Steam
- **AI Recommendations**: Uses LLM to analyze game reviews and provide suggestions
- **Multi-language Support**: Available in Simplified Chinese, Traditional Chinese and English

## Requirements

- python>=3.11

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Use .bat (Windows)

1. (First time) Clone this repository
2. (First time) Edit `configs/model_configs.json` to:
   - Add/remove AI models
   - Adjust model parameters
   - Configure API keys
   - More details: https://doc.agentscope.io/build_tutorial/monitor.html
3. (First time) Run `setup.bat`
4. Run `start.bat`
5. Open the Gradio interface in your browser (default: http://127.0.0.1:7860)
6. Enter a Steam game URL (e.g. `https://store.steampowered.com/app/...`)
7. Select your preferred language, AI model and other parameters
8. Click "Submit" to get AI recommendations

### 2. Manual

1. Clone this repository

2. Create & activate virtual environment (conda):

   ```bash
   conda create -n "my_env" python=3.11
   conda actiavte "my_env"
   ```

3. Install packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Edit `configs/model_configs.json`

5. Start WebUI:

   ```bash
   python web.py
   ```

6. Open the Gradio interface in your browser (default: http://127.0.0.1:7860)

7. Enter a Steam game URL (e.g. `https://store.steampowered.com/app/...`)

8. Select your preferred language, AI model and other parameters

9. Click "Submit" to get AI recommendations

## Supported LLM API

(More details: https://doc.agentscope.io/build_tutorial/model.html)

- OpenAI (and all OpenAI compatible models)
- DashScope
- Gemini
- Ollama
- Yi
- LiteLLM
- ZhipuAI
- Anthropic
