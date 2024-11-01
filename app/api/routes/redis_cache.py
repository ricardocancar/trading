# api/route/cache.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.redis_client import redis_client

router = APIRouter()



@router.post("/")
async def set_cache(key: str, value: dict):
    try:
        await redis_client.set(key, value)
        return {"message": "Value store in cache"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{key}")
async def get_cache(key: str):
    try:
        value = await redis_client.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="key not found")
        return {"key": key, "value": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{key}")
async def delete_cache(key: str):
    try:
        result = await redis_client.delete(key)
        if result == 0:
            raise HTTPException(status_code=404, detail="key not found")
        return {"message": "key was sucessfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
