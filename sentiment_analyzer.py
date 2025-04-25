import pandas as pd
import requests
import os
import time
from config import ANALYZER_CONFIG, ERROR_MESSAGES

class SentimentAnalyzer:
    def __init__(self):
        self.config = ANALYZER_CONFIG
        self.api_key = None
        self.progress_callback = None
        self.is_running = True
        self.current_index = 0
        self.last_file = None
    
    def set_api_key(self, api_key):
        """设置API密钥"""
        self.api_key = api_key
        
    def resume(self):
        """继续分析"""
        self.is_running = True
        if self.last_file and os.path.exists(self.last_file):
            return self.analyze_comments(self.last_file, start_from=self.current_index)
        return None
        
    def stop(self):
        """停止分析"""
        self.is_running = False
        
    def analyze_comments(self, comments_file, start_from=0):
        """分析评论"""
        try:
            if not self.api_key:
                raise ValueError(ERROR_MESSAGES['no_api_key'])
                
            self.last_file = comments_file
            df = pd.read_csv(comments_file)
            results = []
            total = len(df)
            
            # 从指定位置继续分析
            for idx in range(start_from, len(df)):
                if not self.is_running:
                    self.current_index = idx  # 保存当前位置
                    # 保存已分析的结果
                    if results:
                        return self._save_partial_results(results)
                    break
                    
                row = df.iloc[idx]
                try:
                    sentiment = self._analyze_text(row['content'])
                    results.append({
                        'comment_id': row['comment_id'],
                        'content': row['content'],
                        'created_at': row['created_at'],
                        'user_name': row['user_name'],
                        'like_count': row['like_count'],
                        'sentiment': sentiment
                    })
                    
                    if self.progress_callback:
                        progress = (idx + 1) / total * 100
                        self.progress_callback(progress)
                        
                    time.sleep(0.5)  # 避免请求过快
                    
                except Exception as e:
                    print(f"单条评论分析失败: {str(e)}")
                    results.append({
                        'comment_id': row['comment_id'],
                        'content': row['content'],
                        'created_at': row['created_at'],
                        'user_name': row['user_name'],
                        'like_count': row['like_count'],
                        'sentiment': 1  # 出错时设为中性
                    })
            
            # 保存完整结果
            if results:
                return self._save_results(results)
                
        except Exception as e:
            print(f"分析失败: {str(e)}")
            return None
            
    def _save_partial_results(self, results):
        """保存部分分析结果"""
        try:
            if not os.path.exists(self.config['output_dir']):
                os.makedirs(self.config['output_dir'])
                
            output_file = os.path.join(
                self.config['output_dir'],
                f'analyzed_partial_{int(time.time())}.csv'
            )
            
            df_result = pd.DataFrame(results)
            df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
            return output_file
            
        except Exception as e:
            print(f"保存部分结果失败: {str(e)}")
            return None
            
    def _analyze_text(self, text):
        """调用DeepSeek API进行情感分析"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [{
                    'role': 'user',
                    'content': f'请分析下面这段文字的情感倾向(0表示积极,1表示中性,2表示消极),只需要返回数字:\n{text}'
                }]
            }
            
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers=headers,
                json=data
            )
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            sentiment = int(content) if content in ['0', '1', '2'] else 1
            return sentiment
            
        except Exception as e:
            print(f"API调用失败: {str(e)}")
            return 1  # 出错时返回中性
    
    def _save_results(self, results):
        """保存完整分析结果"""
        try:
            if not os.path.exists(self.config['output_dir']):
                os.makedirs(self.config['output_dir'])
                
            output_file = os.path.join(
                self.config['output_dir'],
                f'analyzed_{int(time.time())}.csv'
            )
            
            df_result = pd.DataFrame(results)
            df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
            return output_file
            
        except Exception as e:
            print(f"保存分析结果失败: {str(e)}")
            return None