
<h1 align="center">High-Concurrency API Gateway</h1>
<h3 align="center">Asyncio • FastAPI • Desktop UI Dashboard</h3>

<p align="center">
A professional-grade, high-performance API Gateway built with <b>Python 3.11+</b>, <b>FastAPI</b>, and <b>Asyncio</b>.
Includes a modern minimalist dark-themed desktop interface for real-time traffic monitoring and security management.
</p>

<p align="center">
  <a href="#-key-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-installation--usage">Installation</a> •
  <a href="#-academic-concepts-implemented">Concepts</a> •
  <a href="#-screenshots">Screenshots</a>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-Framework-009688?style=flat&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Asyncio-Concurrency-111111?style=flat&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Uvicorn-ASGI_Server-222222?style=flat&logo=gunicorn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Desktop_UI-CustomTkinter-1f1f1f?style=flat&logo=windows&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat"/>
</p>

---

## 🚀 Key Features

- **High-Concurrency Engine**: Powered by `FastAPI` and `Uvicorn` for non-blocking I/O.
- **Token Bucket Rate Limiting**: Implements a sophisticated `AsyncTokenBucket` with burst capacity (20) and steady refill (2/s).
- **Security Suite**
  - Mandatory API Key validation via request headers.
  - DDoS Protection: Rejects request bodies larger than **512KB**.
  - Silent favicon handling.
- **Desktop Dashboard**: Minimalist dark UI built with `CustomTkinter` for real-time logging of **REQUEST** and **RESPONSE** cycles.
- **Protocol Translation**: Configured to proxy requests to the **GitHub API** with automatic header sanitization and User-Agent injection.

---

## 🛠 Tech Stack

### 🔥 Languages & Frameworks
<p align="left">
  <img src="https://skillicons.dev/icons?i=python,fastapi" />
</p>

### ⚙ Libraries & Tools
- **Python 3.11+**
- **FastAPI** (High-performance async API framework)
- **Uvicorn** (ASGI server)
- **Asyncio** (Concurrency + non-blocking scheduling)
- **CustomTkinter** (Modern dark desktop UI)
- **Token Bucket Algorithm** (Rate limiting engine)
- **Proxy Middleware Logic** (Header sanitization + request forwarding)

---

## 🛠️ Installation & Usage

### 1️⃣ Clone the repository
```bash
git clone https://github.com/shanirayuran-commits/api-gateway.git
cd api-gateway
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Launch the Gateway

```bash
python desktop_app.py
```

### 4️⃣ Test an Authorized Request

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/repos/python/cpython" -Headers @{"X-API-Key"="secret-token-123"}
```

---

## 🎓 Academic Concepts Implemented

* **Asynchronous Programming**: Leveraging Python `asyncio` for scalable network operations.
* **Traffic Shaping**: Token Bucket algorithm ensures fair request distribution under load.
* **Middleware Pattern**: Security and rate limiting decoupled from core proxy logic.
* **Reverse Proxy Architecture**: Protects upstream services from direct exposure and abuse.
* **High-Concurrency System Design**: Optimized request pipeline for non-blocking throughput.

---

## 📸 Screenshots

<details>
  <summary><b>Click to View Screenshots</b></summary>

  <br>

  <p align="center">
    <img src="screenshots/dashboard.png" width="850"/>
  </p>
  <p align="center"><i>Real-time monitoring of incoming requests and security status.</i></p>

  <br>

  <p align="center">
    <img src="screenshots/success_request.png" width="850"/>
  </p>
  <p align="center"><i>Successful proxy of a request to the GitHub API.</i></p>

  <br>

  <p align="center">
    <img src="screenshots/unauthorized_block.png" width="850"/>
  </p>
  <p align="center"><i>Gateway automatically blocking a request without a valid API Key.</i></p>

  <br>

  <p align="center">
    <img src="screenshots/rate_limit.png" width="850"/>
  </p>
  <p align="center"><i>Token Bucket algorithm in action, limiting excessive traffic.</i></p>

</details>

---

<p align="center">
  <b>Built as a Systems Architect demonstration.</b>
</p>
```
