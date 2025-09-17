from fastapi import FastAPI, Request, Response, HTTPException
import httpx
import os

app = FastAPI(title="Gateway", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


SERVICE_MAP = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth:8000"),
    "product": os.getenv("PRODUCT_SERVICE_URL", "http://product:8000"),
    "cart": os.getenv("CART_SERVICE_URL", "http://cart:8000"),
}


@app.middleware("http")
async def proxy_request(request: Request, call_next):
    path = request.url.path

    if path.startswith("/docs") or path.startswith("/openapi.json") or path.startswith("/redoc") or path.startswith("/health"):
        return await call_next(request)

    for prefix, svc_url in SERVICE_MAP.items():
        if path.startswith(f"/{prefix}"):
            target_url = svc_url.rstrip("/") + path[len(prefix) + 1:]

            async with httpx.AsyncClient() as client:
                forwarded = client.build_request(
                    method=request.method,
                    url=target_url,
                    headers=request.headers.raw,
                    params=request.query_params,
                    content=await request.body(),
                )
                resp = await client.send(forwarded, timeout=10.0)

                excluded_headers = {
                    "content-encoding",
                    "transfer-encoding",
                    "connection",
                    "keep-alive",
                    "proxy-authenticate",
                    "proxy-authorization",
                    "te",
                    "trailer",
                    "upgrade",
                }
                headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    headers=headers,
                    media_type=resp.headers.get("content-type"),
                )

    raise HTTPException(status_code=404, detail="Service not found")
