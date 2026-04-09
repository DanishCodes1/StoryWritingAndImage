from workflows.graph import app_workflow
from memory.state import GraphState
from dotenv import load_dotenv
import os

# Load environment variables (API keys)
load_dotenv()

def run_project_montage(input_mode: str, raw_input: str):
    print(f"\n=============================================")
    print(f"STARTING PROJECT MONTAGE - PHASE 1")
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
    print(f"WORKFLOW COMPLETE")
    print(f"Final Status: {final_state['status']}")
    print(f"Generated {len(final_state['characters'])} characters and {len(final_state['images'])} images.")
    print(f"=============================================\n")

if __name__ == "__main__":
    
    print("Choose Ingestion Mode:")
    print("1. Autonomous Generation (Scriptwriter)")
    print("2. Manual Script Injection (Validator)")
    choice = input("Enter 1 or 2: ")
    
    if choice == "1":
        # MODE 2: AUTO 
        user_prompt = "Write a short sci-fi scene where a robot discovers it has emotions."
        run_project_montage(input_mode="auto", raw_input=user_prompt)
        
    elif choice == "2":
        # MODE 1: MANUAL 
        # We simulate a raw script being uploaded by the user
        uploaded_script = """
        Scene 1: A dusty garage.
        Characters: Mechanic, Robot.
        Mechanic: Hand me the wrench.
        Robot: (Hands wrench, looking sad) My gears hurt.
        Action: The mechanic looks up in shock.
        """
        run_project_montage(input_mode="manual", raw_input=uploaded_script)