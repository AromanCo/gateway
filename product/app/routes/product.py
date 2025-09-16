from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead
from app.crud.product import create_product as crud_create_product, get_product_by_id

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new product in the database
    """
    product = await crud_create_product(db, product_in)
    return product


@router.get("/{product_id}", response_model=ProductRead)
async def read_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get product by ID
    """
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
