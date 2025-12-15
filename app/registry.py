# --- Option A Tools ---
def extract_functions(state: dict) -> dict:
    code = state.get("code", "")
    state["functions"] = [f for f in code.split() if "def" in f]
    state["logs"].append(f"Extracted {len(state['functions'])} functions.")
    return state

def check_complexity(state: dict) -> dict:
    state["complexity_score"] = len(state.get("code", "")) // 10
    state["logs"].append(f"Complexity Score: {state['complexity_score']}")
    return state

def detect_issues(state: dict) -> dict:
    issues = []
    if state.get("complexity_score", 0) > 5:
        issues.append("Code is too verbose")
    state["issues"] = issues
    state["logs"].append(f"Issues found: {len(issues)}")
    return state

def suggest_improvements(state: dict) -> dict:
    current_score = state.get("quality_score", 0)
    # Increment score to ensure loop eventually breaks
    new_score = current_score + 20
    state["quality_score"] = min(100, new_score)
    state["logs"].append(f"Improvements applied. Quality Score: {state['quality_score']}")
    return state

TOOL_REGISTRY = {
    "extract_functions": extract_functions,
    "check_complexity": check_complexity,
    "detect_issues": detect_issues,
    "suggest_improvements": suggest_improvements
}

def get_tool(name: str):
    return TOOL_REGISTRY.get(name)