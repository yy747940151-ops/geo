# 仪器营销文章工作台 · 封面修复试用版

这是从 [wechatsync/Wechatsync](https://github.com/wechatsync/Wechatsync) 开源项目固定提交 `42f61e39e214b8d5377d09d788a716defc4abdc0` 构建的个人测试版，非官方正式版本。

## 修复内容

1. **百家号**：先上传封面到百家号图床，再在保存草稿的请求里增加 `vertical_cover`、`cover_images`、`_cover_images_map` 和 `cover_layout` 参数。
2. **知乎**：将图片上传为知乎图片 URL，并在草稿更新 API 的 PATCH body 中加入 `titleImage` 和 `isTitleImageFullScreen: false`。
3. 其他平台（如搜狐号）保持上游代码不变。只调用现有的草稿接口，不调用公开发布接口。

## 安装步骤（只需一次）

1. 从 `https://yy747940151-ops.github.io/geo/downloads/wechatsync-cover-fix-v2.0.10.1.zip` 下载 ZIP 并解压。
2. 在 Chrome/Edge 的扩展管理页面关闭旧版文章同步助手，以免两套扩展互相抢占同步页面。
3. 开启开发者模式，点击 **加载已解压的扩展程序**，选择解压的文件夹（里面必须有 manifest.json）。
4. 不需要复制任何登录密码或 Cookie。依赖同一个浏览器里已登录的百家号、搜狐号、知乎状态。
5. 打开 `https://yy747940151-ops.github.io/geo/`，刷新网页并保存一篇文章到三个平台草稿，检查正文和封面是否都有。

## 状态及风险

- **已完成静态代码补丁；实际保存效果取决于平台当时的私有接口行为，未在账号中验证。**
- 新版扩展继承上游的广泛网站访问权限；只建议在信任源码和构建来源的前提下安装。
- 知乎、百家号后台的保存字段可能随平台更新而变更；如果平台拒绝封面设置，插件会报告错误，而不会直接公开发表文章。
- 如果测试不成功，可以关闭本测试扩展、重新启用原版，恢复原来正常的草稿同步。
