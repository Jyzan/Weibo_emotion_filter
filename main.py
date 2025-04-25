import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog  # 合并导入
import threading
import pandas as pd
from PIL import Image, ImageTk
from weibo_crawler import WeiboCrawler
from sentiment_analyzer import SentimentAnalyzer
from chart_maker import ChartMaker
from config import UI_CONFIG, ERROR_MESSAGES  # 确保从config导入

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("微博评论分析工具")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 600)
        
        # 实例化各个模块的类
        self.crawler = WeiboCrawler()
        self.analyzer = SentimentAnalyzer()
        self.chart_maker = ChartMaker()
        
        # 初始化状态变量
        self.is_crawling = False
        self.is_analyzing = False
        self.last_crawl_file = None    # 添加这行
        self.last_analysis_file = None # 添加这行
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 修改PanedWindow的设置
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧面板 - 固定最小宽度
        left_frame = ttk.Frame(self.paned_window, width=600)  # 减小最小宽度
        left_frame.pack_propagate(False)  # 防止自动收缩
        self.paned_window.add(left_frame, weight=1)
        
        # 右侧面板 - 增加初始宽度
        right_frame = ttk.Frame(self.paned_window, width=600)  # 增加初始宽度
        right_frame.pack_propagate(False)  # 防止自动收缩
        self.paned_window.add(right_frame, weight=1)

        # 配置区域（在左侧面板中）
        config_frame = ttk.LabelFrame(left_frame, text="配置信息")
        config_frame.pack(fill=tk.X, pady=5)
        
        # URL输入(改为Text控件并添加水平滚动条)
        ttk.Label(config_frame, text="URL:").grid(row=0, column=0, padx=5, pady=2, sticky='ne')
        url_frame = ttk.Frame(config_frame)  # 创建框架来容纳文本框和滚动条
        url_frame.grid(row=0, column=1, columnspan=4, sticky='ew')
        
        self.url_text = tk.Text(url_frame, height=1, width=120)
        self.url_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        url_scrollbar = ttk.Scrollbar(url_frame, orient="horizontal", command=self.url_text.xview)
        url_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.url_text.configure(xscrollcommand=url_scrollbar.set, wrap=tk.NONE)
        
        # User-Agent输入
        ttk.Label(config_frame, text="User-Agent:").grid(row=1, column=0, padx=5, pady=2, sticky='ne')
        self.user_agent_text = tk.Text(config_frame, height=2, width=120)
        self.user_agent_text.grid(row=1, column=1, columnspan=4, padx=5, pady=2, sticky='ew')
        
        ua_scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=self.user_agent_text.yview)
        ua_scrollbar.grid(row=1, column=5, sticky='ns')
        self.user_agent_text.configure(yscrollcommand=ua_scrollbar.set)
        
        # Referer输入(改为Text控件并添加水平滚动条)
        ttk.Label(config_frame, text="Referer:").grid(row=2, column=0, padx=5, pady=2, sticky='ne')
        referer_frame = ttk.Frame(config_frame)
        referer_frame.grid(row=2, column=1, columnspan=4, sticky='ew')

        self.referer_text = tk.Text(referer_frame, height=1, width=120)
        self.referer_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        referer_scrollbar = ttk.Scrollbar(referer_frame, orient="horizontal", command=self.referer_text.xview)
        referer_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.referer_text.configure(xscrollcommand=referer_scrollbar.set, wrap=tk.NONE)
        
        # Cookie输入
        ttk.Label(config_frame, text="Cookie:").grid(row=3, column=0, padx=5, pady=2, sticky='ne')
        self.cookie_text = tk.Text(config_frame, height=5, width=120)
        self.cookie_text.grid(row=3, column=1, columnspan=4, padx=5, pady=2, sticky='ew')
        
        cookie_scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=self.cookie_text.yview)
        cookie_scrollbar.grid(row=3, column=5, sticky='ns')
        self.cookie_text.configure(yscrollcommand=cookie_scrollbar.set)
        
        # API Key输入
        ttk.Label(config_frame, text="API Key:").grid(row=4, column=0, padx=5, pady=2, sticky='e')
        self.api_key_entry = ttk.Entry(config_frame, width=80)
        self.api_key_entry.grid(row=4, column=1, columnspan=4, padx=5, pady=2, sticky='ew')
        
        # 配置区域列宽设置
        config_frame.grid_columnconfigure(1, weight=1)  # 让输入框区域可以自适应宽度
        
        # 控制按钮区域
        control_frame = ttk.LabelFrame(left_frame, text="控制面板")
        control_frame.pack(fill=tk.X, pady=5)
        
        # 所有按钮放在一行
        ttk.Button(control_frame, text="开始爬取", command=self.start_crawl).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="停止爬取", command=self.stop_crawl).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="继续爬取", command=self.resume_crawl).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="开始分析", command=self.start_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="停止分析", command=self.stop_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="继续分析", command=self.resume_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="积极评论", command=lambda: self.filter_comments(0)).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="中性评论", command=lambda: self.filter_comments(1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="消极评论", command=lambda: self.filter_comments(2)).pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(left_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # 评论展示区域
        comment_frame = ttk.LabelFrame(left_frame, text="评论展示")
        comment_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = tk.Text(comment_frame, wrap=tk.WORD)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        text_scrollbar = ttk.Scrollbar(comment_frame, orient="vertical", command=self.result_text.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=text_scrollbar.set)

        # 右侧可视化控制区域
        visual_control_frame = ttk.Frame(right_frame)
        visual_control_frame.pack(fill=tk.X, pady=5)
        
        # 添加按钮到右侧控制区域
        ttk.Button(visual_control_frame, text="生成统计饼图", command=self.generate_pie_chart).pack(side=tk.LEFT, padx=5)
        ttk.Button(visual_control_frame, text="生成词云图", command=self.generate_wordcloud).pack(side=tk.LEFT, padx=5)
        ttk.Button(visual_control_frame, text="清空图表", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # 右侧面板中添加垂直PanedWindow
        right_paned = ttk.PanedWindow(right_frame, orient=tk.VERTICAL)
        right_paned.pack(fill=tk.BOTH, expand=True)
        
        # 上方饼图展示区域
        pie_frame = ttk.LabelFrame(right_paned, text="情感分布饼图")
        right_paned.add(pie_frame, weight=1)
        
        self.pie_label = ttk.Label(pie_frame)
        self.pie_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)  # 减小边距
        
        # 下方词云图展示区域
        wordcloud_frame = ttk.LabelFrame(right_paned, text="评论词云图")
        right_paned.add(wordcloud_frame, weight=1)
        
        self.wordcloud_label = ttk.Label(wordcloud_frame)
        self.wordcloud_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)  # 减小边距

        # 添加默认值提示 - 删除 user-agent 的默认值
        # default_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        # self.user_agent_text.insert("1.0", default_ua)
        
        # 在URL输入框不添加提示文字
        # url_placeholder = "请输入微博评论页面URL"
        # self.url_text.insert("1.0", url_placeholder)
        # self.url_text.bind("<FocusIn>", lambda e: self.clear_placeholder(self.url_text, url_placeholder))
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 绑定大小变化事件
        self.pie_label.bind('<Configure>', self._update_pie_display)
        self.wordcloud_label.bind('<Configure>', self._update_wordcloud_display)
        
    # 添加清除占位符的方法
    def clear_placeholder(self, widget, placeholder):
        if widget.get("1.0", "end-1c") == placeholder:
            widget.delete("1.0", tk.END)

    def start_crawl(self):
        """开始爬取"""
        if not self.is_crawling:
            try:
                # 获取输入值
                url = self.url_text.get("1.0", tk.END).strip()
                user_agent = self.user_agent_text.get("1.0", tk.END).strip()
                referer = self.referer_text.get("1.0", tk.END).strip()  # 修改这里
                cookie = self.cookie_text.get("1.0", tk.END).strip()
                
                if not url:
                    messagebox.showerror("错误", "请输入URL")
                    return
                
                if not all([user_agent, referer, cookie]):  # 检查所有必填项
                    messagebox.showerror("错误", "请填写完整的爬取参数")
                    return
                
                # 设置爬虫参数
                self.crawler.set_headers(
                    user_agent=user_agent,  # 使用输入的user-agent
                    cookie=cookie,
                    referer=referer
                )
                
                self.is_crawling = True
                threading.Thread(target=self._crawl_thread).start()
                
            except Exception as e:
                messagebox.showerror("错误", str(e))

    def stop_crawl(self):
        """停止爬取"""
        if self.is_crawling:
            self.crawler.stop()
            self.is_crawling = False
            self.update_status("爬取已停止")

    def resume_crawl(self):
        """继续爬取"""
        if not self.is_crawling:
            if hasattr(self.crawler, 'url'):
                self.is_crawling = True
                threading.Thread(target=self._resume_crawl_thread).start()
            else:
                self.show_message("错误", "没有可继续的爬取任务")

    def _resume_crawl_thread(self):
        """继续爬取线程"""
        try:
            self.update_status("继续爬取评论...")
            output_file = self.crawler.resume()
            if output_file:
                self.last_crawl_file = output_file
                self.show_message("完成", f"评论已保存至: {output_file}")
                
                # 显示评论内容
                df = pd.read_csv(output_file)
                self.result_text.delete(1.0, tk.END)
                for _, row in df.iterrows():
                    self.result_text.insert(tk.END, f"{row['content']}\n")
                
                self.update_status("爬取完成")
        except Exception as e:
            self.show_message("错误", str(e))
            self.update_status("爬取失败")
        finally:
            self.is_crawling = False

    def start_analysis(self):
        """开始分析"""
        if not self.is_analyzing:
            if not hasattr(self, 'last_crawl_file'):
                self.show_message("错误", "请先爬取评论")
                return
                
            self.is_analyzing = True
            threading.Thread(target=self._analysis_thread).start()

    def stop_analysis(self):
        """停止分析"""
        if self.is_analyzing:
            self.analyzer.stop()
            self.is_analyzing = False
            self.update_status("分析已停止")

    def resume_analysis(self):
        """继续分析"""
        if not self.is_analyzing:
            try:
                # 设置API key
                api_key = self.api_key_entry.get().strip()
                if not api_key:
                    self.show_message("错误", "请输入API Key")
                    return
                
                self.analyzer.set_api_key(api_key)
                self.is_analyzing = True
                threading.Thread(target=self._analysis_thread).start()
                
            except Exception as e:
                self.show_message("错误", str(e))
                self.is_analyzing = False

    def generate_pie_chart(self):
        """生成饼图"""
        try:
            chart_file = self.chart_maker.create_pie_chart(self.last_analysis_file)
            if chart_file:
                self.root.update()
                frame_width = self.pie_label.winfo_width()
                frame_height = self.pie_label.winfo_height()
                
                if frame_width > 0 and frame_height > 0:
                    self.current_pie_file = chart_file  # 保存当前文件路径
                    self._update_pie_display()  # 更新显示
                    self.update_status("饼图生成完成")
                    
        except Exception as e:
            print(f"生成饼图错误: {str(e)}")
            self.show_message("错误", str(e))
            self.update_status("饼图生成失败")

    def generate_wordcloud(self):
        """生成词云图"""
        try:
            chart_file = self.chart_maker.create_wordcloud(self.last_analysis_file)
            if chart_file:
                self.root.update()
                frame_width = self.wordcloud_label.winfo_width()
                frame_height = self.wordcloud_label.winfo_height()
                
                if frame_width > 0 and frame_height > 0:
                    self.current_wordcloud_file = chart_file  # 保存当前文件路径
                    self._update_wordcloud_display()  # 更新显示
                    self.update_status("词云图生成完成")
                    
        except Exception as e:
            print(f"生成词云图错误: {str(e)}")
            self.show_message("错误", str(e))
            self.update_status("词云图生成失败")

    def _update_pie_display(self, event=None):
        """更新饼图显示"""
        if hasattr(self, 'current_pie_file'):
            try:
                frame_width = self.pie_label.winfo_width()
                frame_height = self.pie_label.winfo_height()
                
                if frame_width > 0 and frame_height > 0:
                    image = Image.open(self.current_pie_file)
                    image = image.resize((frame_width, frame_height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.pie_label.configure(image=photo)
                    self.pie_label.image = photo
                    
            except Exception as e:
                print(f"更新饼图显示错误: {str(e)}")

    def _update_wordcloud_display(self, event=None):
        """更新词云图显示"""
        if hasattr(self, 'current_wordcloud_file'):
            try:
                frame_width = self.wordcloud_label.winfo_width()
                frame_height = self.wordcloud_label.winfo_height()
                
                if frame_width > 0 and frame_height > 0:
                    image = Image.open(self.current_wordcloud_file)
                    image = image.resize((frame_width, frame_height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.wordcloud_label.configure(image=photo)
                    self.wordcloud_label.image = photo
                    
            except Exception as e:
                print(f"更新词云图显示错误: {str(e)}")

    def clear_all(self):
        """清空所有显示"""
        self.result_text.delete(1.0, tk.END)
        self.pie_label.configure(image='')
        self.wordcloud_label.configure(image='')

    def filter_comments(self, sentiment):
        """筛选评论"""
        try:
            if not hasattr(self, 'last_analysis_file'):
                if hasattr(self, 'last_crawl_file'):
                    if messagebox.askyesno("提示", "需要先进行情感分析，是否立即分析？"):
                        self.start_analysis()
                        return
                else:
                    self.show_message("错误", "请先爬取评论")
                return
                
            self.update_status(f"正在筛选{self.chart_maker.labels[sentiment]}评论...")
            df = pd.read_csv(self.last_analysis_file)
            filtered = df[df['sentiment'] == sentiment]
            
            self.result_text.delete(1.0, tk.END)
            if len(filtered) > 0:
                for _, row in filtered.iterrows():
                    comment_info = (
                        f"用户: {row['user_name']}\n"
                        f"时间: {row['created_at']}\n"
                        f"点赞: {row['like_count']}\n"
                        f"内容: {row['content']}\n"
                        f"{'-'*50}\n"
                    )
                    self.result_text.insert(tk.END, comment_info)
                self.update_status(f"已显示{len(filtered)}条{self.chart_maker.labels[sentiment]}评论")
            else:
                self.result_text.insert(tk.END, f"没有找到{self.chart_maker.labels[sentiment]}评论")
            
        except Exception as e:
            self.show_message("错误", str(e))
            self.update_status("筛选失败")

    def _crawl_thread(self):
        """爬虫线程"""
        try:
            # 更新状态
            self.update_status("正在爬取评论...")
            
            # 清空显示
            self.result_text.delete(1.0, tk.END)
            self.progress_var.set(0)
            
            url = self.url_text.get("1.0", tk.END).strip()
            
            # 定义进度回调
            def progress_callback(count):
                self.result_text.insert(tk.END, f"已爬取 {count} 条评论\n")
                self.result_text.see(tk.END)
                self.progress_var.set(min(count, 100))
                self.root.update()
                
            self.crawler.progress_callback = progress_callback
            
            # 开始爬取
            output_file = self.crawler.crawl_comments(url)
            if output_file:
                self.last_crawl_file = output_file
                self.show_message("完成", f"评论已保存至: {output_file}")
                
                # 显示评论内容(增加更多信息)
                df = pd.read_csv(output_file)
                self.result_text.delete(1.0, tk.END)
                for _, row in df.iterrows():
                    comment_info = (
                        f"用户: {row['user_name']}\n"
                        f"时间: {row['created_at']}\n"
                        f"点赞: {row['like_count']}\n"
                        f"内容: {row['content']}\n"
                        f"{'-'*50}\n"
                    )
                    self.result_text.insert(tk.END, comment_info)
                
                self.update_status("爬取完成")
                
        except Exception as e:
            print(f"爬取错误: {str(e)}")  # 添加错误日志
            self.show_message("错误", str(e))
            self.update_status("爬取失败")
        finally:
            self.is_crawling = False

    def _analysis_thread(self):
        """分析线程"""
        try:
            if not hasattr(self, 'last_crawl_file'):
                self.show_message("错误", "请先爬取评论")
                return
                
            self.update_status("正在进行情感分析...")
            self.analyzer.is_running = True  # 重置运行状态
            
            api_key = self.api_key_entry.get().strip()
            if not api_key:
                self.show_message("错误", "请输入API Key")
                return
                
            # 设置API key
            self.analyzer.set_api_key(api_key)
            
            # 清空显示
            self.result_text.delete(1.0, tk.END)
            self.progress_var.set(0)
            
            # 定义进度回调
            def progress_callback(progress):
                if not self.is_analyzing:  # 检查是否已停止
                    raise Exception("分析已停止")
                self.progress_var.set(progress)
                self.result_text.insert(tk.END, f"分析进度: {progress:.1f}%\n")
                self.result_text.see(tk.END)
                self.root.update()
                
            self.analyzer.progress_callback = progress_callback
            
            # 开始分析
            output_file = self.analyzer.analyze_comments(self.last_crawl_file)
            if output_file and os.path.exists(output_file):  # 确保文件存在
                self.last_analysis_file = output_file  # 保存分析结果文件路径
                print(f"分析结果文件保存在: {output_file}")  # 调试输出
                
                # 显示分析结果
                df = pd.read_csv(output_file)
                self.result_text.delete(1.0, tk.END)
                
                # 统计各类情感数量
                sentiment_counts = df['sentiment'].value_counts()
                total = len(df)
                
                # 显示统计信息
                self.result_text.insert(tk.END, "情感分析结果统计：\n")
                self.result_text.insert(tk.END, "=" * 30 + "\n")
                for sentiment, count in sentiment_counts.items():
                    percentage = count / total * 100
                    label = self.chart_maker.labels[sentiment]
                    self.result_text.insert(tk.END, f"{label}: {count}条 ({percentage:.1f}%)\n")
                self.result_text.insert(tk.END, "=" * 30 + "\n\n")
                
                # 显示详细结果
                for _, row in df.iterrows():
                    sentiment = self.chart_maker.labels[row['sentiment']]
                    comment_info = (
                        f"[{sentiment}]\n"
                        f"用户: {row['user_name']}\n"
                        f"时间: {row['created_at']}\n"
                        f"点赞: {row['like_count']}\n"
                        f"内容: {row['content']}\n"
                        f"{'-'*50}\n"
                    )
                    self.result_text.insert(tk.END, comment_info)
                    
                self.update_status("分析完成")
                self.show_message("完成", "情感分析已完成")
                
            else:
                raise Exception("分析结果文件生成失败")
                
        except Exception as e:
            print(f"分析错误: {str(e)}")  # 调试输出
            self.show_message("错误", str(e))
            self.update_status("分析失败")
        finally:
            self.is_analyzing = False

    def show_message(self, title, message):
        """显示消息对话框"""
        if title == "错误":
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

    def update_status(self, message):
        self.status_var.set(message)
        self.root.update()

def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        'data/raw_comments',
        'data/analyzed_comments',
        'charts'
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def main():
    try:
        ensure_directories()
        app = MainWindow()
        app.root.mainloop()
    except Exception as e:
        print(f"程序运行错误: {str(e)}")

if __name__ == "__main__":
    main()