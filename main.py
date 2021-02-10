from upload import upload

config = {
    'desc': '简介', # 视频简介
    'tag': 'tag1,tag2,tag3', # 视频标签，用逗号分隔
    'tid': 65, # 视频分类序号
    'title': '标题', # 视频标题    
    'video_path': 'video.mp4', # 视频资源路径
    'cover_path': 'cover.png', # 封面图片路径
    'cookie': '', # cookie
}

# 运行此文件即可投稿
if __name__ == "__main__":
    ul = upload(config)
    ul.upload()