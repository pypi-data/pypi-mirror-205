<!-- markdownlint-disable MD033 MD036 MD041 -->

<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# NoneBot-Plugin-AutoReply

_✨ 自动回复 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/lgc2333/nonebot-plugin-autoreply.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-autoreply">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-autoreply.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<a href="https://pypi.python.org/pypi/nonebot-plugin-autoreply">
    <img src="https://img.shields.io/pypi/dm/nonebot-plugin-autoreply" alt="pypi download">
</a>
<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/3eb869b8-2edf-46dd-b325-916d9f8a4888">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/3eb869b8-2edf-46dd-b325-916d9f8a4888.svg" alt="wakatime">
</a>
</div>

## 🛒 回复市场

![market](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/autoreply/QQ截图20230423192951.png)

### [点击进入](https://autoreply.lgc2333.top)

我们的回复配置市场上线啦~  
在这里，你可以分享你的回复配置，也可以找到其他人分享的回复配置，欢迎各位使用！

_如果大家需要，我可以做一个直接使用指令下载安装市场中回复配置的功能 qwq_  
_想要的话就提个 issue 吧，没人想要的话就不做了（_

## 📖 介绍

一个简单的关键词自动回复插件，支持 模糊匹配、完全匹配 与 正则匹配，配置文件高度自定义  
因为商店里没有我想要的那种关键词回复，所以我就自己写了一个  
这个插件是从 [ShigureBot](https://github.com/lgc2333/ShigureBot/tree/main/src/plugins/shigure_bot/plugins/keyword_reply) 那边拆出来的，我重写了一下做成了单品插件

插件并没有经过深度测试，如果在使用中遇到任何问题请一定一定要过来发 issue 向我汇报，我会尽快解决  
如果有功能请求也可以直接发 issue 来 dd 我

## 💿 安装

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-autoreply
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-autoreply
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-autoreply
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-autoreply
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-autoreply
```

</details>

打开 nonebot2 项目的 `bot.py` 文件, 在其中写入

```py
nonebot.load_plugin('nonebot_plugin_autoreply')
```

</details>

## ⚙️ 配置

### 回复配置

插件的配置文件位于 `data/autoreply` 下  
在里面新建一个 `yml` 或 `json` 后缀文件即可开始配置

请根据下面的注释来编辑配置文件，实际配置文件内不要有注释

```jsonc
[
  {
    // 该组配置是否阻塞其他回复配置
    // 可以不填，默认为 `true`
    "block": true,

    // 该组配置的优先级，越大越高
    // 可以不填，默认为 1
    "priority": 1,

    // 消息的匹配规则，可以放置多个
    "matches": [
      {
        // 匹配模式，可选 `full`(完全匹配)、`fuzzy`(模糊匹配)、`regex`(正则匹配)、`poke`(双击头像戳一戳)
        //
        // 使用 `poke` 匹配时，除了 `possibility` 和 `to_me` 条件，其他的匹配条件都会被忽略
        // 注意：`poke` 会匹配所有戳一戳事件，如果你只想要匹配 Bot 被戳的事件，请将 `to_me` 设为 `true`
        //
        // 可以不填，默认为 `fuzzy`
        "type": "fuzzy",

        // 该匹配触发的概率，范围在 0 ~ 1 之间
        // 可以不填，默认为 1.0
        "possibility": 1.0,

        // 用于匹配消息的文本
        // 在正则匹配下，请使用 `\\` 在 json 里的正则表达式里表示 `\`，因为 json 解析时本身就会将 `\` 作为转义字符
        "match": "测试",

        // 是否需要 at 机器人才能触发（叫机器人昵称也可以）
        // 当匹配模式为 `poke` 时，只有 被戳 的对象是 Bot，事件才会匹配成功
        // 可以不填，默认为 `false`
        "to_me": false,

        // 是否忽略大小写
        // 可以不填，默认为 `true`
        "ignore_case": true,

        // 是否去掉消息前后的空格再匹配
        // 可以不填，默认为 `true`
        "strip": true,

        // 当带 cq 码的消息匹配失败时，是否使用去掉 cq 码的消息再匹配一遍
        // 可以不填，默认为 `true`
        "allow_plaintext": true
      },

      // 如果规则为一个字符串，则会转换为一个属性全部默认的 `match` 来匹配
      "测试2"

      // 更多匹配规则...
    ],

    // 匹配成功后，回复的消息
    // 如果有多个，将随机抽取一个回复
    "replies": [
      // type=normal 时，message 需要为字符串，会解析 message 中的 CQ 码并发送
      {
        "type": "normal",
        "message": "这是一条消息，可以使用CQ码[CQ:image,file=https://pixiv.re/103981177.png]"
      },

      // 直接写字符串也能表示 type=normal
      "这是一条消息，可以使用CQ码[CQ:image,file=https://pixiv.re/103981177.png]",

      // type=plain 时，message 需要为字符串，但是 message 中的 CQ 码不会被解析
      {
        "type": "plain",
        "message": "这条消息后面的CQ码会以原样发送[CQ:at,qq=3076823485]"
      },

      // 直接写 @ 开头的字符串也能表示 type=plain
      "@这条消息后面的CQ码也会以原样发送[CQ:at,qq=3076823485]",

      // type=array 时，message 中需要填 CQ 码的 json 格式
      {
        "type": "array",
        "message": [
          {
            "type": "text",
            "data": {
              "text": "我后面带了一张图片哦"
            }
          },
          {
            "type": "image",
            "data": {
              "file": "https://pixiv.re/103981177.png"
            }
          }
        ]
      },

      // 直接写数组也能代表 type=array
      [
        {
          "type": "text",
          "data": {
            "text": "我可以正常发送哦"
          }
        }
      ],

      // type=multi 时，message 需要为上面提到的消息类型的数组
      // 会按顺序发送 message 中的所有内容
      // message 中不允许嵌套其他的 type=multi 类型的回复
      {
        "type": "multi",
        // delay 是每条消息发送成功后的延时，格式为 [最低延时, 最高延时]
        // 单位为毫秒（1000 毫秒 = 1 秒），可以不填，默认为 [0, 0]
        "delay": [1000, 1000],
        "message": [
          "hello! 一会给你发张图哦~",
          "[CQ:image,file=https://pixiv.re/103981177.png]一会给你分享首歌哦awa~",
          [
            {
              "type": "music",
              "data": {
                "type": "163",
                "id": "2008994667"
              }
            }
          ]
        ]
      }

      // 更多消息...
    ],

    // 过滤指定群聊
    // 可以不填，默认为空的黑名单
    "groups": {
      // 黑名单类型，可选 `black`(黑名单)、`white`(白名单)
      "type": "black",

      // 要过滤的群号
      "values": [
        123456789, 987654321
        // 更多群号...
      ]
    },

    // 过滤指定用户
    // 可以不填，默认为空的黑名单
    "users": {
      // 黑名单类型，可选 `black`(黑名单)、`white`(白名单)
      "type": "black",

      // 要过滤的QQ号
      "values": [
        1145141919, 9191415411
        // 更多QQ号...
      ]
    }
  }

  // ...
]
```

插件提供了一些变量，他们可以被用在 `normal` 和 `array` 类型的消息，以及 `multi` 类型中嵌套的这两个类型的消息中；`plain` 类型的消息则无法使用变量  
变量使用 [`MessageTemplate.format_map()`](https://v2.nonebot.dev/docs/tutorial/message#%E4%BD%BF%E7%94%A8%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF) 方法替换

下面是插件提供的变量列表

- `{bs}` - “`{`”，转义用
- `{be}` - “`}`”，转义用
- `{self_id}` - 机器人 QQ
- `{message_id}` - 消息 ID _（当 `match` 的 `type` 为 `poke` 时为 `None`）_
- `{user_id}` - 发送者 QQ
- `{group_id}` - 消息来源群号 _（私聊等为 `None`）_
- `{target_id}` - 被戳者 QQ _（仅当 `match` 的 `type` 为 `poke` 时有值，其他情况为 `None`）_
- `{nickname}` - 发送者昵称
- `{card}` - 发送者群名片
- `{display_name}` - 发送者显示名称 _（优先群名片，当群名片为空时为昵称）_
- `{at}` - 艾特发送者
- `{reply}` - 回复发送者 _（当 `match` 的 `type` 为 `poke` 时为 `None`）_

下面放出几个示例，帮助大家更好的理解如何使用变量

```jsonc
[
  {
    "matches": [
      {
        "match": "^(@|at|艾特)我$",
        "type": "regex"
      }
    ],
    "replies": [
      // 在 normal 类型消息中使用
      "[normal] At了 [CQ:at,qq={user_id}]",

      // 在 array 类型消息中使用
      [
        {
          "type": "text",
          "data": {
            "text": "[array] At了 "
          }
        },
        {
          "type": "at",
          "data": {
            "qq": "{user_id}"
          }
        }
      ],

      // 在 multi 类型消息中使用
      {
        "type": "multi",
        "message": [
          // 嵌套的 array 类型消息
          [
            {
              "type": "at",
              "data": {
                "qq": "{user_id}"
              }
            }
          ],

          // 嵌套的 normal 类型消息
          "[multi] 我刚刚 At 了一下你哦~ 收到了吗？"
        ]
      },

      // 无法在 plain 类型消息中使用，{user_id}、{nickname} 会原样显示
      "@[plain] [CQ:at,qq={user_id}] 啊咧？怎么 At 不了 {nickname}？",

      // 可以在消息中使用 {bs｝ 和 {be} 来转义大括号
      // 前面的 {{user_id}} 会转义成 {user_id} 发送，而后面的 {nickname} 会被替换
      "[normal] [CQ:at,qq={bs}user_id{be}] 啊咧？怎么 At 不了 {nickname}？"
    ]
  }
]
```

### 常规配置

下方的配置皆为可选，如果不需要可以忽略不配置  
配置项请参考下面的文本

```ini
# matcher 是否阻断消息，默认 False
AUTOREPLY_BLOCK=False

# matcher 优先级
AUTOREPLY_PRIORITY=99
```

## 💬 指令

### `重载自动回复`

此命令用于重载自动回复配置，仅 `SUPERUSER` 可以执行

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💰 赞助

感谢大家的赞助！你们的赞助将是我继续创作的动力！

- [爱发电](https://afdian.net/@lgc2333)
- <details>
    <summary>赞助二维码（点击展开）</summary>

  ![讨饭](https://raw.githubusercontent.com/lgc2333/ShigureBotMenu/master/src/imgs/sponsor.png)

  </details>

## 📝 更新日志

### 0.2.8

- 支持解析 `yaml` 格式配置，会将 `.yml` 和 `.yaml` 的文件作为 `yaml` 格式配置加载
- 现在会寻找 `data/autoreply` 文件夹下所有子文件夹中的配置并加载
- 新增变量 `{at}`、`{reply}`
- 换用 `MessageTemplate` 格式化变量；由于这玩意不支持 `{{` 及 `}}` 转义，所以加入了变量 `{bs}` 和 `{be}`

### 0.2.7

- 新增了配置的 `block` 和 `priority` 属性
- 新增 `type` 为 `poke` (双击头像，戳一戳) 的 `match`
- 新增了 `match` 的 `possibility` 属性
- 新增了 `{target_id}` 与 `{display_name}` 变量

### 0.2.6

- 回复中可以使用变量了
- 新增配置市场

### 0.2.5

- 可以加载多个回复 Json

### 0.2.4

- 让字符串可以作为默认属性的 `match` 使用
- 让 `@` 开头的字符串 `reply` 解析为 `plain` 形式的回复

### 0.2.3

- 修复一处 py 3.8 无法使用的类型注解

### 0.2.2

- 修复群聊和用户过滤器无法正常使用的问题

### 0.2.1

- 修复多 `match` 无法使用的问题

### 0.2.0

- 使用 `rule` 匹配消息，避免日志刷屏
- 支持一次回复多条消息，调整配置文件结构
- 增加了两个 `.env` 配置项
- 增加热重载配置文件的指令
