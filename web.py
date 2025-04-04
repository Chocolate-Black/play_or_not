import gradio as gr
from workflow import play_or_not
from spider import get_game_data
import time
import json

def chat_fn(history, url, language, model_name, top_n, max_pages, time_range):
    print("get game data...")
    game_data = get_game_data(url, language, top_n, max_pages, time_range)
    print("print basic info...")
    
    
    if language == 'schinese':
        history.append(gr.ChatMessage(role="user",content=f"如何评价《{game_data['name']}》?"))
        basic_game_info = f"""
## 游戏基本信息

- 游戏名称：《{game_data['name']}》
- 当前价格：{game_data['price']}
- 近期评测：{game_data['game_review_summary_recent']}
- 全部评测：{game_data['game_review_summary_all']}\n
"""
    elif language == 'tchinese':
        history.append(gr.ChatMessage(role="user",content=f"如何評價《{game_data['name']}》?"))
        basic_game_info = f"""
## 遊戲基本信息

- 遊戲名稱：《{game_data['name']}》
- 當前價格：{game_data['price']}
- 近期測評：{game_data['game_review_summary_recent']}
- 全部測評：{game_data['game_review_summary_all']}\n
"""
    elif language == 'english':
        history.append(gr.ChatMessage(role="user",content=f"Please review *{game_data['name']}*."))
        basic_game_info = f"""
## Basic Game Information
        
- Game Name: *{game_data['name']}*
- Current Price: {game_data['price']}
- Recent Reviews: {game_data['game_review_summary_recent']}
- All Reviews: {game_data['game_review_summary_all']}\n
"""
    else:
        history.append(gr.ChatMessage(role="user",content=f"如何评价《{game_data['name']}》?"))
        basic_game_info = f"""
## 游戏基本信息

- 游戏名称：《{game_data['name']}》
- 当前价格：{game_data['price']}
- 近期评测：{game_data['game_review_summary_recent']}
- 全部评测：{game_data['game_review_summary_all']}\n
"""

    history.append(gr.ChatMessage(role="assistant",content=basic_game_info))
    
    print("generate suggestion...")
    suggestion = play_or_not(game_data=game_data,language=language,model_config_name=model_name)
    original_content = history[-1].content
    for _, chunk in enumerate(suggestion.stream):
        history[-1].content = original_content+suggestion.text
        time.sleep(0.05)
        yield history
    print("finish!")

def update_language(language):
    texts = get_text(language)
    config_names = get_config_names()
    return [
        gr.Markdown(f"## {texts['title']}"),
        gr.Markdown(texts["subtitle"]),
        gr.Textbox(
            label=texts["url_label"], 
            placeholder=texts["url_placeholder"]
        ),
        gr.Dropdown(
            label=texts["language_label"],
            choices=["schinese", "tchinese", "english"],
            value=language
        ),
        gr.Dropdown(
            label=texts["config_label"],
            choices=config_names,
            value=config_names[0]
        ),
        gr.Slider(
            label=texts["top_n_label"],
            minimum=1,
            maximum=50,
            step=1,
            value=10
        ),
        gr.Slider(
            label=texts["max_pages_label"],
            minimum=1,
            maximum=5,
            step=1,
            value=1
        ),
        gr.Radio(
            label=texts["time_range_label"],
            choices=texts["time_choices"],
            value=365
        ),
        texts["submit_text"],
        gr.Chatbot(
            value=[],
            type="messages",
            label=texts["chat_label"], 
            render_markdown=True
        )
    ]

def get_config_names():
    with open("configs/model_configs.json", "r", encoding="utf-8") as f:
        configs = json.load(f)
    return [config["config_name"] for config in configs]

def get_text(language):
    texts = {
        "schinese": {
            "title": "玩不玩",
            "subtitle": "输入Steam游戏链接，让AI给出建议",
            "url_label": "Steam游戏URL",
            "url_placeholder": "https://store.steampowered.com/app/...",
            "language_label": "语言",
            "config_label": "配置名称",
            "top_n_label": "前N条评论",
            "max_pages_label": "最大评论页数",
            "time_range_label": "时间范围",
            "time_choices": [
                ("1年", 365),
                ("6个月", 180),
                ("3个月", 90),
                ("1个月", 30)
            ],
            "submit_text": "提交",
            "chat_label": "向AI提问"
        },
        "tchinese": {
            "title": "玩不玩",
            "subtitle": "輸入Steam遊戲鏈接，讓AI給出建議",
            "url_label": "Steam遊戲URL",
            "url_placeholder": "https://store.steampowered.com/app/...",
            "language_label": "語言",
            "config_label": "配置名稱",
            "top_n_label": "前N條評論",
            "max_pages_label": "最大評論頁數",
            "time_range_label": "時間範圍",
            "time_choices": [
                ("1年", 365),
                ("6個月", 180),
                ("3個月", 90),
                ("1個月", 30)
            ],
            "submit_text": "提交",
            "chat_label": "向AI提問"
        },
        "english": {
            "title": "Play or Not",
            "subtitle": "Enter a Steam game link to get AI recommendations",
            "url_label": "Steam Game URL",
            "url_placeholder": "https://store.steampowered.com/app/...",
            "language_label": "Language",
            "config_label": "Config Name",
            "top_n_label": "Top N Reviews",
            "max_pages_label": "Max Review Pages",
            "time_range_label": "Time Range",
            "time_choices": [
                ("1 Year", 365),
                ("6 Months", 180),
                ("3 Months", 90),
                ("1 Month", 30)
            ],
            "submit_text": "Submit",
            "chat_label": "Ask for AI"
        }
    }
    return texts.get(language, texts["schinese"])

def create_web_interface():
    config_names = get_config_names()
    with gr.Blocks(
        title="Play or Not"
    ) as demo:
        # Get default language texts
        texts = get_text("schinese")
        
        title_md = gr.Markdown(f"## {texts['title']}")
        subtitle_md = gr.Markdown(texts["subtitle"])
        
        with gr.Row():
            with gr.Column(scale=3):
                url = gr.Textbox(
                    label=texts["url_label"], 
                    placeholder=texts["url_placeholder"]
                )
                language = gr.Dropdown(
                    label=texts["language_label"],
                    choices=["schinese", "tchinese", "english"],
                    value="schinese"
                )
                config_name = gr.Dropdown(
                    label=texts["config_label"],
                    choices=config_names,
                    value=config_names[0]
                )
                
                top_n = gr.Slider(
                    label=texts["top_n_label"],
                    minimum=1,
                    maximum=50,
                    step=1,
                    value=10
                )
                max_pages = gr.Slider(
                    label=texts["max_pages_label"],
                    minimum=1,
                    maximum=5,
                    step=1,
                    value=1
                )
                time_range = gr.Radio(
                    label=texts["time_range_label"],
                    choices=texts["time_choices"],
                    value=365
                )
                
                submit_button = gr.Button(value=texts["submit_text"])
                
            with gr.Column(scale=7):
                chatbot = gr.Chatbot(
                    value=[],
                    type="messages",
                    label=texts["chat_label"], 
                    render_markdown=True
                )
                clear = gr.ClearButton([chatbot])
        
        # Language change event
        language.change(
            fn=update_language,
            inputs=[language],
            outputs=[
                title_md,  # title
                subtitle_md,  # subtitle
                url,  # url
                language,
                config_name,  # config label
                top_n,  # top_n label
                max_pages,  # max_pages label
                time_range,  # time_range label
                submit_button,  # submit text
                chatbot  # chatbot
            ]
        )
        
        submit_button.click(
            fn=chat_fn,
            inputs=[chatbot, url, language, config_name, top_n, max_pages, time_range],
            outputs=chatbot
        )
    
    return demo
            
if __name__ == '__main__':
    demo = create_web_interface()
    demo.launch()
