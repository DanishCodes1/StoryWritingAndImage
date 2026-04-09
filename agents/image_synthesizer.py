from memory.state import GraphState
from mcp_registry.tools import query_stock_footage
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import json

def image_node(state: GraphState) -> GraphState:
    """
    The LangGraph node for the Image Synthesizer Agent.
    Generates image prompts based on character profiles and invokes the generation tool.
    """
    print("--- [AGENT: IMAGE SYNTHESIZER] Generating Visual References ---")
    
    characters = state.get("characters", [])
    if not characters:
        print("Error: No characters found to generate images for.")
        return state

    generated_images = []
    
    # Process each character individually
    for char in characters:
        print(f"Synthesizing image for character: {char['name']}...")
        
        # We manually construct a highly optimized prompt using the character's extracted traits
        image_prompt = f"Portrait of {char['name']}, {char['appearance_description']}, style of {char['reference_style']}"
        
        try:
            # THIS IS THE FIX: We explicitly execute the tool here to guarantee the download!
            filepath = query_stock_footage.invoke({"character_desc": image_prompt})
            generated_images.append(filepath)
        except Exception as e:
            print(f"    [Error executing tool for {char['name']}: {e}]")
    
    print("--- [AGENT: IMAGE SYNTHESIZER] Visuals Generated ---")
    
    # Update the Shared State
    state["images"] = generated_images
    state["status"] = "images_generated"
    
    return state