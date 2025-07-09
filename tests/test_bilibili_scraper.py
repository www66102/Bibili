# 测试 Bilibili 爬取模块

import unittest
from src.bilibili.scraper import BilibiliScraper

class TestBilibiliScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = BilibiliScraper()

    def test_search_videos(self):
        """测试搜索视频功能"""
        self.assertIsNone(self.scraper.search_videos("test"))

    def test_get_video_id(self):
        """测试获取视频 ID 功能"""
        self.assertIsNone(self.scraper.get_video_id("https://www.bilibili.com/video/test"))

if __name__ == "__main__":
    unittest.main()
