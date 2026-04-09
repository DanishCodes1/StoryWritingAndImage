import chromadb
import json
import os

# Ensure the output directories exist for our JSON deliverables
os.makedirs("output/images", exist_ok=True)

# 1. Initialize ChromaDB client (Persistent storage saved to your hard drive)
chroma_client = chromadb.PersistentClient(path="./chroma_db_storage")

# 2. Create or get collections (think of these as SQL tables) for our data types
script_collection = chroma_client.get_or_create_collection(name="script_history")
character_collection = chroma_client.get_or_create_collection(name="character_metadata")

def commit_state_to_db(state: dict) -> dict:
    """
    Saves the final project state to the Vector DB and writes the JSON deliverables.
    """
    print("--- [MEMORY LAYER] Committing to Storage ---")

    # 1. Save the Script to ChromaDB
    if "script" in state and state["script"]:
        script_str = json.dumps(state["script"])
        script_collection.upsert(
            documents=[script_str],
            metadatas=[{"type": "scene_manifest", "mode": state.get("input_mode", "auto")}],
            ids=["latest_script_001"] # Upsert overwrites/updates the existing ID
        )
        
        # Deliverable: scene_manifest.json [cite: 212]
        with open("output/scene_manifest.json", "w") as f:
            json.dump(state["script"], f, indent=4)
        print("💾 Script saved to Vector DB and output/scene_manifest.json")

    # 2. Save Character Metadata to ChromaDB
    if "characters" in state and state["characters"]:
        for char in state["characters"]:
            char_str = json.dumps(char)
            character_collection.upsert(
                documents=[char_str],
                metadatas=[{"name": char["name"], "style": char["reference_style"]}],
                ids=[f"char_{char['name'].lower()}"]
            )
        
        # Deliverable: character_db.json [cite: 213]
        with open("output/character_db.json", "w") as f:
            json.dump(state["characters"], f, indent=4)
        print(f"💾 {len(state['characters'])} characters saved to Vector DB and output/character_db.json")

    state["status"] = "memory_committed"
    print("--- [MEMORY LAYER] Commit Complete ---")
    
    return state