# **灵境 (LingVerse)**

**版本：0.1.0**

**灵境 (LingVerse)** 是一个基于多智能体系统的虚拟世界构建平台，旨在通过类人化交互单元（`Person`）、动态记忆管理、模型切换与工具整合，打造一个独立于现实的智能交互系统。该系统采用模块化设计，具备高效性、扩展性和个性化服务能力，适用于多种任务处理与智能场景交互。

---

## **功能特点**
- **类人化交互**：基于 `Person` 对象，模拟个性化、多功能智能交互单元。
- **动态记忆管理**：支持交互记录的存储、检索与智能遗忘机制。
- **模型切换与工具整合**：根据任务复杂度动态切换模型，并支持自定义工具的扩展。
- **模块化架构**：便于功能扩展与维护。

---

## **技术栈**
- **后端框架**：FastAPI
- **服务运行**：Uvicorn
- **数据库**：MongoDB、Redis
- **开发工具**：Poetry（依赖管理）、Black（代码格式化）、Isort（导入排序）

---

## **安装与运行**

### **前置要求**
1. Python 版本 >= 3.12
2. 安装 Poetry
3. MongoDB 和 Redis 数据库服务可用

### **安装步骤**
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

---

## **目录结构**
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

---

## **贡献指南**
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

---

## **许可证**
本项目基于 [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) 协议开源。

---

## **联系信息**
如有任何问题，请联系：
- **作者**：liangrui
- **邮箱**：[liangrui.online@gmail.com](mailto:liangrui.online@gmail.com)
