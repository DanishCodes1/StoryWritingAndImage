from workflows.graph import app_workflow
from memory.state import GraphState
from dotenv import load_dotenv
import os

# Load environment variables (API keys)
load_dotenv()

def run_project_montage(input_mode: str, raw_input: str):
    print(f"\n=============================================")
    print(f"🚀 STARTING PROJECT MONTAGE - PHASE 1")
    print(f"Mode: {input_mode.upper()}")
    print(f"=============================================\n")
    
    # Initialize the starting state [cite: 192-200]
    initial_state: GraphState = {
        "input_mode": input_mode,
        "raw_input": raw_input,
        "script": {},
        "characters": [],
        "images": [],
        "status": "initialized"
    }

    # Execute the LangGraph workflow
    # LangGraph will automatically route this through the nodes we built!
    final_state = app_workflow.invoke(initial_state)
    
    print(f"\n=============================================")
    print(f"✅ WORKFLOW COMPLETE")
    print(f"Final Status: {final_state['status']}")
    print(f"Generated {len(final_state['characters'])} characters and {len(final_state['images'])} images.")
    print(f"=============================================\n")

if __name__ == "__main__":
    # Test Case 1: Autonomous Generation (Triggers Scriptwriter) [cite: 77-84]
    user_prompt = "Write a sci-fi thriller scene where two hackers infiltrate a secure server room to steal AI source code."
    run_project_montage(input_mode="auto", raw_input=user_prompt)
    
    # Note: To test manual mode, you would change input_mode to "manual" 
    # and pass the raw script text as raw_input. [cite: 68-76]