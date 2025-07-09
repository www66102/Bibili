from src.bilibili.scraper import BilibiliScraper

def main():
    # 配置参数
    keyword = "病理学切片"
    max_videos = 5
    save_path = "./output"
    record_file = "./Bilibili/downloaded_bv.txt"

    # 初始化爬取器
    scraper = BilibiliScraper(keyword, max_videos, save_path, record_file)

    # 执行爬取
    video_links = scraper.search_videos()
    print("爬取到的视频链接：")
    for link in video_links:
        print(link)

if __name__ == "__main__":
    main()