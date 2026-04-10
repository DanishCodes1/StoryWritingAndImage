PROJECT MONTAGE
Directory Structure
Plaintext
project_montage/
├── main.py                 # Core entry point and mode selector (Auto/Manual)
├── agents/                 # Agent node definitions and reasoning loops
├── mcp_registry/           # Dynamic tool discovery and execution (tools.py)
├── memory/                 # Vector DB commits and shared GraphState (state.py, vector_store.py)
├── workflows/              # LangGraph edge routing and compilation (graph.py)
└── output/                 # Generated deliverables
    ├── images/             # Visual character references (.png)
    ├── audio/              # Intermediate speech and sound files (.wav)
    └── raw_scenes/         # Final synchronized output files (.mp4)
Phases
Phase 1: The Writer's Room
Transforms raw human intent into a structured, machine-interpretable narrative representation. Operates as a sequential, stateful workflow with explicit Human-in-the-Loop approval and dynamic MCP tool discovery.

Agents: Scriptwriter, Validator, Character Designer, Image Synthesizer, HITL Checkpoint.

Deliverables: scene_manifest.json, character_db.json, Character Reference Images.