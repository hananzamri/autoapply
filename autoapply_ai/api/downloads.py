from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/resume")
async def download_resume():
    return FileResponse(
        "generated/resume.pdf",
        filename="resume.pdf",
        media_type="application/pdf",
    )