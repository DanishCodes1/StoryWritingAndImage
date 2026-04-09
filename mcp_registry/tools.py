from langchain_core.tools import tool
from typing import List, Dict

# --- Tool 1: For the Scriptwriter Agent ---
@tool
def generate_script_segment(prompt: str, num_scenes: int) -> List[Dict]:
    """
    Generates a structured script segment based on an abstract prompt.
    Use this to break down a narrative into scenes, dialogues, and visual cues.
    """
    # Note: In a full implementation, this would call an LLM. 
    # For now, we return a mock structure matching the required standard.
    print(f"[Tool Execution] Generating {num_scenes} scenes for prompt: '{prompt}'")
    
    return [
        {
            "scene_id": 1,
            "location": "City street - Night",
            "characters": ["A", "B"],
            "dialogue": [
                {"speaker": "A", "line": "We must act now", "visual_cue": "Close-up, tense lighting"}
            ]
        }
    ]

# --- Tool 2: For the Character Designer & Image Synthesizer ---
import urllib.request
import urllib.parse
import os

@tool
def query_stock_footage(character_desc: str) -> str:
    """
    Queries an image synthesis engine to generate a visual reference.
    """
    print(f"[Tool Execution] Generating real image for: '{character_desc[:30]}...'")
    
    # Create a safe filename
    safe_name = abs(hash(character_desc))
    filepath = f"output/images/{safe_name}_reference.png"
    
    # Use Pollinations.ai 
    encoded_prompt = urllib.parse.quote(character_desc)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    try:
        os.makedirs("output/images", exist_ok=True) 
        
        # THE FIX: Add a standard User-Agent header so the server doesn't block us as a bot
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Download and save the image manually
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
            
        print(f"    -> Successfully saved image to {filepath}")
        return filepath
    except Exception as e:
        print(f"    -> Failed to download image: {e}")
        return "Failed to generate image."
@tool
def commit_memory(data_type: str, payload: dict) -> str:
    """
    Commits stateful data (scripts, character metadata, etc.) to the shared Vector DB.
    """
    print(f"[Tool Execution] Committing {data_type} to Vector DB...")
    # This is where your ChromaDB or FAISS logic would go
    return "Memory successfully committed."

# List of all tools to be registered with the MCP server
AVAILABLE_TOOLS = [generate_script_segment, query_stock_footage, commit_memory]