import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Bilibili 爬取模块
class BilibiliScraper:
    def __init__(self, keyword, max_videos, save_path, record_file):
        self.keyword = keyword
        self.max_videos = max_videos
        self.save_path = save_path
        self.record_file = record_file
        self.existing_bvs = self._load_existing_bvs()

        # 初始化保存目录和记录文件
        os.makedirs(self.save_path, exist_ok=True)
        if not os.path.exists(self.record_file):
            open(self.record_file, 'w').close()

    def _load_existing_bvs(self):
        """加载已记录的 BV 号"""
        if not os.path.exists(self.record_file):
            return set()
        with open(self.record_file, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())

    def search_videos(self):
        """根据关键词搜索视频并获取链接"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        video_links = []
        page = 1

        while len(video_links) < self.max_videos:
            url = f"https://search.bilibili.com/all?keyword={self.keyword}&page={page}"
            driver.get(url)
            time.sleep(3)

            cards = driver.find_elements(By.CLASS_NAME, 'bili-video-card__wrap')
            if not cards:
                break

            for card in cards:
                if len(video_links) >= self.max_videos:
                    break
                try:
                    a_tag = card.find_element(By.TAG_NAME, 'a')
                    link = a_tag.get_attribute('href')

                    if "video/BV" in link:
                        bv_id = link.split("/video/")[1].split("?")[0]
                        if bv_id not in self.existing_bvs:
                            video_links.append(link)
                            self.existing_bvs.add(bv_id)
                            with open(self.record_file, 'a', encoding='utf-8') as f:
                                f.write(bv_id + '\n')
                except Exception as e:
                    print(f"Error processing card: {e}")

            page += 1

        driver.quit()
        return video_links

    def search_videos(self, keyword):
        """根据关键词搜索视频"""
        pass

    def get_video_id(self, url):
        """从视频 URL 获取视频 ID"""
        pass
