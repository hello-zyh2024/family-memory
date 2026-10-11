# -*- coding: utf-8 -*-
"""相册内容。改这里就能改文案、调顺序、换图注，不需要动 app.py。

每张照片一个 dict：
    file     文件名，必须和 static/ 目录下的文件同名
    caption  图注
    note     可选，小字补充（按日期/时段之类的技术信息）
"""

HERO = {
    "file": "IMG_20240828_143708.jpg",
    "sub": "2024 · 夏 · 九寨沟",
}

INTRO = "2024 年夏末，一家人去了九寨沟。水是青的，云压得很低，我们走了很远的路。这里存着那几天里，我们在一起的样子。"

# 侧边栏的背景音乐。文件放 static/ 目录，留空则自动取该目录里的第一首音频。
MUSIC = {"file": "anheqiao.mp3", "title": "安和桥", "artist": "宋冬野"}

GROUPS = [
    {
        "date": "八月十七",
        "title": "清晨",
        "weather": "晴",
        "photos": [
            {
                "file": "IMG_20240817_073209.jpg",
                "caption": "夏末的一个晴日，抬头就是蓝天，我们挤在一起拍了张合照。",
            },
        ],
    },
    {
        "date": "八月廿五",
        "title": "一段录像",
        "weather": "夏",
        "video": "clip_20240825.mp4",
        "video_caption": "一分五十五秒。有些声音，照片是留不住的。",
        "video_note": "原片 272.9MB / 1080p，为放进仓库压成了 720p（19MB）。",
        "photos": [],
    },
    {
        "date": "八月廿六",
        "title": "熊猫基地",
        "weather": "晴",
        "photos": [
            {
                "file": "IMG_20240826_093646.jpg",
                "caption": "在去熊猫基地的路上，和“猴王”合了张影。",
            },
            {
                "file": "IMG_20240826_105308.jpg",
                "caption": "熊猫把整个下午都交给了睡意，就这么趴在木台上不动。",
            },
        ],
    },
    {
        "date": "八月廿七",
        "title": "九寨沟 · 山与彩池",
        "weather": "多云",
        "photos": [
            {
                "file": "IMG_20240827_145135.jpg",
                "caption": "站在半山的观景台上，背后是望不到头的青山。",
            },
            {
                "file": "IMG_20240827_145236.jpg",
                "caption": "站在木栈道上，身后是同一片山。",
            },
            {
                "file": "IMG_20240827_153806.jpg",
                "caption": "走累了就坐在栈道边歇一歇，水声一直在身后响着。",
            },
            {
                "file": "IMG_20240827_153814_1.jpg",
                "caption": "同行的几个人在栈道边坐成一排，等风把云吹薄一点。",
            },
            {
                "file": "IMG_20240827_154659.jpg",
                "caption": "在哗哗的水声旁站定，留下这一张。",
            },
            {
                "file": "IMG_20240827_154727.jpg",
                "caption": "云从山口漫下来，把半座山藏了进去。",
            },
            {
                "file": "IMG_20240827_155923.jpg",
                "caption": "水被一格格盛着，从浅蓝排到青绿。",
            },
            {
                "file": "IMG_20240827_155927.jpg",
                "caption": "同一片水，再走近一点，蓝得又不一样了。",
            },
            {
                "file": "IMG_20240827_171053.jpg",
                "caption": "水清得能看见底，岸边镶了一圈浅浅的黄。",
            },
            {
                "file": "IMG_20240827_175325.jpg",
                "caption": "低头看水，水底是另一片密密的绿。",
            },
        ],
    },
    {
        "date": "八月廿八",
        "title": "九寨沟 · 湖与瀑布",
        "weather": "晴",
        "photos": [
            {
                "file": "IMG_20240828_123443.jpg",
                "caption": "站在栏杆前，身后是一整片说不出颜色的湖水。",
            },
            {
                "file": "IMG_20240828_123501.jpg",
                "caption": "扶着栏杆站定，像是想把这片水记久一点。",
            },
            {
                "file": "IMG_20240828_123540.jpg",
                "caption": "包还背在肩上，先站下来拍一张。",
            },
            {
                "file": "IMG_20240828_123733.jpg",
                "caption": "山、树、云都安静下来，只剩下这一池水。",
            },
            {
                "file": "IMG_20240828_125044.jpg",
                "caption": "树影落在肩上，身后是正在落下的水。",
            },
            {
                "file": "IMG_20240828_125134.jpg",
                "caption": "水从苔藓间分作几股，落进底下那潭青色里。",
            },
            {
                "file": "IMG_20240828_132632.jpg",
                "caption": "天空倒映在水面上，中间隔着一层薄薄的水草。",
            },
            {
                "file": "IMG_20240828_143708.jpg",
                "caption": "整面崖壁都在往下流水，声音盖过了说话声。",
            },
        ],
    },
]


def all_photos():
    """按顺序拉平所有照片，返回 (全局序号, 所属分组, 照片) 三元组。"""
    out = []
    i = 0
    for group in GROUPS:
        for photo in group["photos"]:
            i += 1
            out.append((i, group, photo))
    return out


def total():
    return sum(len(g["photos"]) for g in GROUPS)
