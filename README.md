# 家的记忆

一个给家里人看的相册。2024 年夏末，一家人去九寨沟的几天：出发前、成都熊猫基地、九寨沟的山与钙华彩池、湖与瀑布。

- 21 张照片 + 1 段两分钟的录像
- 按日期分成时间轴
- 点任意一张照片看大图
- 留言板

## 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。

## 目录结构

```
app.py               主程序
photo_data.py        相册内容：日期分组、图注、顺序都在这里改
static/              照片和视频（Streamlit 静态资源目录）
.streamlit/config.toml   主题配色 + 静态资源服务开关
```

想改文案或调整顺序，只需要动 `photo_data.py`，不用碰 `app.py`。

## 几个实现上的说明

**图片是怎么加载的。** 不是把图片转成 base64 塞进 HTML，而是开了 Streamlit 的
`server.enableStaticServing`，让 `static/` 目录以 `app/static/<文件名>` 的路径直接
对外提供。好处是浏览器能正常懒加载和缓存；21 张图转 base64 会让页面体积从 8MB
涨到 11MB 且完全无法缓存。

**点击看大图是怎么做的。** Streamlit 1.64 的 `st.image` 没有 `on_select` 参数，
做不了点击事件。这里用的是纯 CSS：一组隐藏的 `<input type="radio">`，靠
`:checked` 状态加兄弟选择器控制全屏覆盖层的显隐，不需要 JavaScript，也不会改动
URL（避免和 Streamlit 自己的路由打架）。

这个方案有个硬性结构要求：**覆盖层必须和 radio 同父、且排在所有 radio 之后**，
否则 `~` 选择器匹配不到。所以每组照片墙是一次性生成整块 HTML 的，不能拆开渲染。

**视频为什么只有 720p。** 原片是手机竖拍的 1080×1920、码率 19.9 Mbps、272.9MB。
GitHub 单文件硬上限 100MB，Streamlit 静态服务上限 200MB，两个都超。转码后
720×1280、19MB，画质在手机和电脑上看不出差别。

**字体没用 Google Fonts。** 中文字体动辄几 MB，而且国内访问 `googleapis.com`
经常不通。标题用的是系统自带的楷体（Windows 和 macOS 都有），正文走系统无衬线字体。

## 已知限制

- **留言板存在 `guestbook.json` 里，而 Streamlit Community Cloud 的硬盘是临时的。**
  应用重启或重新部署时留言会清空。要长期保存得接外部存储。
- 页面宽度、聊天气泡等样式依赖 Streamlit 的 class 名，Streamlit 大版本升级后
  可能有出入。
