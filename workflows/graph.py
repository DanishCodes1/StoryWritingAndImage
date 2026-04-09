from langgraph.graph import StateGraph, END
from memory.state import GraphState
from agents.scriptwriter import scriptwriter_node
from memory.vector_store import commit_state_to_db
from agents.validator import validator_node
from agents.hitl import hitl_node
# Add these two new imports:
from agents.character_designer import character_node
from agents.image_synthesizer import image_node
# --- STUBS FOR UNWRITTEN AGENTS ---
# We will fill these out in their respective files later.


def memory_commit_node(state: GraphState):
    # Call the actual DB function we just wrote
    updated_state = commit_state_to_db(state)
    return updated_state

# --- ROUTING LOGIC ---
# --- ROUTING LOGIC ---
def mode_selector(state: GraphState) -> str:
    """
    Decides the starting path based on user input mode.
    """
    # We return the actual input mode ("manual" or "auto") 
    # so LangGraph can find it in the conditional dictionary.
    return state.get("input_mode", "auto")

# --- GRAPH CONSTRUCTION ---
def build_workflow():
    # 1. Initialize the graph with our state schema
    workflow = StateGraph(GraphState)

    # 2. Add all the nodes (Agents) [cite: 183-191]
    workflow.add_node("scriptwriter", scriptwriter_node)
    workflow.add_node("validator", validator_node)
    workflow.add_node("hitl", hitl_node)
    workflow.add_node("character_designer", character_node)
    workflow.add_node("image_synthesizer", image_node)
    workflow.add_node("memory_commit", memory_commit_node)

    # 3. Define the Entry Point and Conditional Routing
    # The workflow starts by checking the input mode 
    workflow.set_conditional_entry_point(
        mode_selector,
        {
            "manual": "validator",
            "auto": "scriptwriter"
        }
    )

    # 4. Define the Edges (The Flow of the System)
    # Both paths converge at the Human-in-the-Loop checkpoint [cite: 114]
    workflow.add_edge("validator", "hitl")
    workflow.add_edge("scriptwriter", "hitl")
    
    # After human approval, it goes to the Character Designer [cite: 104-107]
    workflow.add_edge("hitl", "character_designer")
    
    # Character Designer passes info to Image Synthesizer [cite: 108-109]
    workflow.add_edge("character_designer", "image_synthesizer")
    
    # Finally, commit everything to memory [cite: 122-123]
    workflow.add_edge("image_synthesizer", "memory_commit")
    workflow.add_edge("memory_commit", END)

    # 5. Compile the graph
    return workflow.compile()

# You can use this compiled graph in your main.py!
app_workflow = build_workflow()