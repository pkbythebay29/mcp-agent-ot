# 🧠 mcp-agent-ot

**Multi-Agent Context Processor** for Operational Technology (OT) data.

Connects to industrial data sources (MQTT, OPC UA, Modbus), filters signals, embeds context into vector stores, and enables lightweight LLM-based Q&A — all using modular agents and Redis pub/sub.

---

## 🔧 Features

- 🛰️ Plug in **MQTT**, **OPC UA**, or **Modbus** sources
- 🔁 Agents run asynchronously (filtering, vectorizing, answering)
- 📦 Vector DB per zone using **FAISS**
- 🧠 Q&A using **MiniLM** (via `sentence-transformers`)
- 🌐 FastAPI dashboard to monitor messages and triggers
- 🧩 Modular, extensible, and modern Python packaging (`pyproject.toml`)

---

## 🚀 Quick Start

### 1. Clone the Repo

### 2. Install Dependencies

### 3. Start the system 

### 4. Start the dashboard 

- Open browser: http://localhost:8000

🔌 Configuring Data Sources

Edit mcpai/configs/data_sources.yml:

🧱 Architecture

    ingest_agent.py – connects to all OT sources dynamically

    filter_agent.py – identifies meaningful anomalies (e.g., "high temp")

    vector_agent.py – builds FAISS DB per zone

    llm_agent.py – answers based on vector context

    coordinator.py – starts everything

    dashboard.py – FastAPI UI

    redis_pubsub.py – pub/sub messaging layer
	
	

📄 License

MIT

🤝 Contributing

PRs and issues welcome. Designed to be extensible for edge computing and OT AI use cases.