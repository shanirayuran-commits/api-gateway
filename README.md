# High-Concurrency API Gateway with Asyncio & Desktop UI

A professional-grade, high-performance API Gateway built with **Python 3.11+**, **FastAPI**, and **Asyncio**. It features a modern minimalist dark-themed desktop interface for real-time traffic monitoring and security management.

## 🚀 Key Features

- **High-Concurrency Engine**: Powered by `FastAPI` and `Uvicorn` for non-blocking I/O.
- **Token Bucket Rate Limiting**: Implements a sophisticated `AsyncTokenBucket` with burst capacity (20) and steady refill (2/s).
- **Security Suite**: 
  - Mandatory API Key validation via headers.
  - DDoS Protection: Rejects request bodies larger than **512KB**.
  - Silent Favicon handling.
- **Desktop Dashboard**: Minimalist dark UI built with `CustomTkinter` for real-time logging of **REQUEST** and **RESPONSE** cycles.
- **Protocol Translation**: Configured to proxy requests to the **GitHub API** with automatic header sanitization and User-Agent injection.

## 📸 Screenshots

![Desktop App Dashboard](screenshots/dashboard.png)
*Real-time monitoring of incoming requests and security status.*

![Authorized Request Success](screenshots/success_request.png)
*Successful proxy of a request to the GitHub API.*

![Unauthorized Block](screenshots/unauthorized_block.png)
*Gateway automatically blocking a request without a valid API Key.*

![Rate Limit Exceeded](screenshots/rate_limit.png)
*Token Bucket algorithm in action, limiting excessive traffic.*

## 🛠️ Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shanirayuran-commits/api-gateway.git
   cd api-gateway
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Gateway**:
   ```bash
   python desktop_app.py
   ```

4. **Test an Authorized Request**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/repos/python/cpython" -Headers @{"X-API-Key"="secret-token-123"}
   ```

## 🎓 Academic Concepts Implemented

- **Asynchronous Programming**: Utilizing Python's `asyncio` for scalable network operations.
- **Traffic Shaping**: Implementing the Token Bucket algorithm for fair resource allocation.
- **Middleware Pattern**: Decoupling security concerns from backend proxy logic.
- **Reverse Proxy Architecture**: Protecting internal/upstream services from direct public exposure.

---
Built as a Systems Architect demonstration.
