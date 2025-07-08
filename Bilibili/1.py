import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

KEYWORD = "病理学切片"
MAX_VIDEOS = 2
SAVE_PATH = "./病理学视频"
RECORD_FILE = "downloaded_bv.txt"  # 用于记录已下载过的 BV 号

# 创建保存目录和记录文件
os.makedirs(SAVE_PATH, exist_ok=True)
if not os.path.exists(RECORD_FILE):
    open(RECORD_FILE, 'w').close()

# 读取已记录的 BV 号
with open(RECORD_FILE, 'r', encoding='utf-8') as f:
    existing_bvs = set(line.strip() for line in f if line.strip())

# === 启动 Selenium 浏览器（可视化/取消注释改为无头）===
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

video_links = []
print("正在抓取视频链接...")

page = 1
while len(video_links) < MAX_VIDEOS:
    url = f"https://search.bilibili.com/all?keyword={KEYWORD}&page={page}"
    driver.get(url)
    time.sleep(3)

    cards = driver.find_elements(By.CLASS_NAME, 'bili-video-card__wrap')
    if not cards:
        break  # 没有更多结果了

    for card in cards:
        if len(video_links) >= MAX_VIDEOS:
            break
        try:
            a_tag = card.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')

            if "video/BV" in link:
                bv_id = link.split("video/")[1].split("?")[0]
                if bv_id not in existing_bvs:
                    video_links.append((bv_id, link))
        except Exception:
            continue
    page += 1

driver.quit()

print(f" 找到 {len(video_links)} 个新视频，准备下载...\n")

#下载视频
for idx, (bv_id, link) in enumerate(video_links):
    print(f"[{idx+1}/{len(video_links)}] 正在下载: {bv_id}")
    output_template = os.path.join(SAVE_PATH, "%(id)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-o", output_template,
        link
    ]
    try:
        subprocess.run(cmd, check=True)

        with open(RECORD_FILE, 'a', encoding='utf-8') as f:
            f.write(bv_id + '\n')
    except subprocess.CalledProcessError:
        print(f"下载失败: {bv_id}")

print("\n所有新视频处理完成，文件保存在：", os.path.abspath(SAVE_PATH))
