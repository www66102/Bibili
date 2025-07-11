
import os
import time
import subprocess
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# === 配置 ===
KEYWORD = "病理学切片"
MAX_VIDEOS = 2
MAX_PAGES = 5
SAVE_PATH = "./病理学视频"
RECORD_FILE = "downloaded_bv.txt"

# === 初始化 ===
os.makedirs(SAVE_PATH, exist_ok=True)
if not os.path.exists(RECORD_FILE):
    open(RECORD_FILE, 'w', encoding='utf-8').close()

with open(RECORD_FILE, 'r', encoding='utf-8') as f:
    existing_bvs = set(line.strip() for line in f if line.strip())

# === 启动浏览器 ===
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 如需无头模式可取消注释
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

video_links = []
print("🔍 正在抓取 B站 视频链接...")

page = 1
encoded_keyword = urllib.parse.quote(KEYWORD)

while len(video_links) < MAX_VIDEOS and page <= MAX_PAGES:
    url = f"https://search.bilibili.com/all?keyword={encoded_keyword}&page={page}"
    print(f"\n第 {page} 页: {url}")
    driver.get(url)
    time.sleep(3)

    a_tags = driver.find_elements(By.CSS_SELECTOR, 'a[href*="video/BV"]')
    if not a_tags:
        print(f"第 {page} 页无视频链接，尝试下一页。")
        page += 1
        continue

    found_new = False
    for a_tag in a_tags:
        if len(video_links) >= MAX_VIDEOS:
            break
        try:
            link = a_tag.get_attribute('href')
            if not link:
                continue
            bv_id = link.split("video/")[1].split("?")[0]
            if bv_id not in existing_bvs and bv_id not in [x[0] for x in video_links]:
                video_links.append((bv_id, link))
                found_new = True
                print(f"新视频：{bv_id}")
            else:
                print(f"已下载或重复：{bv_id}")
        except Exception:
            continue

    if not found_new:
        print(" 本页无新视频，继续翻页...")

    page += 1

driver.quit()

print(f"\n共找到 {len(video_links)} 个新视频，准备下载...\n")

# === 下载视频 ===
for idx, (bv_id, link) in enumerate(video_links):
    print(f"[{idx+1}/{len(video_links)}] 🎬 正在下载: {bv_id}")
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
        continue

print("\n所有新视频处理完成，文件保存在：", os.path.abspath(SAVE_PATH))

