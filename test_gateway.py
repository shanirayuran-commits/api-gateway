import asyncio
import httpx
import time

GATEWAY_URL = "http://127.0.0.1:8000"
API_KEY = "secret-token-123"

async def test_request(client, name, body=None):
    headers = {"X-API-Key": API_KEY}
    try:
        if body:
            response = await client.post(f"{GATEWAY_URL}/test", headers=headers, content=body)
        else:
            response = await client.get(f"{GATEWAY_URL}/test", headers=headers)
        print(f"[{name}] Status: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"[{name}] Error: {e}")
        return None

async def run_tests():
    async with httpx.AsyncClient() as client:
        print("\n--- Testing API Key Validation ---")
        bad_headers = {"X-API-Key": "wrong-key"}
        resp = await client.get(f"{GATEWAY_URL}/test", headers=bad_headers)
        print(f"Wrong API Key: {resp.status_code} (Expected 401)")

        print("\n--- Testing Rate Limiting (Burst) ---")
        tasks = []
        for i in range(25):  # Burst is 20
            tasks.append(test_request(client, f"Req {i+1}"))
        
        results = await asyncio.gather(*tasks)
        success_count = results.count(200)
        limit_count = results.count(429)
        print(f"Burst Results: {success_count} Success, {limit_count} Rate Limited")

        print("\n--- Testing Body Size Limit (512KB) ---")
        large_body = "a" * (513 * 1024) # 513KB
        resp = await client.post(f"{GATEWAY_URL}/test", headers={"X-API-Key": API_KEY}, content=large_body)
        print(f"Large Body (513KB): {resp.status_code} (Expected 413)")

        small_body = "a" * (100 * 1024) # 100KB
        # Wait a bit for tokens to refill for the next success test
        print("Waiting 1s for refill...")
        await asyncio.sleep(1)
        resp = await client.post(f"{GATEWAY_URL}/test", headers={"X-API-Key": API_KEY}, content=small_body)
        print(f"Small Body (100KB): {resp.status_code} (Expected 200)")

if __name__ == "__main__":
    asyncio.run(run_tests())
