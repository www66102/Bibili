# 配置文件

class Config:
    def __init__(self):
        self.platforms = ["bilibili", "youtube", "mooc"]
        self.output_dir = "output/"

    def get_platforms(self):
        return self.platforms

    def get_output_dir(self):
        return self.output_dir
