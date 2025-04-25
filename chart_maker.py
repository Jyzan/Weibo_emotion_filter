import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import jieba
import os
from matplotlib.font_manager import FontProperties

class ChartMaker:
    def __init__(self):
        # 固定的颜色映射
        self.colors = {
            'positive': '#3498db',  # 蓝色
            'neutral': '#95a5a6',   # 灰色
            'negative': '#e74c3c'   # 红色
        }
        self.labels = {
            0: '积极',
            1: '中性',
            2: '消极' 
        }
        # 使用系统自带的中文字体或尝试多个字体路径
        self.font = self._get_chinese_font()
        
    def _get_chinese_font(self):
        """获取可用的中文字体路径"""
        try:
            # Windows系统常见中文字体路径
            font_paths = [
                'C:/Windows/Fonts/simhei.ttf',  # 黑体
                'C:/Windows/Fonts/SIMYOU.TTF',  # 幼圆
                'C:/Windows/Fonts/simsun.ttc',  # 宋体
                'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
            ]
            
            # 返回第一个存在的字体路径
            for path in font_paths:
                if os.path.exists(path):
                    return path
                    
            raise Exception("未找到可用的中文字体")
            
        except Exception as e:
            print(f"加载中文字体失败: {str(e)}")
            return None
    
    def create_pie_chart(self, analyzed_file):
        """生成情感分布饼图"""
        try:
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            df = pd.read_csv(analyzed_file)
            total = len(df)
            
            # 按固定顺序统计情感
            sentiment_data = []
            sentiment_labels = []
            sentiment_colors = []
            
            for idx, label in self.labels.items():
                count = len(df[df['sentiment'] == idx])
                if count > 0:
                    sentiment_data.append(count)
                    sentiment_labels.append(label)
                    color = self.colors['positive' if idx == 0 else 'neutral' if idx == 1 else 'negative']
                    sentiment_colors.append(color)
            
            plt.figure(figsize=(8, 6))
            plt.pie(
                sentiment_data,
                labels=sentiment_labels,
                colors=sentiment_colors,
                autopct='%1.1f%%',
                shadow=True,
                textprops={'fontsize': 12, 'weight': 'bold'}  # 加大字体并加粗
            )
            plt.title('评论情感分布', fontsize=14, weight='bold', pad=20)  # 加大标题字体并加粗
            
            if not os.path.exists('charts'):
                os.makedirs('charts')
            output_file = 'charts/sentiment_pie.png'
            plt.savefig(output_file, bbox_inches='tight', dpi=300)
            plt.close()
            
            return output_file
            
        except Exception as e:
            print(f"生成饼图失败: {str(e)}")
            return None
            
    def create_wordcloud(self, analyzed_file, sentiment=None):
        """生成词云图"""
        try:
            # 获取字体路径
            font_path = self._get_chinese_font()
            if not font_path:
                raise Exception("未找到可用的中文字体")
            
            # 读取分析结果
            df = pd.read_csv(analyzed_file)
            if sentiment is not None:
                df = df[df['sentiment'] == sentiment]
            
            # 合并评论文本
            text = ' '.join(df['content'].astype(str))
            
            # 添加停用词
            stop_words = set(['了', '的', '是', '啊', '吗', '呢', '吧', '呀', '着', '啦', '么', 
                             '都', '就', '也', '要', '这', '那', '不', '还', '有', '和', '我',
                             '你', '他', '她', '它', '们', '个', '年', '月', '日'])
            
            # 分词并过滤
            words = []
            for word in jieba.cut(text):
                if len(word) > 1 and word not in stop_words:
                    words.append(word)
            
            text = ' '.join(words)
            
            # 生成词云
            wordcloud = WordCloud(
                font_path=font_path,
                width=800,
                height=400,
                background_color='white',
                max_words=100,
                collocations=False,
                colormap='viridis',
                min_font_size=10,
                max_font_size=80
            ).generate(text)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            
            title = '评论词云图'
            if sentiment is not None:
                title += f' - {self.labels[sentiment]}'
            plt.title(title, fontsize=14, weight='bold', pad=20)
            
            if not os.path.exists('charts'):
                os.makedirs('charts')
            output_file = f'charts/wordcloud{"_" + str(sentiment) if sentiment is not None else ""}.png'
            plt.savefig(output_file, bbox_inches='tight', dpi=300)
            plt.close()
            
            return output_file
            
        except Exception as e:
            print(f"生成词云图失败: {str(e)}")
            return None

    def save_sentiment_stats(self, analyzed_file):
        """保存情感分析统计结果
        
        Args:
            analyzed_file: 分析结果文件路径
        """
        try:
            # 读取分析结果
            df = pd.read_csv(analyzed_file)
            
            # 统计各情感数量及占比
            stats = df['sentiment'].value_counts()
            total = len(df)
            
            # 生成统计报告
            report = "情感分析统计报告\n"
            report += "=" * 20 + "\n"
            for sentiment, count in stats.items():
                percentage = count / total * 100
                report += f"{self.labels[sentiment]}: {count} 条 ({percentage:.1f}%)\n"
            report += "=" * 20 + "\n"
            
            # 保存报告
            if not os.path.exists('charts'):
                os.makedirs('charts')
            output_file = 'charts/sentiment_stats.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            return output_file, report
            
        except Exception as e:
            print(f"保存统计结果失败: {str(e)}")
            return None, None