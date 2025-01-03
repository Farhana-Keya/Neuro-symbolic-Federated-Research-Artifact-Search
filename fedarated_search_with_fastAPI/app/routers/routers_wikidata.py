import sys


sys.path.append("..")
from fastapi import APIRouter
from app.common.util.decorators import log
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal
from app.services.services_wikidata import MetadataExtractionFromWikidata
router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class Quiz(BaseModel):
    # question: str
    Choice: Literal['Dataset', 'SoftwareApplication']

@router.post('/question_wikidata', status_code=200)
@log(__name__)
def search_question(Question,Type: Quiz = Depends()):
    # question = data.question
    wikidata_metadata = MetadataExtractionFromWikidata()
    try:
        # Use the service to extract key term and search OERSI
        response_data = wikidata_metadata.search_wikidata(str(Question),str(Type.Choice))
        return {"status": "success", "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# uvicorn main:app --reload

