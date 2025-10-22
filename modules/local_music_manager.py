import os
import fnmatch

class LocalMusicManager:
    def __init__(self):
        # 支持的音频文件格式
        self.supported_formats = [
            '*.mp3', '*.wav', '*.flac', '*.aac', '*.ogg', '*.wma',
            '*.m4a', '*.opus', '*.amr', '*.mid', '*.midi'
        ]
    
    def scan_folder(self, folder_path):
        """
        扫描指定文件夹中的所有音乐文件
        
        Args:
            folder_path: 要扫描的文件夹路径
            
        Returns:
            list: 音乐文件的完整路径列表
        """
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            raise ValueError(f"无效的文件夹路径: {folder_path}")
        
        music_files = []
        
        # 遍历文件夹及其子文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if self._is_audio_file(file):
                    full_path = os.path.join(root, file)
                    music_files.append(full_path)
        
        # 按照文件名排序
        music_files.sort(key=lambda x: os.path.basename(x).lower())
        
        return music_files
    
    def _is_audio_file(self, filename):
        """
        检查文件是否为支持的音频格式
        
        Args:
            filename: 文件名
            
        Returns:
            bool: 如果是支持的音频格式返回True，否则返回False
        """
        for pattern in self.supported_formats:
            if fnmatch.fnmatch(filename.lower(), pattern):
                return True
        return False
    
    def get_file_info(self, file_path):
        """
        获取音频文件的基本信息
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            dict: 包含文件名、大小、修改时间等信息的字典
        """
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise ValueError(f"无效的文件路径: {file_path}")
        
        # 获取文件基本信息
        stats = os.stat(file_path)
        
        info = {
            'filename': os.path.basename(file_path),
            'path': file_path,
            'size': stats.st_size,  # 字节
            'size_mb': round(stats.st_size / (1024 * 1024), 2),  # MB
            'modified_time': stats.st_mtime,
            'format': os.path.splitext(file_path)[1].lower()
        }
        
        # 尝试获取音频元数据（这里只是基础实现，实际项目中可以使用mutagen等库）
        info['title'] = self._extract_title(file_path)
        info['artist'] = self._extract_artist(file_path)
        
        return info
    
    def _extract_title(self, file_path):
        """
        尝试从文件名提取歌曲标题
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 歌曲标题
        """
        # 移除扩展名
        filename = os.path.splitext(os.path.basename(file_path))[0]
        
        # 尝试分离艺术家和标题
        # 常见格式: 艺术家 - 标题
        if ' - ' in filename:
            parts = filename.split(' - ', 1)
            if len(parts) > 1:
                return parts[1].strip()
        
        # 如果无法分离，返回整个文件名
        return filename
    
    def _extract_artist(self, file_path):
        """
        尝试从文件名提取艺术家信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 艺术家名称
        """
        # 移除扩展名
        filename = os.path.splitext(os.path.basename(file_path))[0]
        
        # 尝试分离艺术家和标题
        # 常见格式: 艺术家 - 标题
        if ' - ' in filename:
            parts = filename.split(' - ', 1)
            return parts[0].strip()
        
        # 如果无法提取，返回"未知艺术家"
        return "未知艺术家"
    
    def search_local_music(self, folder_path, keyword):
        """
        在本地音乐库中搜索指定关键词的音乐
        
        Args:
            folder_path: 音乐文件夹路径
            keyword: 搜索关键词
            
        Returns:
            list: 匹配的音乐文件路径列表
        """
        all_music = self.scan_folder(folder_path)
        keyword = keyword.lower()
        
        results = []
        for music_file in all_music:
            filename = os.path.basename(music_file).lower()
            if keyword in filename:
                results.append(music_file)
        
        return results
    
    def get_folder_size(self, folder_path):
        """
        计算音乐文件夹的总大小
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            int: 文件夹总大小（字节）
        """
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            raise ValueError(f"无效的文件夹路径: {folder_path}")
        
        total_size = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if self._is_audio_file(file):
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
        
        return total_size
    
    def organize_music_by_artist(self, folder_path):
        """
        按艺术家对音乐文件进行分组
        
        Args:
            folder_path: 音乐文件夹路径
            
        Returns:
            dict: 以艺术家为键，音乐文件列表为值的字典
        """
        all_music = self.scan_folder(folder_path)
        organized = {}
        
        for music_file in all_music:
            artist = self._extract_artist(music_file)
            if artist not in organized:
                organized[artist] = []
            organized[artist].append(music_file)
        
        return organized
    
    def organize_music_by_folder(self, folder_path):
        """
        按文件夹结构对音乐文件进行分组
        
        Args:
            folder_path: 根文件夹路径
            
        Returns:
            dict: 以相对文件夹路径为键，音乐文件列表为值的字典
        """
        organized = {}
        
        for root, dirs, files in os.walk(folder_path):
            # 获取相对路径
            relative_path = os.path.relpath(root, folder_path)
            if relative_path == '.':
                relative_path = '根目录'
            
            # 收集此文件夹中的音频文件
            music_files = []
            for file in files:
                if self._is_audio_file(file):
                    full_path = os.path.join(root, file)
                    music_files.append(full_path)
            
            if music_files:
                organized[relative_path] = music_files
        
        return organized
    
    def get_recently_added(self, folder_path, days=7):
        """
        获取最近添加的音乐文件
        
        Args:
            folder_path: 音乐文件夹路径
            days: 天数范围
            
        Returns:
            list: 最近添加的音乐文件列表
        """
        import time
        
        all_music = self.scan_folder(folder_path)
        recent_files = []
        
        # 计算时间阈值
        time_threshold = time.time() - (days * 24 * 3600)
        
        for music_file in all_music:
            if os.path.getmtime(music_file) > time_threshold:
                recent_files.append(music_file)
        
        # 按修改时间倒序排序
        recent_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return recent_files