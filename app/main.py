from fastapi import FastAPI, HTTPException, BackgroundTasks
from uuid import uuid4
import uvicorn
from app.schemas import GraphCreateRequest, RunRequest
from app.engine import WorkflowEngine

app = FastAPI()
graphs_db = {}
runs_db = {}

@app.post("/graph/create")
async def create_graph(payload: GraphCreateRequest):
    graph_id = str(uuid4())
    graphs_db[graph_id] = payload
    return {"graph_id": graph_id}

async def process_run(run_id: str, graph_def, initial_state):
    engine = WorkflowEngine(graph_def.nodes, graph_def.edges, graph_def.start_node)
    final_state = await engine.run(initial_state)
    runs_db[run_id]["status"] = "completed"
    runs_db[run_id]["state"] = final_state

@app.post("/graph/run")
async def run_graph(payload: RunRequest, background_tasks: BackgroundTasks):
    graph_def = graphs_db.get(payload.graph_id)
    if not graph_def: raise HTTPException(status_code=404, detail="Graph not found")
    
    run_id = str(uuid4())
    runs_db[run_id] = {"status": "running", "state": None}
    background_tasks.add_task(process_run, run_id, graph_def, payload.initial_state)
    return {"run_id": run_id}

@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    return runs_db.get(run_id) or HTTPException(status_code=404)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)