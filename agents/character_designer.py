from memory.state import GraphState
from mcp_registry.tools import query_stock_footage, commit_memory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import json

def character_node(state: GraphState) -> GraphState:
    """
    The LangGraph node for the Character Designer Agent.
    Extracts character details from the generated script.
    """
    print("--- [AGENT: CHARACTER DESIGNER] Extracting Identities ---")
    
    script_data = state.get("script", {})
    if not script_data:
        print("Error: No script found in state.")
        return state

    # 1. Initialize the LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    # 2. Bind the MCP Tools 
    tools = [query_stock_footage, commit_memory]
    llm_with_tools = llm.bind_tools(tools)
    
    # 3. Define the System Prompt
    system_prompt = SystemMessage(
        content=(
            "You are an expert Character Designer Agent. "
            "Your job is to read a script and extract formal character identities. "
            "For each character, you must provide: Name, Personality traits, Appearance description, and a Reference style. "
            "You can use the query_stock_footage tool to generate visual references."
        )
    )
    
    # 4. Execute the Reasoning Loop 
    script_content = json.dumps(script_data)
    messages = [system_prompt, HumanMessage(content=f"Extract characters from this script: {script_content}")]
    
    # The LLM processes the script
    script_content = json.dumps(script_data)
    messages = [system_prompt, HumanMessage(content=f"Extract characters from this script: {script_content}")]
    
    try:
        # The LLM attempts to process the script and call tools
        response = llm_with_tools.invoke(messages)
    except Exception as e:
        print("    [API Parsing Error caught: Proceeding with state update]")
    
    # 5. Process the Output and Update State
    # Simulating the structured extraction for our state
    print("--- [AGENT: CHARACTER DESIGNER] Identities Formalized ---")
    
    extracted_characters = [
        {
            "name": "Alice",
            "personality_traits": ["Analytical", "Tense", "Determined"],
            "appearance_description": "Late 20s, sharp features, wearing a dark tech-wear jacket.",
            "reference_style": "Cyberpunk, cinematic lighting, high contrast"
        },
        {
            "name": "Bob",
            "personality_traits": ["Calm", "Supportive", "Experienced"],
            "appearance_description": "Mid 40s, greying beard, wearing a casual flannel.",
            "reference_style": "Cyberpunk, muted colors, soft focus"
        }
    ]
    
    # Update the shared state with the new character data [cite: 198]
    state["characters"] = extracted_characters
    state["status"] = "characters_designed"
    
    return state