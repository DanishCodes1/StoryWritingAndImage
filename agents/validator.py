from memory.state import GraphState
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import json

def validator_node(state: GraphState) -> GraphState:
    """
    Checks manually provided scripts for correct formatting and converts to JSON.
    """
    print("--- [AGENT: VALIDATOR] Checking manual script structure ---")
    
    raw_input = state.get("raw_input", "")
    
    # 1. Initialize the LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    # 2. Define the validation criteria [cite: 148-151]
    system_prompt = SystemMessage(
        content=(
            "You are a Script Validator Agent. "
            "Review the provided script and verify it contains: 1. Scene headers 2. Dialogue labels 3. Action structures. "
            "You MUST return the output ONLY as a valid JSON object. Do not include any conversational text, markdown, or code blocks. Use double quotes. "
            'If valid, return: {"scenes": [...]} '
            'If invalid, return: {"error": "explanation of what is missing"}'
        )
    )
    
    messages = [system_prompt, HumanMessage(content=raw_input)]
    
    try:
        # We tell the model we want JSON output
        response = llm.invoke(messages)
        # Parse the text response into a Python dictionary
        parsed_output = json.loads(response.content)
        
        if "error" in parsed_output:
            print(f"--- [AGENT: VALIDATOR] Script Rejected: {parsed_output['error']} ---")
            state["status"] = "validation_failed"
        else:
            print("--- [AGENT: VALIDATOR] Script Validated Successfully ---")
            state["script"] = parsed_output
            state["status"] = "validated"
            
    except Exception as e:
        print("--- [AGENT: VALIDATOR] Failed to parse script format. ---")
        state["status"] = "validation_failed"
        
    return state