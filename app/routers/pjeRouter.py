from fastapi import APIRouter, HTTPException
from app.service.scrapyPjeService import read_excel
router = APIRouter(
    prefix="/pje"
)

@router.get("/read-excel")
def get_init():
    read_excel()
    return 123


