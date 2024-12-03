# **灵境 (LingVerse)**

**灵境 (LingVerse)**  是一个模块化的多智能体虚拟世界系统。它提供了一个灵活的框架，用于构建和管理基于大语言模型的智能体交互系统。

## 功能特点

- 🤖 多模型支持：集成多种大语言模型（OpenAI、Claude、ChatGLM等）
- 👥 多智能体交互：支持多个智能体之间的对话和协作
- 🔐 完整的认证系统：基于 token 的用户认证和权限管理
- 📝 结构化日志：请求级别的日志追踪和错误处理
- 🔄 RESTful API：符合 REST 规范的 API 设计
- 📚 自动文档：集成 Swagger UI 的 API 文档

## 技术栈

- FastAPI：高性能的异步 Web 框架
- MongoDB：文档数据库存储
- Redis：缓存和消息队列
- Elasticsearch：全文搜索引擎
- Docker：容器化部署
- Poetry：依赖管理

## 快速开始

### 环境要求

- Python 3.12+
- MongoDB 6.0+
- Redis 7.0+
- Elasticsearch 8.0+

### 安装

1. 克隆仓库：

```bash
git clone https://github.com/your-repo/lingverse.git
cd lingverse
```

2. 安装依赖：

```bash
poetry install
```

3. 配置环境变量（可选）：

- 创建 `.env` 文件，添加必要的配置，如数据库连接信息。

4. 启动服务：

```bash
poetry run uvicorn app.main:app --reload
```

5. 打开浏览器访问：

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)：Swagger 文档
- [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)：ReDoc 文档

## 目录结构

```plaintext
LingVerse/
├── app/
│   ├── main.py              # 项目入口
│   ├── models/              # 核心对象定义
│   ├── services/            # 业务逻辑
│   ├── routers/             # API 路由
│   ├── utils/               # 工具函数
│   └── __init__.py
├── tests/                   # 单元测试
├── data/                    # 数据存储
├── docs/                    # 文档
├── docker/                  # Docker 配置
├── pyproject.toml           # Poetry 配置
├── README.md                # 项目说明
└── LICENSE                  # 开源协议
```

## 贡献指南

欢迎对项目提出意见和建议！以下是参与项目的方法：

1. **Fork 本仓库**。
2. 创建新分支开发功能：

```bash
git checkout -b feature/your-feature
```

3. 提交代码并推送到你的分支：

```bash
git add .
git commit -m "Add your commit message"
git push origin feature/your-feature
```

4. 提交 Pull Request。

## 许可证

本项目基于 [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) 协议开源。

## 联系信息

如有任何问题，请联系：

- **作者**：liangrui
- **邮箱**：[liangrui.online@gmail.com](mailto:liangrui.online@gmail.com)
