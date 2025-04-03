import requests
from bs4 import BeautifulSoup
import json
import time
        

# 配置请求头模拟浏览器
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': "wants_mature_content=1;lastagecheckage=1-0-1900; path=/;birthtime=-2211667760; path=/"
}
MAX_RETRIES = 3
BASE_DELAY = 1  # seconds

def get_app_id(url):
    """从商店URL提取appid"""
    return url.split('/')[4]

def parse_game_info(html):
    """解析基础游戏信息"""
    soup = BeautifulSoup(html, 'lxml')
    
    name_elem = soup.find('div', {'class': 'apphub_AppName'})
    price_elem = soup.find('div', {'class': 'game_purchase_price price'})
    if not price_elem:
        price_elem = soup.find('div', {'class': 'discount_final_price'})
    game_review_summary_recent = soup.find('span', {'class': 'game_review_summary'})
    game_review_summary_all = soup.find('span', {'class': 'game_review_summary','itemprop':'description'})
    data = {
        'name': name_elem.text.strip() if name_elem else '未知',
        'price': price_elem.text.strip() if price_elem else '未知',
        'game_review_summary_recent': game_review_summary_recent.text.strip() if game_review_summary_recent else '未知',
        'game_review_summary_all': game_review_summary_all.text.strip() if game_review_summary_all else '未知'
    }
    return data

def get_reviews(appid, review_type='positive', pages=5, count=10, language='schinese', day_range=365):
    """获取指定类型评论"""
    reviews = []
    cursor = '*'
    p = 0
    
    while p < pages:
        params = {
            'json': 1,
            'filter': 'all',
            'language': language,
            'day_range': day_range,
            'review_type': review_type,
            'purchase_type': 'all',
            'cursor': cursor,
            'num_per_page': 100
        }
        
        url = f'https://store.steampowered.com/appreviews/{appid}'
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    url,
                    params=params,
                    headers=HEADERS,
                    timeout=30,
                    stream=True  # Handle large responses better
                )
                response.raise_for_status()  # Raises HTTPError for bad responses
                
                # Read content with error handling
                try:
                    content = response.content.decode('utf-8')
                    result = json.loads(content)
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(BASE_DELAY * (attempt + 1))
                        continue
                    raise
                
                if result['success'] != 1:
                    break
                    
                break  # Success - exit retry loop
                
            except (requests.exceptions.RequestException, 
                   requests.exceptions.ChunkedEncodingError,
                   requests.exceptions.IncompleteRead) as e:
                if attempt == MAX_RETRIES - 1:
                    print(f"Failed to get reviews after {MAX_RETRIES} attempts: {str(e)}")
                    return reviews[:count]  # Return whatever we have
                time.sleep(BASE_DELAY * (attempt + 1))
            
        for review in result['reviews']:
            reviews.append({
                'content': review['review'],
                'hours_played': review['author']['playtime_forever']/100,
                'votes_up': review['votes_up'],
                'timestamp': review['timestamp_updated']
            })
        cursor = result['cursor']
        p +=1
        time.sleep(1)  # 请求间隔
        
    # 按votes_up降序排序
    reviews.sort(key=lambda x: x['votes_up'], reverse=True)
    return reviews[:count]       

def get_game_data(target_url:str,
                  language:str = 'schinese',
                  top_n:int = 10,
                  max_pages:int = 5,
                  day_range:int = 365) -> dict:
    # 获取基础信息
    response = requests.get(target_url, headers=HEADERS)
    appid = get_app_id(target_url)
    game_data = parse_game_info(response.text)
    
    # 获取评论
    game_data['positive_reviews'] = get_reviews(appid, 'positive',pages=max_pages,count=top_n,language=language,day_range=day_range)
    game_data['negative_reviews'] = get_reviews(appid, 'negative',pages=max_pages,count=top_n,language=language,day_range=day_range)
    game_data['top_n'] = top_n
    return game_data
