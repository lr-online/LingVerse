# 消息类型文档

以下文档定义了不同类型消息在 MongoDB 中的存储格式，详细说明了消息的核心字段：`message_type`、`content`、`media_url` 和 `metadata`。

---

## 1. 文本消息
**定义：** 文本消息用于存储纯文本内容。

| 字段          | 类型      | 描述                       |
|---------------|-----------|----------------------------|
| `message_type` | `"TEXT"` | 表示消息类型为文本          |
| `content`     | `string`  | 文本内容                   |
| `media_url`   | `null`    | 不适用                     |
| `metadata`    | `null`    | 不适用                     |

**示例：**
```json
{
  "message_type": "TEXT",
  "content": "Hello, how are you?",
  "media_url": null,
  "metadata": null
}

```

## 2. 音频消息

定义： 音频消息用于存储语音或音频文件的信息。

字段	类型	描述
message_type	"VOICE"	表示消息类型为音频
content	null	不适用
media_url	string	音频文件的存储地址
metadata	object	包含音频的附加信息，如时长和格式

示例：
```json
{
  "message_type": "VOICE",
  "content": null,
  "media_url": "https://example.com/audio/12345.mp3",
  "metadata": {
    "duration": 15,
    "format": "mp3"
  }
}
```

## 3. 视频消息

定义： 视频消息用于存储视频文件的信息。

字段	类型	描述
message_type	"VIDEO"	表示消息类型为视频
content	null	不适用
media_url	string	视频文件的存储地址
metadata	object	包含视频的附加信息，如时长和分辨率

示例：
```json
{
  "message_type": "VIDEO",
  "content": null,
  "media_url": "https://example.com/video/67890.mp4",
  "metadata": {
    "duration": 120,
    "resolution": "1920x1080",
    "format": "mp4"
  }
}
```

## 4. 图片消息

定义： 图片消息用于存储图片文件的信息。

字段	类型	描述
message_type	"IMAGE"	表示消息类型为图片
content	null	不适用
media_url	string	图片文件的存储地址
metadata	object	包含图片的附加信息，如宽高和格式

示例：
```json
{
  "message_type": "IMAGE",
  "content": null,
  "media_url": "https://example.com/image/12345.jpg",
  "metadata": {
    "width": 1080,
    "height": 720,
    "format": "jpg"
  }
}
```

## 5. 链接消息

定义： 链接消息用于存储超链接及其附加信息（如标题、描述和缩略图）。

字段	类型	描述
message_type	"LINK"	表示消息类型为链接
content	string	链接附加说明
media_url	string	链接地址
metadata	object	包含链接的附加信息，如标题和描述

示例：
```json
{
  "message_type": "LINK",
  "content": "Check out this article!",
  "media_url": "https://example.com/article",
  "metadata": {
    "title": "Exciting News",
    "description": "This is a short description of the linked article.",
    "thumbnail_url": "https://example.com/image/thumbnail.jpg"
  }
}
```

## 6. 卡片消息

定义： 卡片消息用于存储结构化信息，如事件邀请或按钮交互。

字段	类型	描述
message_type	"CARD"	表示消息类型为卡片
content	null	不适用
media_url	null	不适用
metadata	object	包含卡片的结构化信息，如标题和按钮

示例：
```json
{
  "message_type": "CARD",
  "content": null,
  "media_url": null,
  "metadata": {
    "title": "Event Invitation",
    "description": "You're invited to the annual company event.",
    "image_url": "https://example.com/image/event.jpg",
    "buttons": [
      {
        "text": "RSVP Now",
        "action_url": "https://example.com/rsvp"
      },
      {
        "text": "Learn More",
        "action_url": "https://example.com/event-details"
      }
    ]
  }
}
```

备注

1.	字段的使用规则：

- message_type 决定消息的类型和具体字段的使用。

- content 和 media_url 是互斥的，大多数情况下仅需要一个。

- metadata 用于扩展消息的附加信息，结构随消息类型变化。

2. 字段可选性：

- metadata 在部分消息类型中可能为 null，如文本消息。

- 媒体消息必须提供 media_url 和相关 metadata。

该文档定义了各类消息的核心字段及其适用场景，可用于开发和维护中对消息数据的管理。

