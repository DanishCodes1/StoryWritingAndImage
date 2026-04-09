from memory.state import GraphState

def hitl_node(state: GraphState) -> GraphState:
    """
    Pauses the workflow and asks for terminal input to approve the script.
    """
    print("\n=============================================")
    print("[HUMAN-IN-THE-LOOP] CHECKPOINT REACHED")
    print("=============================================")
    
    # If the validator failed the script, we don't bother asking the human.
    # If the validator OR the scriptwriter failed, we don't bother asking the human.
    if state.get("status") in ["validation_failed", "generation_failed"]:
        print(f"Skipping review because script status is: {state.get('status')}.")
        return state

    print("\n--- Current Script Data ---")
    # Print a quick preview of the script so the user knows what they are approving
    script_preview = str(state.get("script", {}))[:200] + "..."
    print(script_preview)
    print("---------------------------\n")
    
    # Actually pause the terminal and wait for user input
    user_approval = input("Do you approve this script to proceed to Character & Image generation? (y/n): ")
    
    if user_approval.lower().strip() == 'y':
        print("\n[HUMAN-IN-THE-LOOP] Script Approved. Continuing workflow...")
        state["status"] = "human_approved"
    else:
        print("\n[HUMAN-IN-THE-LOOP] Script Rejected. Halting workflow.")
        # In a more advanced graph, this could route back to the scriptwriter to rewrite it.
        # For Phase 1, we just update the status to show it was rejected.
        state["status"] = "human_rejected"
        # We wipe the script so downstream nodes don't process it
        state["script"] = {} 
        
    return state