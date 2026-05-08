# AI Short Video Director Agent

一个可运行的「AI 短视频导演工作台」Demo。  
用户输入一句创意，系统通过 Multi-Agent Workflow 自动生成：

- Creative Brief
- 视频脚本
- 分镜设计
- 镜头字幕与旁白
- 图片 Prompt
- Timeline
- Storyboard 可视化预览数据

> 该项目默认支持 **Mock 模式**（未配置 API Key 也可完整运行）。

## 项目结构

```text
backend/
  app/
    agents/
    config.py
    llm_client.py
    orchestrator.py
    schemas.py
    mock.py
    main.py
frontend/
  src/
README.md
```

## 后端安装与启动

```bash
cd backend
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

Windows PowerShell 可使用：

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 前端安装与启动

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 `http://localhost:5173`。（一定要这个网址才能请求api）  
后端默认运行在 `http://localhost:8000`。

## API 说明

### `GET /health`

返回：

```json
{ "status": "ok" }
```

### `POST /api/generate`

请求：

```json
{
  "idea": "帮我生成一个赛博朋克风格的猫咪咖啡广告",
  "style": "商业广告",
  "aspect_ratio": "9:16"
}
```

响应：

```json
{
  "title": "xxx",
  "brief": {},
  "script": {},
  "storyboard": [],
  "review": {},
  "timeline": [],
  "render": {}
}
```

## OpenAI-compatible 配置

文件：`backend/app/config.py`

```python
class Settings:
    LLM_API_BASE_URL = "https://api.openai.com/v1"
    LLM_API_KEY = ""
    LLM_MODEL = "gpt-4o-mini"
```

也可通过环境变量覆盖：

- `LLM_API_BASE_URL`
- `LLM_API_KEY`
- `LLM_MODEL`

## Mock 模式

当 `LLM_API_KEY` 为空时：

- 自动进入 mock 模式
- 不调用外部模型 API
- 后端仍可完整返回 storyboard/timeline/preview 数据

主要用于演示

## Multi-Agent Workflow

执行顺序（由 `AgentOrchestrator` 编排）：

1. `CreativeDirectorAgent`
2. `ScriptWriterAgent`
3. `StoryboardAgent`
4. `VisualPromptAgent`
5. `ReviewAgent`
6. `RenderAgent`
