# MNN Pocket 帮助与隐私

MNN Pocket 的公开使用帮助、隐私政策及相关说明。网站提供简体中文和英文，无需登录。

- [帮助中心](https://tangesion.github.io/mnn-chat/)
- [隐私政策](https://tangesion.github.io/mnn-chat/privacy/)
- [帮助与反馈](https://tangesion.github.io/mnn-chat/support/)
- [使用条款](https://tangesion.github.io/mnn-chat/terms/)
- [AI 使用须知](https://tangesion.github.io/mnn-chat/ai/)
- [联网服务说明](https://tangesion.github.io/mnn-chat/services/)

联系邮箱：tangesion@163.com

## 更新页面

`content/LegalDocuments-*.json` 保存与 App 同步的法律文案，`content/labels.json` 保存帮助页和标题文案。修改后运行：

```bash
python3 build.py
python3 check.py
```

将源文件和生成的 `docs/` 一起提交。GitHub Pages 使用 `main` 分支的 `/docs` 目录发布，`.nojekyll` 保留静态 HTML 输出。项目路径固定为 `/mnn-chat`，迁移或改名时需同步更新 `build.py` 中的 `BASE_PATH` 和 App 的页面链接。

这里仅提供静态文档。网站不自行添加统计脚本或反馈提交表单；邮件链接由访客自行发送。GitHub Pages 会为安全目的记录访问者 IP，详见隐私页面中单独的“本网站的访问”说明。
