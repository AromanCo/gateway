from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate

async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    new_product = Product(**product_in.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.get(Product, product_id)
    return result
