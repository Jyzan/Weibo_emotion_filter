import os

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 微博爬虫配置
CRAWLER_CONFIG = {
    'output_dir': os.path.join(ROOT_DIR, 'data/raw_comments'),
    'headers': {
        'User-Agent': '',  # 移除默认值
        'Cookie': '',
        'Referer': ''
    },
    'sleep_time': 1.0
}

# DeepSeek API配置
ANALYZER_CONFIG = {
    'api_key': '',  # 运行时从UI获取
    'output_dir': os.path.join(ROOT_DIR, 'data/analyzed_comments')
}

# 可视化配置
CHART_CONFIG = {
    'charts_dir': os.path.join(ROOT_DIR, 'charts'),
    'chart_size': (640, 480),
    'colors': {
        'positive': '#2ecc71',
        'neutral': '#95a5a6',
        'negative': '#e74c3c'
    },
    'labels': {
        0: '积极',
        1: '中性', 
        2: '消极'
    }
}

# UI配置
UI_CONFIG = {
    'title': '微博评论分析工具',
    'window_size': '1400x800',
    'min_size': (1200, 600),
    'padding': 10,
    'font': ('SimHei', 9)  # 添加字体配置
}

# 错误消息配置
ERROR_MESSAGES = {
    'no_url': '请输入URL',
    'no_headers': '请填写完整的Headers信息',
    'no_api_key': '请输入API Key',
    'no_comments': '请先爬取评论',
    'no_analysis': '请先进行情感分析',
    'invalid_url': '无效的URL格式',
    'network_error': '网络连接错误',
    'api_error': 'API调用失败'
}

# 文件路径配置
FILE_PATHS = {
    'font': 'simhei.ttf',
    'raw_comments': 'data/raw_comments',
    'analyzed_comments': 'data/analyzed_comments',
    'charts': 'charts'
}