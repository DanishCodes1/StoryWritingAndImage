from memory.state import GraphState
from mcp_registry.tools import generate_script_segment, commit_memory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import json

def scriptwriter_node(state: GraphState) -> GraphState:
    print("--- [AGENT: SCRIPTWRITER] Initiating Reasoning Loop ---")
    
    raw_input = state.get("raw_input", "")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    tools = [generate_script_segment, commit_memory]
    llm_with_tools = llm.bind_tools(tools)
    
    system_prompt = SystemMessage(
        content=(
            "You are an expert autonomous Scriptwriter Agent. "
            "Write a multi-scene screenplay based on the user's prompt. "
            "You MUST return the output ONLY as a valid JSON object. Do not include any conversational text, markdown formatting, or code blocks. "
            "You MUST use double quotes for all keys and string values. Structure it exactly like this: "
            '{"scenes": [{"scene_id": 1, "location": "...", "characters": ["A"], "dialogue": [{"speaker": "A", "line": "...", "visual_cue": "..."}]}]}'
        )
    )
    
    messages = [system_prompt, HumanMessage(content=raw_input)]
    
    try:
        # We tell the model we want JSON output
        response = llm.invoke(messages)
        
        # ---> ADD THIS CLEANING LINE <---
        # This strips out markdown formatting if the LLM gets chatty
        content = response.content.replace("```json", "").replace("```", "").strip()
        
        # Parse the CLEANED text response into a Python dictionary
        parsed_output = json.loads(content)
        
        if "error" in parsed_output:
            print(f"--- [AGENT: VALIDATOR] Script Rejected: {parsed_output['error']} ---")
            state["status"] = "validation_failed"
        else:
            print("--- [AGENT: VALIDATOR] Script Validated Successfully ---")
            state["script"] = parsed_output
            state["status"] = "validated"
            
    except Exception as e:
        print(f"--- [AGENT: VALIDATOR] Failed to parse script format: {e} ---")
        state["status"] = "validation_failed"
        
    return state