# distribute-llm-serving-system
it is distributed service system, it was seperated into different responsibilities and automatically expand the cache volumn. the point for this project is not to train the model, it is to make a api like openai, more industial and reusable, the target is not to train the model, and also manage the high cocurrency and load the balance. 

# Distributed LLM Serving (MVP)

把现成的大语言模型（LLM）**部署成在线推理服务**的工程练习项目。目标是做出一个**可运行、可观测、可扩展**的最小服务（类似 OpenAI 的接口形态），分阶段迭代实现。

> 本仓库目前处于 **Step 1：最小 API 网关**（仅健康检查），后续将逐步接入 vLLM、监控与压测。

---

## Roadmap（分阶段）

- [x] **Step 1：最小 FastAPI**（`/healthz` 健康检查，本地可跑）
- [ ] Step 2：`/chat` 接口（先回显/假响应，后接入 vLLM）
- [ ] Step 3：接入 vLLM OpenAI 兼容服务（本地/容器）
- [ ] Step 4：监控（Prometheus 指标、Grafana 看板）
- [ ] Step 5：压测（Locust/k6），记录 RPS / p95 / tokens/sec
- [ ] Step 6：限流/排队（admission control）、超时与重试
- [ ] Step 7：容器编排（Docker Compose），一键起所有组件

---

## Step 1

- 技术栈：FastAPI + Uvicorn
- 已实现接口：
  - `GET /healthz` → `{"ok": true}`（用于本地冒烟、LB/K8s 探活、部署验收）


## Step 2
1. stream还没配置--站位了
2./chat 接口测试 -ok
3. 交互文档 swagger ui -- /docs[fastapi 自动配的]
- 新增：
  - `POST /chat`（最小回显版，OpenAI 风格响应；为后续接 vLLM 做好响应契约）

## Step 3：接入 vLLM（Colab 上跑模型，本地 `/chat` 调用）

本步骤目标：  
让本地 FastAPI 的 `POST /chat` 不再回显，而是**通过 HTTP 调用 Colab 上的 vLLM 模型**，并把模型生成结果返回。  
接口形态与 **OpenAI 兼容**（路径与 JSON 结构尽量一致），便于后续复用任意 OpenAI 客户端/SDK。

---

### 3.1 在 Colab 启动 vLLM 并暴露端口

在 Colab Notebook 依次运行以下单元：

**(1) 安装依赖**
```python
!pip install vllm openai pyngrok


---
## 本地运行

> 需要 Python 3.10+

```bash
git clone <your-repo-url>
cd <repo-dir>

python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install fastapi uvicorn

uvicorn api_gateway.main:app --reload --port 8001






