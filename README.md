# 智能旅行助手 🌍✈️

> 本项目改编自 [Datawhale](https://github.com/datawhalechina) 开源的 [Hello-Agents](https://github.com/datawhalechina/Hello-Agents) 项目，原项目采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可证。本项目在原作基础上将后端框架从 HelloAgents 改为 **LangChain**，并对 Agent 实现、API 层和前端进行了适配与优化。

基于LangChain框架构建的智能旅行规划助手,集成高德地图MCP服务,提供个性化的旅行计划生成。

## ✨ 功能特点

- 🤖 **AI驱动的旅行规划**: 基于LangChain框架的OpenAI格式,智能生成详细的多日旅程
- 🗺️ **高德地图集成**: 通过MCP协议接入高德地图服务,支持景点搜索、路线规划、天气查询
- 🧠 **智能工具调用**: Agent自动调用高德地图MCP工具,获取实时POI、路线和天气信息
- 🎨 **现代化前端**: Vue3 + TypeScript + Vite,响应式设计,流畅的用户体验
- 📱 **完整功能**: 包含住宿、交通、餐饮和景点游览时间推荐

##   演示

以苏州两日游为例:

### 首页 — 填写旅行信息

<img width="2552" height="1409" alt="首页" src="https://github.com/user-attachments/assets/9950cb14-04c7-4c6e-ad19-b25ab3e1d513" />


### 行程概览 — 总览与预算

<img width="2552" height="3269" alt="结果页" src="https://github.com/user-attachments/assets/c101cce0-766d-40a6-a811-262e87faf51c" />



## 🏗️ 技术栈

### 后端

- **框架**: LangChain、langchain-openai
- **API**: FastAPI
- **MCP工具**: amap-mcp-server (高德地图)
- **LLM**: 支持多种LLM提供商(OpenAI, DeepSeek等)

### 前端

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI组件库**: Ant Design Vue
- **地图服务**: 高德地图 JavaScript API
- **HTTP客户端**: Axios

## 📁 项目结构

```
LangChainTravelAgent/
├── backend/                          # 后端 - Python FastAPI 服务
│   ├── .env                          # 环境变量配置（API Key等）
│   ├── requirements.txt              # Python 依赖
│   ├── run.py                        # 应用启动入口
│   └── app/
│       ├── config.py                 # 配置管理（Pydantic Settings）
│       ├── agents/
│       │   └── trip_planner_agent.py # 多智能体旅行规划系统（景点/天气/酒店/行程）
│       ├── api/
│       │   ├── main.py               # FastAPI 应用实例 & 生命周期管理
│       │   └── routes/
│       │       ├── trip.py           # 旅行规划接口（POST /api/trip/plan）
│       │       ├── poi.py            # POI 查询接口（搜索/详情/图片）
│       │       └── map.py            # 地图服务接口（POI/天气/路线）
│       ├── models/
│       │   └── schemas.py            # Pydantic 请求/响应模型定义
│       ├── services/
│       │   ├── llm_service.py        # LLM 模型服务（OpenAI 兼容）
│       │   ├── amap_service.py       # 高德地图 MCP 服务封装
│       │   └── unsplash_service.py   # Unsplash 图片服务
│       └── tools/
│           └── mcp_agent.py          # MCP Agent（高德地图工具集成）
│
└── frontend/                         # 前端 - Vue 3 + TypeScript
    ├── .env                          # 前端环境变量（Vite 约定）
    ├── index.html                    # HTML 入口
    ├── package.json                  # Node.js 依赖
    ├── tsconfig.json                 # TypeScript 配置
    ├── vite.config.ts                # Vite 构建配置（含后端代理）
    └── src/
        ├── main.ts                   # Vue 应用入口 & 路由配置
        ├── App.vue                   # 根组件（全局布局）
        ├── services/
        │   └── api.ts                # Axios HTTP 客户端 & API 封装
        ├── types/
        │   ├── env.d.ts              # 环境变量类型声明
        │   └── index.ts              # TypeScript 接口定义
        └── views/
            ├── Home.vue              # 首页 - 旅行表单输入
            └── Result.vue            # 结果页 - 行程展示/地图/导出
```

## 🚀 快速开始

### 前提条件

- Python 3.10+
- Node.js 16+
- 高德地图API密钥 (Web服务API和Web端(JS API))
- LLM API密钥 (OpenAI/DeepSeek等)

### 后端安装

1. 安装python依赖

```bash
uv sync
```

2.配置环境变量

```bash
cp .env.example .env
# 编辑.env文件,填入你的API密钥
```

3.启动后端服务

```bash
uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端安装

1. 进入前端目录

```bash
cd frontend
```

2. 安装依赖

```bash
npm install
```

3. 配置环境变量

```bash
# 创建.env文件, 填入高德地图Web API Key 和 Web端JS API Key
cp .env.example .env
```

4. 启动开发服务器

```bash
npm run dev
```

5. 打开浏览器访问 `http://localhost:5173`

## 📝 使用指南

1. 在首页填写旅行信息:
   - 目的地城市
   - 旅行日期和天数
   - 交通方式偏好
   - 住宿偏好
   - 旅行风格标签

2. 点击"生成旅行计划"按钮

3. 系统将:
   - 调用LangChain Agent生成初步计划
   - Agent自动调用高德地图MCP工具搜索景点
   - Agent获取天气信息和路线规划
   - 整合所有信息生成完整行程

4. 查看结果:
   - 每日详细行程
   - 景点信息与地图标记
   - 交通路线规划
   - 天气预报
   - 餐饮推荐

## 🔧 核心实现

### MCP工具调用

Agent可以自动调用以下高德地图MCP工具:

- `maps_text_search`: 搜索景点POI
- `maps_weather`: 查询天气
- `maps_direction_walking_by_address`: 步行路线规划
- `maps_direction_driving_by_address`: 驾车路线规划
- `maps_direction_transit_integrated_by_address`: 公共交通路线规划

## 📄 API文档

启动后端服务后,访问 `http://localhost:8000/docs` 查看完整的API文档。

主要端点:

- `POST /api/trip/plan` - 生成旅行计划
- `GET /api/map/poi` - 搜索POI
- `GET /api/map/weather` - 查询天气
- `POST /api/map/route` - 规划路线

## 🤝 贡献指南

欢迎提交Pull Request或Issue!

## 📜 开源协议

本项目基于 [Datawhale/Hello-Agents](https://github.com/datawhalechina/Hello-Agents) 改编，原项目采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可证。

本改编作品同样采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议发布。

- **署名 (BY)** — 使用时请注明原作者 [Datawhale](https://github.com/datawhalechina) 及原项目 [Hello-Agents](https://github.com/datawhalechina/Hello-Agents)，并说明本项目所做的修改。
- **非商业性使用 (NC)** — 不得将本项目用于商业目的。
- **相同方式共享 (SA)** — 对本项目的改编或二次创作须以相同许可证发布。

