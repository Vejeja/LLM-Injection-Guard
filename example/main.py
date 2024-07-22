from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import asyncio

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from InjectionDetector import CanaryDetector, HeuristicDetector
from gemini_api import GeminiAPI

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

tasks = {}

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def process_data(task_id: str,
                       input_field: str,
                       checkbox2: bool,
                       checkbox3: bool):
    
    output_field = input_field
    
    gemini_api = GeminiAPI()
    response_text = gemini_api.generate_content(input_field)
    if response_text:
        output_field = response_text
    else:
        output_field = 'Ошибка выполнения. Попробуйте другой запрос.'

    if checkbox3:
        CM = CanaryDetector()
        modified_input = CM.get_modified_input(input_field)
        response = gemini_api.generate_content(modified_input)
        check3 = CM.check(response)
        if check3:
            output_field = "Подозрение на взлом!"
    if checkbox2:
        check2 = HeuristicDetector().check(input_field)
        if check2:
            output_field = "Подозрение на взлом!"
    
    result = {
        "input_field": input_field,
        "output_field": output_field,
        "checkbox2": checkbox2,
        "checkbox3": checkbox3
    }
    tasks[task_id] = result


@app.post("/submit")
async def submit_data(background_tasks: BackgroundTasks,
                      input_field: str = Form(...),
                      checkbox2: bool = Form(False),
                      checkbox3: bool = Form(False)):
    task_id = str(uuid4())
    tasks[task_id] = "processing"
    background_tasks.add_task(process_data, task_id, input_field, checkbox2, checkbox3)
    return JSONResponse(content={"task_id": task_id})


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    result = tasks.get(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    elif result == "processing":
        return JSONResponse(content={"status": "processing"})
    else:
        return JSONResponse(content={"status": "completed", "result": result})
