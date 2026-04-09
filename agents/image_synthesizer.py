from memory.state import GraphState
from mcp_registry.tools import query_stock_footage
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

def image_node(state: GraphState) -> GraphState:
    """
    The LangGraph node for the Image Synthesizer Agent.
    Uses an LLM to dynamically discover and invoke the image generation tool.
    """
    print("--- [AGENT: IMAGE SYNTHESIZER] Generating Visual References ---")
    
    characters = state.get("characters", [])
    if not characters:
        print("Error: No characters found to generate images for.")
        return state

    # 1. Initialize the LLM (The "Brain")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    # 2. MCP Constraint: Bind the tool dynamically!
    llm_with_tools = llm.bind_tools([query_stock_footage])
    
    # 3. System Prompt
    system_prompt = SystemMessage(
        content=(
            "You are an expert Image Synthesizer Agent. "
            "Your job is to read a character profile and use the 'query_stock_footage' tool "
            "to generate a visual reference for them. Pass a highly descriptive prompt to the tool."
        )
    )

    generated_images = []
    
    # Process each character individually
    for char in characters:
        print(f"Synthesizing image for character: {char['name']}...")
        
        # We tell the LLM about the character, and let IT decide to use the tool
        char_details = f"Name: {char['name']}, Appearance: {char['appearance_description']}, Style: {char['reference_style']}"
        messages = [system_prompt, HumanMessage(content=f"Generate an image for this character: {char_details}")]
        
        try:
            # The LLM reasons and returns a "tool_call" request
            response = llm_with_tools.invoke(messages)
            
            # 4. Dynamically execute the tool the LLM discovered
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    if tool_call["name"] == "query_stock_footage":
                        # We pass the LLM's arguments dynamically into our tool
                        filepath = query_stock_footage.invoke(tool_call["args"])
                        generated_images.append(filepath)
            else:
                print(f"    [Agent failed to use the MCP tool for {char['name']}]")
                
        except Exception as e:
            print(f"    [Error during agent reasoning for {char['name']}: {e}]")
    
    print("--- [AGENT: IMAGE SYNTHESIZER] Visuals Generated ---")
    
    state["images"] = generated_images
    state["status"] = "images_generated"
    
    return state