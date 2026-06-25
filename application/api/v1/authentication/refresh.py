from fastapi import APIRouter

router = APIRouter()


@router.post("/refresh")
async def refresh():
    return {"detail": None}
