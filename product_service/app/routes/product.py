from fastapi import FastAPI
import httpx

router = FastAPI()

@router.post("/")
def create_product(...): ...
