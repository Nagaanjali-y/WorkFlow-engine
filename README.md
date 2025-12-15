# Workflow Engine

A lightweight, backend-only workflow engine inspired by systems like LangGraph. [cite_start]This project allows you to define, connect, and execute Python functions ("Nodes") as a stateful graph workflow via HTTP APIs. [cite: 10, 11]

## 🚀 Features

[cite_start]This engine supports the core requirements of an agentic workflow: [cite: 15]

* [cite_start]**Nodes:** Standard Python functions that modify a shared state[cite: 16].
* [cite_start]**Edges:** Define the sequence of execution (which node runs next)[cite: 19].
* [cite_start]**Branching:** Conditional routing based on state values (e.g., if `score > 80`, go to End)[cite: 20].
* [cite_start]**Looping:** Cycles back to previous nodes until a condition is met (e.g., refine code until quality improves)[cite: 21].
* [cite_start]**State Management:** Passes a data dictionary between steps[cite: 17].

## 🛠️ Tech Stack

* [cite_start]**Language:** Python 3.9+ [cite: 4]
* [cite_start]**Framework:** FastAPI [cite: 29]
* [cite_start]**Storage:** In-memory dictionary (simulating a database) 

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Nagaanjali-y/WorkFlow-engine.git](https://github.com/Nagaanjali-y/WorkFlow-engine.git)
    cd WorkFlow-engine
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start the Server:**
    ```bash
    python -m app.main
    ```
    The server will start at `http://127.0.0.1:8000`.

## 📖 API Usage

You can interact with the API using **Swagger UI** at `http://127.0.0.1:8000/docs` or via **curl/Postman**.

### 1. Create a Workflow (Code Review Agent)
[cite_start]**POST** `/graph/create` [cite: 31]

[cite_start]This example creates a workflow that extracts functions, checks complexity, detects issues, and loops on "suggest_improvements" until the quality score is high enough[cite: 45, 50].

```json
{
  "name": "Code Review Agent",
  "nodes": ["extract_functions", "check_complexity", "detect_issues", "suggest_improvements"],
  "start_node": "extract_functions",
  "edges": [
    {"from_node": "extract_functions", "to_node": "check_complexity"},
    {"from_node": "check_complexity", "to_node": "detect_issues"},
    {"from_node": "detect_issues", "to_node": "suggest_improvements"},
    {
      "from_node": "suggest_improvements",
      "condition": {
        "key": "quality_score",
        "operator": ">=",
        "value": 80,
        "target_if_true": null,
        "target_if_false": "suggest_improvements"
      }
    }
  ]
}
