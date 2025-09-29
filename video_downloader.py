"""
Advanced Video Downloader

Supports 100+ platforms including YouTube, Instagram, TikTok, Twitter, Reddit, Facebook, and more.
Features include quality selection, batch downloading, progress tracking, and metadata extraction.
"""

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
import os
import re
import json
import time
import threading
from urllib.parse import urlparse
from logger import setup_logger, log_event, log_error

class VideoDownloader:
    """
    Advanced video downloader supporting 100+ platforms with comprehensive features
    """
    
    def __init__(self, download_dir='downloads'):
        """Initialize the video downloader"""
        self.download_dir = download_dir
        self.logger = setup_logger('video_downloader', 'video_downloader.log')
        self.active_downloads = {}
        self.download_history = []
        
        # Create downloads directory
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Default yt-dlp options with enhanced mobile support and 403 handling
        self.base_options = {
            'outtmpl': f'{self.download_dir}/%(title)s.%(ext)s',  # Will be overridden with quality-specific template
            'format': 'best/bestvideo+bestaudio/bestvideo*+bestaudio/best[height<=1080]/best[height<=720]/best[height<=480]/worst',
            'writesubtitles': False,
            'writeautomaticsub': False,
            'writethumbnail': False,
            'extract_flat': False,
            'no_warnings': False,
            'ignoreerrors': True,
            'socket_timeout': 30,
            'retries': 5,
            'noplaylist': True,  # CRITICAL: Only download single videos, never entire playlists
            'extractor_args': {
                'youtube': {
                    'skip': ['hls', 'dash'],
                    'player_skip': ['configs'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
            'merge_output_format': 'mp4',
            'prefer_ffmpeg': True,
            'cookiefile': None,
            'age_limit': None
        }
        
        log_event(self.logger, 'init', 'Video downloader initialized')
    
    def get_video_info(self, url):
        """Extract video information without downloading"""
        if not YT_DLP_AVAILABLE:
            return {'error': 'yt-dlp not available. Please install it to use video downloader.'}
        
        try:
            # Enhanced options for better mobile/shorts support
            info_options = {
                'quiet': True, 
                'no_warnings': True,
                'socket_timeout': 30,
                'retries': 3,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
                }
            }
            
            with yt_dlp.YoutubeDL(info_options) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Handle playlists
                if 'entries' in info:
                    videos = []
                    for entry in info['entries'][:10]:  # Limit to first 10 for preview
                        if entry:
                            videos.append({
                                'title': entry.get('title', 'Unknown'),
                                'duration': self._format_duration(entry.get('duration')),
                                'uploader': entry.get('uploader', 'Unknown'),
                                'view_count': entry.get('view_count', 0),
                                'upload_date': entry.get('upload_date', ''),
                                'url': entry.get('webpage_url', ''),
                                'thumbnail': entry.get('thumbnail', ''),
                                'formats': self._extract_formats(entry.get('formats', []))
                            })
                    
                    return {
                        'type': 'playlist',
                        'title': info.get('title', 'Playlist'),
                        'uploader': info.get('uploader', 'Unknown'),
                        'video_count': len(info['entries']),
                        'videos': videos,
                        'url': url
                    }
                else:
                    # Single video
                    return {
                        'type': 'video',
                        'title': info.get('title', 'Unknown'),
                        'duration': self._format_duration(info.get('duration')),
                        'uploader': info.get('uploader', 'Unknown'),
                        'view_count': info.get('view_count', 0),
                        'upload_date': info.get('upload_date', ''),
                        'description': info.get('description', '')[:500] + '...' if info.get('description', '') else '',
                        'thumbnail': info.get('thumbnail', ''),
                        'formats': self._extract_formats(info.get('formats', [])),
                        'url': url,
                        'platform': self._detect_platform(url)
                    }
                    
        except Exception as e:
            log_error(self.logger, 'get_video_info', e, {'url': url})
            return {'error': str(e)}
    
    def _extract_formats(self, formats):
        """Extract available video formats and qualities"""
        video_formats = []
        audio_formats = []
        
        for fmt in formats:
            if fmt.get('vcodec') != 'none':  # Video format
                video_formats.append({
                    'format_id': fmt.get('format_id'),
                    'quality': fmt.get('height', 'Unknown'),
                    'fps': fmt.get('fps', ''),
                    'ext': fmt.get('ext'),
                    'filesize': self._format_filesize(fmt.get('filesize')),
                    'vcodec': fmt.get('vcodec', ''),
                    'acodec': fmt.get('acodec', '')
                })
            elif fmt.get('acodec') != 'none':  # Audio format
                audio_formats.append({
                    'format_id': fmt.get('format_id'),
                    'ext': fmt.get('ext'),
                    'abr': fmt.get('abr', ''),
                    'filesize': self._format_filesize(fmt.get('filesize')),
                    'acodec': fmt.get('acodec', '')
                })
        
        # Sort by quality
        video_formats.sort(key=lambda x: x.get('quality', 0) if isinstance(x.get('quality'), int) else 0, reverse=True)
        audio_formats.sort(key=lambda x: x.get('abr', 0) if isinstance(x.get('abr'), (int, float)) else 0, reverse=True)
        
        return {
            'video': video_formats[:10],  # Top 10 video qualities
            'audio': audio_formats[:5]    # Top 5 audio qualities
        }
    
    def download_video(self, url, options=None, download_id=None):
        """Download video with progress tracking"""
        if not YT_DLP_AVAILABLE:
            return {'success': False, 'error': 'yt-dlp not available. Please install it to use video downloader.'}
        
        if not download_id:
            download_id = f"download_{int(time.time())}"
        
        # Initialize download tracking
        self.active_downloads[download_id] = {
            'url': url,
            'status': 'starting',
            'progress': 0,
            'speed': '0 B/s',
            'eta': 'Unknown',
            'filename': '',
            'filepath': '',
            'error': None,
            'start_time': time.time()
        }
        
        # Start download in separate thread
        def download_worker():
            try:
                # Merge options
                dl_options = self.base_options.copy()
                if options:
                    dl_options.update(options)
                
                # Progress hook
                dl_options['progress_hooks'] = [lambda d: self._progress_hook(d, download_id)]
                
                with yt_dlp.YoutubeDL(dl_options) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                    # Mark as completed
                    self.active_downloads[download_id]['status'] = 'completed'
                    self.active_downloads[download_id]['progress'] = 100
                    self.active_downloads[download_id]['title'] = info.get('title', 'Unknown')
                    
                    # Add to history
                    self.download_history.append({
                        'url': url,
                        'title': info.get('title', 'Unknown'),
                        'filename': self.active_downloads[download_id]['filename'],
                        'filepath': self.active_downloads[download_id]['filepath'],
                        'download_time': time.time() - self.active_downloads[download_id]['start_time'],
                        'platform': self._detect_platform(url),
                        'timestamp': time.time()
                    })
                    
                    log_event(self.logger, 'download_completed', f"Successfully downloaded: {info.get('title')}")
                    
            except Exception as e:
                self.active_downloads[download_id]['status'] = 'error'
                self.active_downloads[download_id]['error'] = str(e)
                log_error(self.logger, 'download_video', e, {'url': url})
        
        # Start download thread
        thread = threading.Thread(target=download_worker)
        thread.daemon = True
        thread.start()
        
        return {'success': True, 'download_id': download_id}
    
    def download_video_sync(self, url, options=None):
        """Download video synchronously and return file info"""
        if not YT_DLP_AVAILABLE:
            return {'success': False, 'error': 'yt-dlp not available. Please install it to use video downloader.'}
        
        try:
            # Merge options with enhanced mobile/shorts support
            dl_options = self.base_options.copy()
            if options:
                dl_options.update(options)
            
            # Platform-specific optimizations for shorts and reels
            platform = self._detect_platform(url)
            if 'shorts' in url.lower() or platform == 'Instagram':
                # Enhanced options for mobile-first content
                dl_options.update({
                    'format': 'best/bestvideo*+bestaudio/bestvideo/bestaudio/worst',
                    'fragment_retries': 10,
                    'skip_unavailable_fragments': True
                })
            
            # Ensure downloads directory exists
            os.makedirs(self.download_dir, exist_ok=True)
            
            downloaded_file = None
            
            with yt_dlp.YoutubeDL(dl_options) as ydl:
                # Extract info first to get basic video info
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                
                # Manually construct quality-aware filename 
                # Extract quality from format options if available
                quality_suffix = "unknown"
                if options and isinstance(options, dict) and 'format' in options:
                    format_str = options['format']
                    # Extract height from format string (e.g., "best[height>=1080]" -> "1080p")
                    import re
                    height_match = re.search(r'height[>=<]+([0-9]+)', format_str)
                    if height_match:
                        quality_suffix = f"{height_match.group(1)}p"
                
                # Construct filename with quality info
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)  # Clean title for filename
                expected_basename = f"{safe_title}_[{quality_suffix}].mp4"
                expected_filepath = os.path.join(self.download_dir, expected_basename)
                
                # Check if THIS specific quality file already exists
                if os.path.exists(expected_filepath):
                    # File already exists - return it as successful download
                    downloaded_file = {
                        'filename': expected_basename,
                        'filepath': expected_filepath,
                        'title': title,
                        'size': os.path.getsize(expected_filepath),
                        'platform': self._detect_platform(url),
                        'url': url
                    }
                    log_event(self.logger, 'sync_download_completed', f"File already exists: {title}")
                else:
                    # File doesn't exist, proceed with download
                    # Update the output template to include quality info
                    ydl.params['outtmpl'] = expected_filepath.replace('.mp4', '.%(ext)s')
                    
                    try:
                        ydl.download([url])
                        
                        # Find the downloaded file (check expected location first)
                        if os.path.exists(expected_filepath):
                            downloaded_file = {
                                'filename': expected_basename,
                                'filepath': expected_filepath,
                                'title': title,
                                'size': os.path.getsize(expected_filepath),
                                'platform': self._detect_platform(url),
                                'url': url
                            }
                        else:
                            # Fallback: search for recently created files
                            for filename in os.listdir(self.download_dir):
                                filepath = os.path.join(self.download_dir, filename)
                                if os.path.isfile(filepath):
                                    file_time = os.path.getctime(filepath)
                                    if time.time() - file_time < 120:  # Extended to 2 minutes
                                        downloaded_file = {
                                            'filename': filename,
                                            'filepath': filepath,
                                            'title': title,
                                            'size': os.path.getsize(filepath),
                                            'platform': self._detect_platform(url),
                                            'url': url
                                        }
                                        break
                    except Exception as download_error:
                        # Handle specific download errors
                        if "already been downloaded" in str(download_error).lower():
                            # yt-dlp says it's already downloaded, find the file
                            if os.path.exists(expected_filepath):
                                downloaded_file = {
                                    'filename': expected_basename,
                                    'filepath': expected_filepath,
                                    'title': title,
                                    'size': os.path.getsize(expected_filepath),
                                    'platform': self._detect_platform(url),
                                    'url': url
                                }
                                log_event(self.logger, 'sync_download_completed', f"Found existing file: {title}")
                            else:
                                raise download_error
                        else:
                            raise download_error
                
                if downloaded_file:
                    # Add to history
                    self.download_history.append({
                        'url': url,
                        'title': title,
                        'filename': downloaded_file['filename'],
                        'filepath': downloaded_file['filepath'],
                        'download_time': 0,  # Sync download
                        'platform': self._detect_platform(url),
                        'timestamp': time.time()
                    })
                    
                    log_event(self.logger, 'sync_download_completed', f"Successfully downloaded: {title}")
                    return {'success': True, 'file_info': downloaded_file}
                else:
                    return {'success': False, 'error': 'File not found after download'}
                
        except Exception as e:
            error_msg = str(e)
            # Enhanced error handling for format issues
            if 'Requested format is not available' in error_msg:
                error_msg = f"Video format not available. This may be due to platform restrictions or regional blocking. Original error: {error_msg}"
            log_error(self.logger, 'sync_download_video', e, {'url': url})
            return {'success': False, 'error': error_msg}
    
    def download_audio_only(self, url, format='mp3', quality='192'):
        """Download audio only"""
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': quality,
            }],
            'outtmpl': f'{self.download_dir}/%(uploader)s - %(title)s.%(ext)s'
        }
        
        return self.download_video(url, options)
    
    def batch_download(self, urls, options=None):
        """Download multiple videos"""
        results = []
        
        for i, url in enumerate(urls):
            download_id = f"batch_{int(time.time())}_{i}"
            
            # Start download in thread
            thread = threading.Thread(
                target=lambda: results.append(self.download_video(url, options, download_id))
            )
            thread.start()
            
            # Small delay to prevent overwhelming
            time.sleep(0.5)
        
        return results
    
    def get_download_progress(self, download_id):
        """Get progress for specific download"""
        return self.active_downloads.get(download_id, {'error': 'Download not found'})
    
    def get_all_downloads(self):
        """Get all active downloads"""
        return self.active_downloads
    
    def get_download_history(self, limit=50):
        """Get download history"""
        return sorted(self.download_history, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_supported_platforms(self):
        """Get list of supported platforms"""
        return [
            'YouTube', 'Instagram', 'TikTok', 'Twitter/X', 'Facebook', 'Reddit',
            'Vimeo', 'Dailymotion', 'Twitch', 'SoundCloud', 'Bandcamp',
            'Archive.org', 'BBC iPlayer', 'CNN', 'ESPN', 'NBC', 'Pornhub',
            'Telegram', 'VK', 'Weibo', 'Bilibili', 'Niconico', 'Crunchyroll',
            'And 80+ more platforms...'
        ]
    
    def cleanup_old_downloads(self, days=7):
        """Clean up old download files"""
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            cleaned_count = 0
            
            for filename in os.listdir(self.download_dir):
                filepath = os.path.join(self.download_dir, filename)
                if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff_time:
                    os.remove(filepath)
                    cleaned_count += 1
            
            log_event(self.logger, 'cleanup', f"Cleaned {cleaned_count} old files")
            return cleaned_count
            
        except Exception as e:
            log_error(self.logger, 'cleanup', e)
            return 0
    
    def _progress_hook(self, d, download_id):
        """Progress hook for yt-dlp"""
        if download_id in self.active_downloads:
            if d['status'] == 'downloading':
                # Extract progress percentage safely
                progress_str = d.get('_percent_str', '0%')
                try:
                    progress = float(progress_str.replace('%', '').strip()) if progress_str else 0
                except:
                    progress = 0
                    
                self.active_downloads[download_id].update({
                    'status': 'downloading',
                    'progress': progress,
                    'speed': d.get('_speed_str', '0 B/s'),
                    'eta': d.get('_eta_str', 'Unknown'),
                    'filename': d.get('filename', '').split('/')[-1] if d.get('filename') else '',
                    'filepath': d.get('filename', '')
                })
            elif d['status'] == 'finished':
                self.active_downloads[download_id].update({
                    'status': 'processing',
                    'filename': d.get('filename', '').split('/')[-1] if d.get('filename') else '',
                    'filepath': d.get('filename', '')
                })
    
    def _detect_platform(self, url):
        """Detect platform from URL with enhanced shorts/reels detection"""
        domain = urlparse(url).netloc.lower()
        url_lower = url.lower()
        
        platform_map = {
            'youtube.com': 'YouTube',
            'youtu.be': 'YouTube',
            'instagram.com': 'Instagram',
            'tiktok.com': 'TikTok',
            'twitter.com': 'Twitter',
            'x.com': 'Twitter/X',
            'facebook.com': 'Facebook',
            'reddit.com': 'Reddit',
            'vimeo.com': 'Vimeo',
            'dailymotion.com': 'Dailymotion',
            'twitch.tv': 'Twitch',
            'soundcloud.com': 'SoundCloud',
        }
        
        # Enhanced detection for mobile content
        for domain_key, platform in platform_map.items():
            if domain_key in domain:
                if 'shorts' in url_lower and 'youtube' in domain_key:
                    return 'YouTube Shorts'
                elif 'reel' in url_lower and 'instagram' in domain_key:
                    return 'Instagram Reels'
                return platform
        
        return 'Unknown Platform'
    
    def _format_duration(self, duration):
        """Format duration in seconds to HH:MM:SS"""
        if not duration:
            return 'Unknown'
        
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def _format_filesize(self, size):
        """Format file size in bytes to human readable"""
        if not size:
            return 'Unknown'
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        
        return f"{size:.1f} TB"


def test_downloader():
    """Test the video downloader"""
    downloader = VideoDownloader()
    
    # Test URLs
    test_urls = [
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Rick Roll
        'https://youtu.be/jNQXAC9IVRw'  # Me at the zoo
    ]
    
    print("🎬 Testing Video Downloader")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\n🔍 Getting info for: {url}")
        info = downloader.get_video_info(url)
        
        if 'error' not in info:
            print(f"✅ Title: {info.get('title')}")
            print(f"📱 Platform: {info.get('platform')}")
            print(f"⏱️ Duration: {info.get('duration')}")
            print(f"👤 Uploader: {info.get('uploader')}")
            print(f"📺 Available qualities: {len(info.get('formats', {}).get('video', []))}")
        else:
            print(f"❌ Error: {info['error']}")
    
    print(f"\n🌐 Supported platforms: {len(downloader.get_supported_platforms())}")
    return downloader


if __name__ == "__main__":
    test_downloader()