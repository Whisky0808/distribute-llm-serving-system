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

## 当前状态（Step 1）

- 技术栈：FastAPI + Uvicorn
- 已实现接口：
  - `GET /healthz` → `{"ok": true}`（用于本地冒烟、LB/K8s 探活、部署验收）

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
