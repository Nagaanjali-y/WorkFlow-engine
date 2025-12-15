import operator
from typing import Dict, Any, List, Optional
from app.schemas import Edge, Condition
from app.registry import get_tool

class WorkflowEngine:
    def __init__(self, nodes: List[str], edges: List[Edge], start_node: str):
        self.nodes = nodes
        self.edges = edges
        self.start_node = start_node

    def _evaluate_condition(self, state: Dict, condition: Condition) -> str:
        state_val = state.get(condition.key)
        target_val = condition.value
        ops = {">": operator.gt, "<": operator.lt, ">=": operator.ge, "<=": operator.le, "==": operator.eq}
        op_func = ops.get(condition.operator)
        
        if op_func and state_val is not None and op_func(state_val, target_val):
            return condition.target_if_true
        return condition.target_if_false

    async def run(self, initial_state: Dict[str, Any]):
        current_node = self.start_node
        state = initial_state.copy()
        if "logs" not in state: state["logs"] = []

        steps = 0
        while current_node and steps < 20:
            steps += 1
            tool_func = get_tool(current_node)
            if not tool_func: break
            
            try:
                state = tool_func(state)
            except Exception as e:
                state["logs"].append(f"Error: {str(e)}")
                break

            # Determine next node
            next_node = None
            relevant_edges = [e for e in self.edges if e.from_node == current_node]
            for edge in relevant_edges:
                if edge.condition:
                    next_node = self._evaluate_condition(state, edge.condition)
                    if next_node: break
                elif edge.to_node:
                    next_node = edge.to_node
                    break
            
            current_node = next_node

        return state