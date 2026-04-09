from memory.state import GraphState
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import json

def character_node(state: GraphState) -> GraphState:
    """
    The LangGraph node for the Character Designer Agent.
    Dynamically extracts character details from the generated script.
    """
    print("--- [AGENT: CHARACTER DESIGNER] Extracting Identities ---")
    
    script_data = state.get("script", {})
    if not script_data:
        print("Error: No script found in state.")
        return state

    # 1. Initialize the LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    # 2. Define the System Prompt with STRICT JSON rules
    # 2. Define the System Prompt with an OBJECT at the root
    system_prompt = SystemMessage(
        content=(
            "You are an expert Character Designer Agent. "
            "Read the provided script and extract formal character identities. "
            "You MUST return the output ONLY as a valid JSON object. Do not include any conversational text or markdown. "
            "You MUST use double quotes for all keys. Avoid using quotes inside the descriptions. "
            "Structure it exactly like this: "
            '{"characters": [{"name": "...", "personality_traits": ["...", "..."], "appearance_description": "...", "reference_style": "..."}]}'
        )
    )
    
    # 3. Execute the Reasoning Loop 
    script_content = json.dumps(script_data)
    messages = [system_prompt, HumanMessage(content=f"Extract characters from this script: {script_content}")]
    
    try:
        response = llm.invoke(messages)
        content = response.content.replace("```json", "").replace("```", "").strip()
        
        # Parse the JSON Object
        parsed_json = json.loads(content)
        
        # Extract the array from inside the "characters" key!
        extracted_characters = parsed_json.get("characters", [])
        
        print("--- [AGENT: CHARACTER DESIGNER] Identities Formalized ---")
        
        state["characters"] = extracted_characters
        state["status"] = "characters_designed"
        
    except Exception as e:
        print(f"--- [AGENT: CHARACTER DESIGNER] Failed to parse characters: {e} ---")
        state["status"] = "character_extraction_failed"
        
    return state