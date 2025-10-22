import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import pygame
import threading
import time
import json
from modules.local_music_manager import LocalMusicManager
from modules.online_music_manager import OnlineMusicManager

class MusicPlayer:
    def __init__(self, root):
        # 初始化主窗口
        self.root = root
        self.root.title("音乐播放器")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        # 初始化pygame混音器
        pygame.mixer.init()
        
        # 初始化音乐管理器
        self.local_music_manager = LocalMusicManager()
        self.online_music_manager = OnlineMusicManager()
        
        # 当前播放状态
        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0
        self.is_repeat = False
        self.is_shuffle = False
        self.playlist = []
        
        # 加载配置
        self.config = self.load_config()
        
        # 创建UI界面
        self.create_ui()
        
        # 创建播放进度条更新线程
        self.update_thread = None
        self.stop_thread = False
        
        # 扫描默认音乐文件夹
        if 'default_music_folder' in self.config:
            self.scan_music_folder(self.config['default_music_folder'])
    
    def load_config(self):
        """加载配置文件"""
        config_file = "config.json"
        default_config = {
            'default_music_folder': os.path.expanduser("~") + "\Music",
            'download_folder': os.path.expanduser("~") + "\Music\Downloads",
            'volume': 0.7
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置和用户配置
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except:
                return default_config
        else:
            # 创建默认下载文件夹
            os.makedirs(default_config['download_folder'], exist_ok=True)
            return default_config
    
    def save_config(self):
        """保存配置文件"""
        with open("config.json", 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
    
    def create_ui(self):
        """创建用户界面"""
        # 创建选项卡控件
        tab_control = ttk.Notebook(self.root)
        tab_control.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建本地音乐选项卡
        self.local_tab = ttk.Frame(tab_control)
        tab_control.add(self.local_tab, text="本地音乐")
        
        # 创建在线音乐选项卡
        self.online_tab = ttk.Frame(tab_control)
        tab_control.add(self.online_tab, text="在线音乐")
        
        # 创建本地音乐界面
        self.create_local_music_ui()
        
        # 创建在线音乐界面
        self.create_online_music_ui()
        
        # 创建底部控制栏
        self.create_control_bar()
    
    def create_local_music_ui(self):
        """创建本地音乐界面"""
        # 创建文件夹选择按钮
        folder_frame = ttk.Frame(self.local_tab)
        folder_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(folder_frame, text="选择音乐文件夹", command=self.select_music_folder).pack(side="left", padx=5)
        
        # 创建音乐列表
        list_frame = ttk.Frame(self.local_tab)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        # 创建列表视图
        self.song_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, width=100, height=20, font=("SimHei", 10))
        self.song_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.song_listbox.yview)
        
        # 绑定双击事件
        self.song_listbox.bind("<Double-1>", self.play_selected_song)
    
    def create_online_music_ui(self):
        """创建在线音乐界面"""
        # 创建搜索框
        search_frame = ttk.Frame(self.online_tab)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        self.search_entry = ttk.Entry(search_frame, font=("SimHei", 12))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        ttk.Button(search_frame, text="搜索", command=self.search_online_music).pack(side="left", padx=5)
        
        # 创建搜索结果列表
        result_frame = ttk.Frame(self.online_tab)
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side="right", fill="y")
        
        # 创建列表视图
        self.online_listbox = tk.Listbox(result_frame, yscrollcommand=scrollbar.set, width=100, height=15, font=("SimHei", 10))
        self.online_listbox.pack(fill="both", expand=True, side="left")
        scrollbar.config(command=self.online_listbox.yview)
        
        # 创建下载按钮
        ttk.Button(self.online_tab, text="下载选中音乐", command=self.download_selected_music).pack(pady=5)
    
    def create_control_bar(self):
        """创建底部控制栏"""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        # 音量控制
        volume_frame = ttk.Frame(control_frame)
        volume_frame.pack(side="right", padx=10)
        
        ttk.Label(volume_frame, text="音量").pack(side="left")
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=1, orient="horizontal", length=100, command=self.set_volume)
        self.volume_scale.set(self.config['volume'])
        self.volume_scale.pack(side="left", padx=5)
        
        # 播放控制按钮
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side="left")
        
        # 重复按钮
        self.repeat_var = tk.BooleanVar(value=self.is_repeat)
        ttk.Checkbutton(button_frame, text="重复", variable=self.repeat_var, command=self.toggle_repeat).pack(side="left", padx=5)
        
        # 随机播放按钮
        self.shuffle_var = tk.BooleanVar(value=self.is_shuffle)
        ttk.Checkbutton(button_frame, text="随机", variable=self.shuffle_var, command=self.toggle_shuffle).pack(side="left", padx=5)
        
        # 上一曲
        ttk.Button(button_frame, text="上一曲", command=self.play_previous).pack(side="left", padx=5)
        
        # 播放/暂停
        self.play_button = ttk.Button(button_frame, text="播放", command=self.toggle_play_pause)
        self.play_button.pack(side="left", padx=5)
        
        # 下一曲
        ttk.Button(button_frame, text="下一曲", command=self.play_next).pack(side="left", padx=5)
        
        # 进度条
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.time_label = ttk.Label(progress_frame, text="00:00")
        self.time_label.pack(side="left", padx=5)
        
        self.progress_scale = ttk.Scale(progress_frame, from_=0, to=100, orient="horizontal", length=600, command=self.set_position)
        self.progress_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.progress_scale.bind("<ButtonRelease-1>", self.seek_position)
        
        self.duration_label = ttk.Label(progress_frame, text="00:00")
        self.duration_label.pack(side="right", padx=5)
        
        # 当前播放歌曲显示
        self.current_song_label = ttk.Label(self.root, text="未播放任何歌曲", font=("SimHei", 12), anchor="center")
        self.current_song_label.pack(fill="x", padx=10, pady=5)
    
    def select_music_folder(self):
        """选择音乐文件夹"""
        folder_path = filedialog.askdirectory(title="选择音乐文件夹")
        if folder_path:
            self.config['default_music_folder'] = folder_path
            self.save_config()
            self.scan_music_folder(folder_path)
    
    def scan_music_folder(self, folder_path):
        """扫描音乐文件夹"""
        self.song_listbox.delete(0, tk.END)
        try:
            self.playlist = self.local_music_manager.scan_folder(folder_path)
            for song in self.playlist:
                song_name = os.path.basename(song)
                self.song_listbox.insert(tk.END, song_name)
        except Exception as e:
            messagebox.showerror("错误", f"扫描文件夹失败: {str(e)}")
    
    def play_selected_song(self, event=None):
        """播放选中的歌曲"""
        selection = self.song_listbox.curselection()
        if selection:
            index = selection[0]
            self.current_song = self.playlist[index]
            self.play_music(self.current_song)
    
    def play_music(self, music_file):
        """播放音乐"""
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.play_button.config(text="暂停")
            self.current_song_label.config(text=os.path.basename(music_file))
            
            # 启动进度更新线程
            self.stop_thread = True
            if self.update_thread and self.update_thread.is_alive():
                self.update_thread.join()
            self.stop_thread = False
            self.update_thread = threading.Thread(target=self.update_progress)
            self.update_thread.daemon = True
            self.update_thread.start()
        except Exception as e:
            messagebox.showerror("错误", f"播放失败: {str(e)}")
    
    def toggle_play_pause(self):
        """切换播放/暂停状态"""
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.play_button.config(text="暂停")
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_button.config(text="播放")
        elif self.current_song:
            self.play_music(self.current_song)
    
    def play_next(self):
        """播放下一曲"""
        if not self.playlist or not self.current_song:
            return
        
        current_index = self.playlist.index(self.current_song)
        if self.is_shuffle:
            import random
            next_index = random.randint(0, len(self.playlist) - 1)
        else:
            next_index = (current_index + 1) % len(self.playlist)
        
        self.current_song = self.playlist[next_index]
        self.play_music(self.current_song)
        self.song_listbox.selection_clear(0, tk.END)
        self.song_listbox.selection_set(next_index)
        self.song_listbox.see(next_index)
    
    def play_previous(self):
        """播放上一曲"""
        if not self.playlist or not self.current_song:
            return
        
        current_index = self.playlist.index(self.current_song)
        if self.is_shuffle:
            import random
            prev_index = random.randint(0, len(self.playlist) - 1)
        else:
            prev_index = (current_index - 1) % len(self.playlist)
        
        self.current_song = self.playlist[prev_index]
        self.play_music(self.current_song)
        self.song_listbox.selection_clear(0, tk.END)
        self.song_listbox.selection_set(prev_index)
        self.song_listbox.see(prev_index)
    
    def set_volume(self, volume):
        """设置音量"""
        volume_value = float(volume)
        pygame.mixer.music.set_volume(volume_value)
        self.config['volume'] = volume_value
        self.save_config()
    
    def update_progress(self):
        """更新播放进度"""
        while not self.stop_thread:
            if self.is_playing and not self.is_paused:
                # 获取当前播放位置
                current_pos = pygame.mixer.music.get_pos() / 1000.0
                # 获取音乐总时长
                try:
                    # 尝试使用pygame获取时长
                    pygame.mixer.music.set_pos(0)
                    pygame.mixer.music.set_pos(current_pos)
                    # 由于pygame限制，我们使用一种估算方法
                    # 实际项目中可能需要使用其他库来获取准确时长
                    duration = 300  # 假设默认5分钟
                    
                    # 更新进度条
                    self.root.after(0, lambda: self.update_progress_ui(current_pos, duration))
                    
                    # 检查是否播放结束
                    if current_pos > 0 and pygame.mixer.music.get_busy() == False:
                        if self.is_repeat:
                            self.root.after(0, lambda: self.play_music(self.current_song))
                        else:
                            self.root.after(0, self.play_next)
                except:
                    pass
            time.sleep(0.5)
    
    def update_progress_ui(self, current_pos, duration):
        """更新进度条UI"""
        if duration > 0:
            self.progress_scale.config(to=duration)
            self.progress_scale.set(current_pos)
            
            # 更新时间标签
            self.time_label.config(text=self.format_time(current_pos))
            self.duration_label.config(text=self.format_time(duration))
    
    def format_time(self, seconds):
        """格式化时间为分:秒"""
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def seek_position(self, event):
        """拖动进度条跳转播放位置"""
        if self.is_playing:
            position = self.progress_scale.get()
            pygame.mixer.music.set_pos(position)
    
    def set_position(self, position):
        """设置播放位置"""
        # 这个方法主要用于进度条拖动时的实时更新
        pass
    
    def toggle_repeat(self):
        """切换重复播放"""
        self.is_repeat = self.repeat_var.get()
    
    def toggle_shuffle(self):
        """切换随机播放"""
        self.is_shuffle = self.shuffle_var.get()
    
    def search_online_music(self):
        """搜索在线音乐"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("提示", "请输入搜索关键词")
            return
        
        # 清空列表
        self.online_listbox.delete(0, tk.END)
        
        # 显示搜索中
        self.online_listbox.insert(tk.END, "正在搜索中...")
        
        # 在新线程中执行搜索
        def do_search():
            try:
                results = self.online_music_manager.search_music(keyword)
                self.root.after(0, lambda: self.show_search_results(results))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("搜索失败", str(e)))
        
        search_thread = threading.Thread(target=do_search)
        search_thread.daemon = True
        search_thread.start()
    
    def show_search_results(self, results):
        """显示搜索结果"""
        self.online_listbox.delete(0, tk.END)
        
        if not results:
            self.online_listbox.insert(tk.END, "未找到相关音乐")
            return
        
        # 保存搜索结果
        self.search_results = results
        
        # 显示结果
        for i, result in enumerate(results):
            title = result.get('title', '未知标题')
            artist = result.get('artist', '未知艺术家')
            duration = result.get('duration', '未知时长')
            self.online_listbox.insert(tk.END, f"{i+1}. {title} - {artist} ({duration})")
    
    def download_selected_music(self):
        """下载选中的音乐"""
        selection = self.online_listbox.curselection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要下载的音乐")
            return
        
        index = selection[0]
        if hasattr(self, 'search_results') and index < len(self.search_results):
            music_info = self.search_results[index]
            
            # 选择下载目录
            download_folder = filedialog.askdirectory(title="选择下载目录", initialdir=self.config['download_folder'])
            if not download_folder:
                return
            
            # 更新默认下载目录
            self.config['download_folder'] = download_folder
            self.save_config()
            
            # 显示下载中
            self.online_listbox.itemconfig(index, fg="blue")
            original_text = self.online_listbox.get(index)
            self.online_listbox.delete(index)
            self.online_listbox.insert(index, f"{original_text} [下载中...]")
            
            # 在新线程中执行下载
            def do_download():
                try:
                    file_path = self.online_music_manager.download_music(music_info, download_folder)
                    self.root.after(0, lambda: self.online_listbox.itemconfig(index, fg="green"))
                    self.root.after(0, lambda idx=index: self.online_listbox.delete(idx))
                    self.root.after(0, lambda idx=index, text=original_text: self.online_listbox.insert(idx, f"{text} [下载完成]"))
                    self.root.after(0, lambda path=file_path: messagebox.showinfo("下载成功", f"音乐已下载到:\n{path}"))
                except Exception as e:
                    self.root.after(0, lambda: self.online_listbox.itemconfig(index, fg="red"))
                    self.root.after(0, lambda idx=index: self.online_listbox.delete(idx))
                    self.root.after(0, lambda idx=index, text=original_text: self.online_listbox.insert(idx, f"{text} [下载失败]"))
                    self.root.after(0, lambda error=str(e): messagebox.showerror("下载失败", error))
            
            download_thread = threading.Thread(target=do_download)
            download_thread.daemon = True
            download_thread.start()
    
    def on_closing(self):
        """关闭窗口时的清理工作"""
        self.stop_thread = True
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(1.0)
        pygame.mixer.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()