import requests
import json
import os
import re
import time
import random
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

class OnlineMusicManager:
    def __init__(self):
        # 初始化搜索API配置
        # 注意：这里使用的是示例API，实际项目中需要使用可靠的音乐API服务
        # 并且要确保遵守相关版权法规
        self.api_timeout = 30
        self.max_retries = 3
    
    def search_music(self, keyword):
        """
        搜索在线音乐
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            list: 音乐搜索结果列表
        """
        if not keyword or len(keyword.strip()) == 0:
            raise ValueError("搜索关键词不能为空")
        
        try:
            # 这里实现一个基础的搜索功能
            # 在实际项目中，你需要替换为真实的音乐API
            results = self._search_music_demo(keyword)
            return results
        except Exception as e:
            # 如果API调用失败，返回模拟数据作为演示
            print(f"搜索API调用失败: {str(e)}")
            return self._get_mock_search_results(keyword)
    
    def _search_music_demo(self, keyword):
        """
        演示用的音乐搜索方法
        在实际项目中，这里应该调用真实的音乐搜索API
        """
        # 构建搜索URL示例（这里使用了一个免费的音乐搜索API示例）
        # 注意：这些API可能不稳定或有使用限制
        search_urls = [
            f"https://api.example.com/search?keyword={quote(keyword)}",
            f"https://api.demo.com/music/search?q={quote(keyword)}"
        ]
        
        for url in search_urls:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                # 添加重试机制
                for retry in range(self.max_retries):
                    try:
                        response = requests.get(url, headers=headers, timeout=self.api_timeout)
                        if response.status_code == 200:
                            data = response.json()
                            # 解析API响应
                            return self._parse_api_response(data)
                        else:
                            print(f"API返回非200状态码: {response.status_code}")
                    except requests.exceptions.Timeout:
                        print(f"请求超时，正在重试 ({retry+1}/{self.max_retries})...")
                        time.sleep(2)
                    except requests.exceptions.RequestException as e:
                        print(f"请求异常: {str(e)}")
                        break
            except Exception as e:
                print(f"搜索URL {url} 调用失败: {str(e)}")
                # 尝试下一个URL
                continue
        
        # 如果所有API都失败，返回模拟数据
        return self._get_mock_search_results(keyword)
    
    def _parse_api_response(self, data):
        """
        解析API响应数据
        不同的API可能有不同的响应格式，需要根据实际情况调整
        """
        results = []
        
        # 尝试解析常见的API响应格式
        try:
            # 格式1: {"data": [{"title": "...", "artist": "...", ...}]}
            if "data" in data and isinstance(data["data"], list):
                for item in data["data"]:
                    result = self._extract_music_info(item)
                    if result:
                        results.append(result)
            # 格式2: {"songs": [{"name": "...", "singer": "...", ...}]}
            elif "songs" in data and isinstance(data["songs"], list):
                for item in data["songs"]:
                    result = self._extract_music_info(item)
                    if result:
                        results.append(result)
            # 格式3: {"result": [{"title": "...", "artist": "...", ...}]}
            elif "result" in data and isinstance(data["result"], list):
                for item in data["result"]:
                    result = self._extract_music_info(item)
                    if result:
                        results.append(result)
        except Exception as e:
            print(f"解析API响应失败: {str(e)}")
        
        return results[:20]  # 最多返回20条结果
    
    def _extract_music_info(self, item):
        """
        从API返回的单个项目中提取音乐信息
        """
        try:
            # 尝试不同的字段名称来获取信息
            title = item.get("title") or item.get("name") or item.get("songname") or "未知标题"
            artist = item.get("artist") or item.get("singer") or item.get("artistname") or "未知艺术家"
            
            # 如果艺术家是列表，将其转换为字符串
            if isinstance(artist, list):
                artist = ", ".join(artist)
            
            duration = item.get("duration") or item.get("time") or "00:00"
            
            # 获取音乐URL或ID
            url = item.get("url") or item.get("download_url") or ""
            song_id = item.get("id") or item.get("songid") or ""
            
            return {
                "title": title,
                "artist": artist,
                "duration": duration,
                "url": url,
                "id": song_id,
                "source": "api"
            }
        except Exception:
            return None
    
    def _get_mock_search_results(self, keyword):
        """
        获取模拟的搜索结果（当API调用失败时使用）
        """
        # 模拟一些搜索结果
        mock_titles = [
            "晴天", "告白气球", "青花瓷", "七里香", "听妈妈的话",
            "夜曲", "稻香", "双截棍", "简单爱", "安静",
            "东风破", "珊瑚海", "发如雪", "烟花易冷", "蒲公英的约定",
            "不能说的秘密", "七里香", "退后", "借口", "轨迹"
        ]
        
        mock_artists = ["周杰伦", "林俊杰", "陈奕迅", "张学友", "王力宏"]
        
        results = []
        # 根据关键词筛选模拟结果
        for title in mock_titles:
            if keyword in title:
                results.append({
                    "title": title,
                    "artist": random.choice(mock_artists),
                    "duration": f"0{random.randint(3, 5)}:{random.randint(10, 59):02d}",
                    "id": f"mock_{len(results) + 1}",
                    "source": "mock"
                })
        
        # 如果没有匹配的结果，添加一些包含关键词的模拟结果
        if not results:
            for i in range(5):
                results.append({
                    "title": f"{keyword} - 歌曲{i+1}",
                    "artist": random.choice(mock_artists),
                    "duration": f"0{random.randint(3, 5)}:{random.randint(10, 59):02d}",
                    "id": f"mock_custom_{i+1}",
                    "source": "mock"
                })
        
        return results
    
    def download_music(self, music_info, download_folder):
        """
        下载音乐文件
        
        Args:
            music_info: 包含音乐信息的字典
            download_folder: 下载目录
            
        Returns:
            str: 下载后的文件路径
        """
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        
        # 生成文件名
        title = music_info.get("title", "未知歌曲")
        artist = music_info.get("artist", "未知艺术家")
        
        # 清理文件名中的非法字符
        filename = self._sanitize_filename(f"{artist} - {title}.mp3")
        file_path = os.path.join(download_folder, filename)
        
        # 检查文件是否已存在
        if os.path.exists(file_path):
            # 如果文件已存在，添加数字后缀
            base_name, ext = os.path.splitext(file_path)
            counter = 1
            while os.path.exists(f"{base_name}({counter}){ext}"):
                counter += 1
            file_path = f"{base_name}({counter}){ext}"
        
        try:
            # 如果音乐信息中已有URL，可以直接下载
            if music_info.get("url"):
                return self._download_file(music_info["url"], file_path)
            else:
                # 否则，尝试获取下载链接
                download_url = self._get_download_url(music_info)
                if download_url:
                    return self._download_file(download_url, file_path)
                else:
                    # 如果无法获取真实下载链接，创建一个模拟的音频文件
                    return self._create_mock_audio_file(file_path, music_info)
        except Exception as e:
            raise Exception(f"下载失败: {str(e)}")
    
    def _get_download_url(self, music_info):
        """
        获取音乐下载链接
        """
        # 这里应该根据音乐ID调用相应的API获取下载链接
        # 由于是演示，返回None以使用模拟下载
        return None
    
    def _download_file(self, url, file_path):
        """
        下载文件
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 添加重试机制
        for retry in range(self.max_retries):
            try:
                response = requests.get(url, headers=headers, stream=True, timeout=self.api_timeout)
                response.raise_for_status()
                
                # 下载文件
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # 验证文件是否成功下载
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    return file_path
                else:
                    raise Exception("文件下载失败，文件大小为0")
                    
            except requests.exceptions.RequestException as e:
                print(f"下载请求异常: {str(e)}")
                if retry < self.max_retries - 1:
                    print(f"正在重试 ({retry+1}/{self.max_retries})...")
                    time.sleep(2)
                else:
                    raise
    
    def _create_mock_audio_file(self, file_path, music_info):
        """
        创建模拟的音频文件（用于演示）
        """
        # 在实际应用中，这里应该尝试真实的下载
        # 这里只是为了演示功能，创建一个文本文件作为模拟
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"这是一个模拟的音频文件\n")
            f.write(f"标题: {music_info.get('title', '未知歌曲')}\n")
            f.write(f"艺术家: {music_info.get('artist', '未知艺术家')}\n")
            f.write(f"时长: {music_info.get('duration', '未知时长')}\n")
            f.write(f"\n注意: 这是一个演示用的模拟文件。在实际应用中，")
            f.write(f"这里应该包含真实的音频数据。")
        
        return file_path
    
    def _sanitize_filename(self, filename):
        """
        清理文件名中的非法字符
        """
        # 移除Windows文件名中的非法字符
        illegal_chars = '<>:"/\\|?*'
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        
        # 移除控制字符
        filename = re.sub(r'[\x00-\x1f\x7f]', '', filename)
        
        # 限制文件名长度
        max_length = 200
        if len(filename) > max_length:
            name, ext = os.path.splitext(filename)
            filename = name[:max_length - len(ext)] + ext
        
        return filename.strip()
    
    def batch_download(self, music_list, download_folder, max_workers=3):
        """
        批量下载音乐
        
        Args:
            music_list: 音乐信息列表
            download_folder: 下载目录
            max_workers: 最大工作线程数
            
        Returns:
            dict: 下载结果字典，键为音乐ID，值为下载状态和路径
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有下载任务
            future_to_music = {
                executor.submit(self.download_music, music_info, download_folder): music_info 
                for music_info in music_list
            }
            
            # 处理下载结果
            for future in future_to_music:
                music_info = future_to_music[future]
                music_id = music_info.get('id', 'unknown')
                try:
                    file_path = future.result()
                    results[music_id] = {
                        'status': 'success',
                        'path': file_path
                    }
                except Exception as e:
                    results[music_id] = {
                        'status': 'failed',
                        'error': str(e)
                    }
        
        return results