# 微博评论情感分析工具

## 项目简介
这是一个基于 Python 的微博评论分析工具，可以爬取微博评论并进行情感分析，生成可视化图表。主要功能包括评论爬取、情感分类、数据可视化等，帮助用户快速了解评论的情感倾向分布。

## 主要特性
- 💬 支持微博评论的批量爬取
- 🤖 基于 DeepSeek API 的情感分析
- 📊 直观的数据可视化展示（饼图、词云图）
- 🔄 支持暂停/继续爬取和分析
- 📱 友好的图形用户界面
- 🎨 可拖拽调整的界面布局

## 技术栈
- Python 3.8+
- Tkinter (GUI)
- Requests (网络请求)
- Pandas (数据处理)
- Matplotlib (数据可视化)
- WordCloud (词云生成)
- PIL (图像处理)

## 安装说明
1. 克隆仓库
```bash
git clone https://github.com/Jyzan/Weibo_emotion_filter.git
cd Weibo_emotion_filter
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用说明
1. 启动程序
```bash
python main.py
```

2. 配置参数
   - 输入微博评论页面 URL
   - 填写必要的网络请求参数（User-Agent、Cookie、Referer）
   - 输入 DeepSeek API Key

3. 功能操作
   - 点击"开始爬取"进行评论获取
   - 点击"开始分析"进行情感分析
   - 点击"生成统计饼图"查看情感分布
   - 点击"生成词云图"查看高频词汇
   - 可随时暂停/继续操作

## 项目结构
```
team-comment-analyzer/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── weibo_crawler.py     # 评论爬虫模块
├── sentiment_analyzer.py # 情感分析模块
├── chart_maker.py       # 图表生成模块
├── data/               # 数据存储目录
│   ├── raw_comments/   # 原始评论
│   └── analyzed/       # 分析结果
└── charts/             # 图表输出目录
```

## 界面预览
- 支持左右拖拽调整布局
- 评论区与图表区域自适应
- 实时显示处理进度
- 支持查看不同情感类型的评论

## 注意事项
1. 使用前请确保：
   - 已安装所有依赖包
   - 有效的 DeepSeek API Key
   - 正确的网页请求参数

2. 性能建议：
   - 评论数量较大时，请耐心等待
   - 可以随时暂停/继续操作
   - 建议定期清理临时文件

## 开发计划
- [ ] 支持更多数据源
- [ ] 添加更多可视化图表
- [ ] 优化分析算法
- [ ] 支持导出分析报告
- [ ] 添加批量处理功能

## 贡献指南
欢迎提交 Issues 和 Pull Requests！

## 许可证
本项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。

## 联系方式
如有问题或建议，请通过 Issues 与我们联系。

## 致谢
感谢所有为本项目做出贡献的开发者！
