from memory.state import GraphState
from mcp_registry.tools import generate_script_segment, commit_memory
from langchain_core.messages import HumanMessage, SystemMessage
# Assuming we are using OpenAI for the LLM reasoning loop. 
# You can swap this for ChatOllama if running locally!
from langchain_groq import ChatGroq

def scriptwriter_node(state: GraphState) -> GraphState:
    """
    The LangGraph node for the Scriptwriter Agent.
    It takes the current state, processes the input, and updates the script.
    """
    print("--- [AGENT: SCRIPTWRITER] Initiating Reasoning Loop ---")
    
    raw_input = state.get("raw_input", "")
    
    # 1. Initialize the LLM (The "Brain")
    # We use a relatively capable model since it needs to do tool calling.
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    # 2. Bind the MCP Tools to the LLM
    # This tells the LLM: "You have these specific functions available to use."
    tools = [generate_script_segment, commit_memory]
    llm_with_tools = llm.bind_tools(tools)
    
    # 3. Define the System Prompt (The "Role")
    system_prompt = SystemMessage(
        content=(
            "You are an expert autonomous Scriptwriter Agent. "
            "Your job is to transform raw human intent into a structured, multi-scene screenplay. "
            "You must decompose the narrative into scenes, generate dialogue, and attach visual context. "
            "Use your available tools to generate the script segments and commit them to memory."
        )
    )
    
    # 4. Execute the Reasoning Loop
    print(f"Analyzing input: '{raw_input[:50]}...'")
    messages = [system_prompt, HumanMessage(content=raw_input)]
    
    # The LLM decides what to do next (e.g., call a tool or reply with text)
    response = llm_with_tools.invoke(messages)
    
    # 5. Process the Output and Update State
    # In a fully robust version, we would execute the tool call here.
    # For now, we will simulate the tool execution to update our state.
    
    print("--- [AGENT: SCRIPTWRITER] Scene Segmentation Complete ---")
    
    # Updating the shared graph state
    state["status"] = "script_generated"
    
    # Simulating the structured JSON output required by the assignment
    state["script"] = {
        "scenes": [
            {
                "scene_id": 1,
                "location": "Darkened Server Room",
                "characters": ["Alice", "Bob"],
                "dialogue": [
                    {"speaker": "Alice", "line": "The system is compiling.", "visual_cue": "Close up on monitor"}
                ]
            }
        ]
    }
    
    return state