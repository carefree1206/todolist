# 个人网站

一个现代化的个人网站，包含照片轮播、AI对话界面和社交媒体链接。

## ✨ 功能特性

### 📸 照片轮播
- 自动轮播功能（每4秒切换）
- 手动切换按钮（左右箭头）
- 指示器导航
- 鼠标悬停暂停
- 平滑过渡动画

### 💬 AI对话界面
- 类似OpenAI的聊天界面
- 智能对话回复
- 打字动画效果
- 响应式设计
- 支持常见问题识别

### 🔗 社交媒体链接
- 美观的社交图标展示
- 支持多个平台链接
- 悬停动画效果

### ✏️ 可视化编辑
- 直接在网页上编辑信息
- 无需修改代码
- 数据自动保存

## 🚀 快速开始

### 本地运行

1. **直接打开**
   - 双击 `index.html` 文件即可

2. **使用本地服务器（推荐）**
   ```bash
   # Python 3
   python -m http.server 8000
   
   # 然后访问 http://localhost:8000
   ```

### 部署到线上

查看 **[部署指南.md](./部署指南.md)** 了解详细部署步骤。

**快速推荐：**
- 🌐 **国内用户**：使用 [Gitee Pages](https://gitee.com)
- 🌍 **全球用户**：使用 [Vercel](https://vercel.com) 或 [Netlify](https://netlify.com)

## 📖 使用说明

### 编辑个人信息

1. 打开网站后，点击右下角的 **编辑按钮** ✏️
2. 在编辑面板中填写：
   - 你的名字
   - 副标题
   - 照片链接（可添加多个）
   - 社交媒体链接
3. 点击 **保存**，页面会自动更新

### 照片管理

**使用网络图片：**
- 在编辑面板中直接输入图片URL

**使用本地图片：**
1. 在网站文件夹创建 `images` 文件夹
2. 将照片放入 `images` 文件夹
3. 在编辑面板中输入：`images/你的照片.jpg`

### 支持的社交媒体

- GitHub
- LinkedIn
- Twitter
- Instagram
- Email
- Facebook
- YouTube
- 微信
- 微博

不填写链接的平台不会显示。

## 📁 文件结构

```
.
├── index.html          # 主HTML文件
├── style.css           # 样式文件
├── script.js           # JavaScript功能文件
├── README.md           # 说明文档
├── 部署指南.md         # 部署教程
├── 使用说明.md         # 详细使用说明
└── 快速开始.txt        # 快速参考
```

## 🛠️ 技术栈

- **HTML5** - 页面结构
- **CSS3** - 现代化样式和动画
- **JavaScript (ES6+)** - 交互功能
- **Font Awesome** - 图标库
- **Google Fonts** - 字体（自动回退到系统字体）

## 🌐 浏览器支持

- ✅ Chrome（推荐）
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ 移动端浏览器

## 💡 自定义

### 修改颜色主题

在 `style.css` 文件顶部的 `:root` 变量中修改：

```css
:root {
    --primary-color: #6366f1;  /* 主色 */
    --bg-color: #0f172a;      /* 背景色 */
    /* ... 其他颜色变量 */
}
```

### 集成真实AI API

如需集成真实的AI API（如OpenAI），可修改 `script.js` 中的 `ChatBot` 类的 `sendMessage()` 方法。

## 📝 注意事项

1. **数据保存**：所有修改保存在浏览器的 localStorage 中，清除缓存会丢失数据
2. **外部资源**：如果某些资源无法加载，网站会自动使用备选方案
3. **照片链接**：建议使用本地图片或可靠的图床服务

## 🤝 贡献

欢迎提交 Issue 或 Pull Request！

## 📄 许可证

MIT License - 可自由使用和修改

## 🙏 致谢

- [Font Awesome](https://fontawesome.com) - 图标库
- [Unsplash](https://unsplash.com) - 示例图片

---

**享受你的个人网站！** 🎉
