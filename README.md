# AI Chat Assistant

一个基于Deepseek API的现代化AI聊天助手，提供类似ChatGPT的用户体验，支持流式响应和对话历史管理。

## 🌟 特性

- **🤖 智能对话**: 基于Deepseek API的智能对话功能
- **⚡ 流式响应**: 支持实时流式响应，提供打字机效果
- **💾 对话历史**: 完整的对话历史管理和持久化存储
- **🔐 用户认证**: JWT认证系统，支持用户注册和登录
- **🎨 现代化UI**: 基于Vue 3的响应式用户界面
- **🚀 高性能**: FastAPI后端，支持异步处理和并发

## 📋 技术栈

### 后端
- **FastAPI** - 现代化Python Web框架
- **SQLAlchemy** - ORM数据库操作
- **SQLite** - 轻量级数据库（支持PostgreSQL）
- **JWT** - 用户认证
- **Deepseek API** - AI对话引擎

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 快速构建工具
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP客户端

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- npm 或 yarn

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/dayongchan/my-chat-assistant.git
cd my-chat-assistant
```

2. **后端设置**
```bash
cd backend

# 配置环境变量
cp .env.example .env
# 编辑.env文件，设置你的Deepseek API密钥

```

3. **前端设置**
```bash
cd ../frontend

# 安装依赖
npm install

# 配置API地址（如果需要）
# 编辑src/config.js中的API_BASE_URL
```

4. **启动服务**

**后端服务** (在backend目录下):
```bash
chmod +x start.sh
./start.sh
```

**前端服务** (在frontend目录下):
```bash
npm run dev
```

5. **访问应用**
- 前端地址: http://localhost:3000
- 后端API文档: http://localhost:8000/docs

## 🔧 配置说明

### 环境变量

在`backend/.env`文件中配置以下变量：

```env
# 数据库配置
DATABASE_URL=sqlite:///./assistant.db

# JWT配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# DeepSeek API配置
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_API_BASE=https://api.deepseek.com

# 应用配置
APP_NAME=AI Chat Assistant
DEBUG=True
```

### API密钥获取

1. 访问 [Deepseek开发者官网](https://platform.deepseek.com/)
2. 注册账号并获取API密钥
3. 在.env文件中配置`DEEPSEEK_API_KEY`

## 📁 项目结构

```
my-chat-assistant/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── database/       # 数据库配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   └── main.py         # 应用入口
│   ├── requirements.txt    # Python依赖
│   └── .env               # 环境变量
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── views/         # 页面视图
│   │   ├── store/         # 状态管理
│   │   ├── router/        # 路由配置
│   │   └── main.js        # 应用入口
│   └── package.json       # Node.js依赖
└── README.md              # 项目说明
```

## 🔌 API接口

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/refresh` - 刷新令牌

### 对话接口
- `GET /api/conversations` - 获取对话列表
- `POST /api/conversations` - 创建新对话
- `GET /api/conversations/{id}` - 获取对话详情
- `DELETE /api/conversations/{id}` - 删除对话
- `POST /api/conversations/{id}/messages` - 发送消息（支持流式响应）

### 流式响应
启用流式响应时，API会返回Server-Sent Events格式的数据流：

```json
{"type": "start", "user_message": {...}}
{"type": "chunk", "content": "Hello"}
{"type": "chunk", "content": " world"}
{"type": "end", "ai_message": {...}}
```

## 🎯 使用指南

### 基本使用

1. **注册/登录**: 首次使用需要注册账号
2. **创建对话**: 点击"新建对话"开始新的会话
3. **发送消息**: 在输入框中输入问题，支持流式响应
4. **管理历史**: 左侧面板查看和管理对话历史
5. **流式响应**: 启用后可以实时看到AI回复过程
6. **多会话管理**: 同时管理多个对话会话

### 未完成功能
1. **提示词工程**: 支持提示词，可以根据用户输入的关键词来提示AI的回答
2. **上下文管理**: 支持上下文管理，可以保存和加载上下文信息
3. **结果校验**: 支持结果校验，可以根据用户输入的关键词来校验AI的回答是否存在不适宜的内容
4. **AI模型选择**: 支持AI模型选择，可以选择不同的AI模型来回答问题
5. **AI模型训练**: 支持AI模型反馈训练，可以根据用户输入的反馈情况来对系统的提示词以及上下文进行优化及大模型微调

## 🐛 故障排除

### 常见问题

**Q: 后端启动失败**
A: 检查Python版本和依赖安装，确保虚拟环境已激活

**Q: 前端无法连接后端**
A: 检查后端服务是否运行在8000端口，CORS配置是否正确

**Q: API调用失败**
A: 检查Deepseek API密钥是否正确配置，网络连接是否正常

**Q: 数据库错误**
A: 检查数据库文件权限，或尝试删除数据库文件重新初始化

**Q: 是否使用AI技术**
A: 这个项目只是调用了Deepseek的API，暂时还没有使用AI相关的技术框架

### 日志查看

后端日志会显示详细的错误信息，包括API调用状态和数据库操作。

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发流程

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范

- 后端代码遵循PEP 8规范
- 前端代码使用ESLint和Prettier
- 提交信息使用约定式提交格式

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Deepseek](https://www.deepseek.com/) - 提供强大的AI API
- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的Python Web框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/dayongchan/my-chat-assistant/issues)
- 发送邮件至: admin@dayongchan.com

---

⭐ 如果这个项目对你有帮助，请给个Star！