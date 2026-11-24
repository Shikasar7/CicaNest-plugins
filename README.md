# CicaNest 插件市场

[CicaNest](https://github.com/Shikasar7/CicaNest) 的插件清单。在 nest 控制台的「插件」页最上面「插件市场」里填这个地址，就能看到这里的插件、看清它要什么权限，再决定装不装：

```
https://raw.githubusercontent.com/Shikasar7/CicaNest-plugins/main/index.json
```

nest 下载插件后会核对 `index.json` 里写的 sha256，再读一遍包里的 `plugin.json`，把它要的权限和技能全文给你看，你点「安装」才装。

## 目录

- `plugins/<插件 id>/`：每个插件的源文件，最上层是 `plugin.json`。
- `dist/`：打好的 zip（脚本生成，不要手改）。
- `index.json`：清单（脚本生成，不要手改）。
- `scripts/build_index.py`：把 `plugins/` 里的每个插件打成 zip，算 sha256，写出 `index.json`。

## 加一个插件

1. 在 `plugins/` 下新建一个文件夹，名字就是插件 id（`作者.名字`，小写字母、数字、点和 -；`nest.` 开头的留给 nest 自己）。
2. 写 `plugin.json` 和它提供的东西（技能是 `.md`，主题是 `.json`，桌宠是文件夹……格式见 CicaNest 的 `docs/plugins.md`）。
3. 运行 `python scripts/build_index.py`，把 `plugins/`、`dist/` 和 `index.json` 一起提交。
4. 改了插件就把 `version` 往上加，nest 会显示「能升级」。

## 信任等级

清单里的 `trust` 由插件提供的东西决定，nest 会按包里的实际内容再判断一次，取高的那个：

| 等级 | 意思 |
|---|---|
| content | 只有内容（主题、桌宠图片） |
| guides | 会指挥伙伴做事（技能、伙伴人设），装之前要看全文 |
| code | 有代码，在伙伴自己的容器里跑（MCP 工具） |
| trusted | 代码在 nest 进程里跑（模型、平台），只有你勾了「我信任它」才装 |

这里不收付费插件，也不做账号、评分和评论。
