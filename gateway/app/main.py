from fastapi import FastAPI, Request, Response, HTTPException
import httpx
import os

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


app = FastAPI()

# map of path prefix → service base URL (could load from env / config)
SERVICE_MAP = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth:8000"),
    "product": os.getenv("PRODUCT_SERVICE_URL", "http://product:8000"),
    "cart": os.getenv("CART_SERVICE_URL", "http://cart:8000"),
    # etc
}

@app.middleware("http")
async def proxy_request(request: Request, call_next):
    path = request.url.path
    for prefix, svc_url in SERVICE_MAP.items():
        if path.startswith(f"/{prefix}"):
            url = svc_url + path[len(prefix)+1:]  # adjust
            async with httpx.AsyncClient() as client:
                forwarded = client.build_request(
                    method=request.method,
                    url=url,
                    headers=request.headers.raw,
                    params=request.query_params,
                    content=await request.body()
                )
                resp = await client.send(forwarded, timeout=10.0)
                return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)
    # if no matching prefix
    raise HTTPException(status_code=404, detail="Service not found")