import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
from typing import Optional, Union, Sequence
from spider import get_game_data

agentscope.init(
    model_configs="./configs/model_configs.json", 
)

class StreamDialogAgent(DialogAgent):
    def reply_in_stream(self,x: Optional[Union[Msg, Sequence[Msg]]] = None):
        if self.memory:
            self.memory.add(x)

        # prepare prompt
        prompt = self.model.format(
            Msg(
                "system",
                self.sys_prompt,
                role="system",
            )
            if self.sys_prompt
            else None,
            self.memory
            and self.memory.get_memory()
            or x,  # type: ignore[arg-type]
        )

        # call llm and generate response
        response = self.model(prompt)
        return response

def steam_recommendation_prompt(game_data:dict,top_n:int,language:str) ->str:
    prompt = f"""
    请根据以下内容，分析总结{game_data['name']}的优点和缺点，并告诉我是否推荐我游玩这款游戏:\n
    游戏名称：{game_data['name']}\n
    价格：{game_data['price']}\n
    近期风评：{game_data['game_review_summary_recent']}\n
    全部风评：{game_data['game_review_summary_all']}\n
    近期最有价值的前{top_n}条好评：\n
    """
    for idx, review in enumerate(game_data['positive_reviews'], 1):
        prompt += f"好评{idx}：[{review['hours_played']}小时] [投票数：{review['votes_up']}] {review['content']}\n"
    
    prompt += f'近期最有价值的前{top_n}条差评：\n'

    for idx, review in enumerate(game_data['negative_reviews'], 1):
        prompt += f"差评{idx}：[{review['hours_played']}小时] [投票数：{review['votes_up']}] {review['content']}\n"
        
    if language == 'schinese':
        prompt += "请用简体中文进行回复。"
    elif language == 'tchinese':
        prompt += "请用繁体中文进行回复。"
    elif language == 'english':
        prompt += "请用英文进行回复。"
    else:
        prompt += "请用简体中文进行回复。"
        
    return prompt

def play_or_not(game_data:dict,
                language:str,
                model_config_name:str):
    steam_analyzer = StreamDialogAgent(
        name = "SteamGameAnalyzer",
        model_config_name = model_config_name,
        sys_prompt="你是一个专业的游戏评测编辑。",
        use_memory=False
    )
    
    msg = Msg(name="User",content=steam_recommendation_prompt(game_data,game_data['top_n'],language=language),role='user')
    suggestion = steam_analyzer.reply_in_stream(msg)
    
    return suggestion