from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/{path:path}")
async def proxy_auth(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.body()
        headers = dict(request.headers)
        res = await client.request(
            request.method, f"http://auth_service:8001/{path}",
            content=body, headers=headers
        )
        return Response(content=res.content, status_code=res.status_code)
