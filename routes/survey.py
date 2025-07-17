from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import csv

router = APIRouter(prefix="/api")

# פונקציית עזר אחידה
def save_to_csv(csv_path, row):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([f"Q{i+1}" for i in range(len(row))])  # כותרת רק אם חדש
        writer.writerow(row)


@router.post("/samsung/dfjd3432")
async def samsung_post(payload: dict):
    try:
        row = [payload.get(str(i)) for i in range(1, 5)]
        save_to_csv("other/samsung.csv", row)
        return {"message": "samsung post added successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/clalit/submit")
async def clalit_submit(payload: dict):
    try:
        answers = payload.get("answers", {})
        row = [answers.get(i) for i in range(1, 5)]
        save_to_csv("other/clalit_survey.csv", row)
        return {"message": "Survey responses added successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/agetest/submit")
async def age_test_submit(payload: dict):
    try:
        row = [payload.get("policy"), payload.get("playerid"), payload.get("timestamp")]
        save_to_csv("other/age.csv", row)
        return {"message": "Survey responses added successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/ceravesurvey/submit")
async def cerave_submit(payload: dict):
    try:
        answers = payload.get("answers", {})
        row = [
            answers.get(i) for i in range(1, 8)
        ] + [payload.get("isverified"), payload.get("isover13"), payload.get("playerid")]
        save_to_csv("other/d.csv", row)
        return {"message": "Survey responses added successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/galaxys25/submit")
async def galaxy_submit(payload: dict):
    try:
        answers = payload.get("answers", {})
        row = [
            answers.get(i) for i in range(1, 5)
        ] + [payload.get("isverified"), payload.get("isover13"), payload.get("playerid")]
        save_to_csv("other/galaxys25.csv", row)
        return {"message": "Survey responses added successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

