from fastapi import FastAPI
from pydantic import BaseModel
from browser_use import Agent, Browser, ChatGoogle
import os

app = FastAPI()

class TaskRequest(BaseModel):
    task: str

@app.post("/run")
async def run_browser_task(request: TaskRequest):
    # Map the environment variable for ChatGoogle
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

    # Using the official wrapper and your preferred 500 RPD model
    llm = ChatGoogle(model='gemini-3.1-flash-lite')

    # Configure Browser directly (BrowserConfig was deprecated and removed)
    browser = Browser(
        headless=False, # Allowed now because of xvfb in Docker
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage'
        ]
    )

    agent = Agent(
        task=request.task,
        llm=llm,
        use_vision=False, # Keeping this to make it lightning fast
        browser=browser   # Attaching our stealth browser
    )

    result = await agent.run()

    # Close the browser to prevent memory leaks in the Docker container
    await browser.close()

    return {"result": result.final_result()}
