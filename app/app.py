from fastapi import FastAPI
import json

app = FastAPI(title="Pitt CS Course Advisor - MCP Server")

@app.get("/courses")
def get_courses():
    with open("/api/mcp/course_data.json", "r") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)