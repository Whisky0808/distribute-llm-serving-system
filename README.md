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
```


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



## Step 4: add basic observability (Prometheus metrics) to the API.
### Prometheus：
1. 为什么这很重要（特别是做分布式/LLM服务）

你可以 量化性能瓶颈：模型推理慢在哪、响应时间分布如何；

你能 自动报警：比如错误率 >5% 时触发告警；

你能 做容量规划：观察 QPS 与延迟变化关系，决定是否扩容 GPU 节点；

是所有 SRE（可观测性 / Observability）体系的基础层。

2. 一句话总结

Prometheus 指标就是你的程序对外暴露的“健康体检表”。
它告诉监控系统：我现在处理了多少请求、延迟多大、有没有报错。
后面接上 Prometheus + Grafana，你就能画出漂亮的监控图，看到 LLM 服务运行的真实状况。

- QPS（每秒请求数）

- 错误率

- 延迟（p50 / p95 / p99）

- CPU / 内存使用率

- 模型推理吞吐量

```bash
在项目根目录执行：

# Prometheus
docker run --name prometheus \
  -p 9090:9090 \
  -v "$PWD/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  prom/prometheus:latest

# 另开一个终端起 Grafana
docker run --name grafana \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  grafana/grafana:latest
```

打开：

Prometheus: http://localhost:9090
 （Status → Targets 看到 UP 就成功）
 

Grafana: http://localhost:3000
 （用户名 admin，密码 admin）
<img width="1530" height="805" alt="image" src="https://github.com/user-attachments/assets/8724eeaf-fb34-493d-8b31-dbc64d28c591" />


---



##Step 5
— Load Testing (Locust / k6): Record RPS / P95 / tokens per second

At this stage, use k6 or Locust to perform load testing on your core APIs to measure system performance under different levels of concurrency.

Key metrics to record:

RPS (Requests Per Second) — the number of successful requests processed per second, indicating system throughput.

P95 (95th Percentile Latency) — the response time below which 95 percent of requests complete, showing tail latency and user experience stability.

tokens/sec — for LLM or AI inference APIs, represents how many tokens are generated per second (model throughput).

These metrics provide a quantitative baseline for later optimization and capacity planning.

