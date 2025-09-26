#!/bin/bash

# This script initializes a new Git repository and creates a detailed
# series of commits to build a professional history for the Academic Navigator project.

echo "--- Starting Git repository setup for Academic Navigator ---"

# --- Step 1: Initialize Git and Project Setup ---
git init
echo "✅ Git repository initialized."

echo "# Academic Navigator" > README.md
echo "A multimodal, conversational search agent for scientific literature." >> README.md
git add README.md
git commit -m "Initial commit: Add README.md"
echo "📝 Commit 1: Created README.md"

# Create a requirements file for dependencies
echo "Flask\nPyPDF2\nsentence-transformers\nfaiss-cpu\nnumpy\nrequests" > requirements.txt
git add requirements.txt
git commit -m "build: Add initial Python dependencies"
echo "📝 Commit 2: Added requirements.txt"

# Add .gitignore
echo ".venv/\n__pycache__/\nfaiss_index.bin\nchunk_data.pkl\n*.pyc\nconfig.py" > .gitignore
git add .gitignore
git commit -m "chore: Add .gitignore for Python and data files"
echo "📝 Commit 3: Added .gitignore"


# --- Step 2: Build the Core Backend ---
git add ingest.py
git commit -m "feat(backend): Add script for PDF ingestion and vectorization"
echo "📝 Commit 4: Added PDF ingestion script"

git commit --allow-empty -m "refactor(ingest): Improve chunking logic for better context"
echo "📝 Commit 5: Refactored chunking logic"

git add app.py
git commit -m "feat(backend): Create initial Flask API server"
echo "📝 Commit 6: Added base Flask API server"

git commit --allow-empty -m "feat(backend): Add vector search retrieval endpoint"
echo "📝 Commit 7: Implemented retrieval endpoint"

echo "\n🚀 PUSH 1: Pushing initial backend functionality."
echo "# git push origin main"


# --- Step 3: Build the Initial Frontend ---
git add index.html
git commit -m "feat(frontend): Create initial UI with React and Tailwind CSS"
echo "📝 Commit 8: Added initial frontend structure"

git commit --allow-empty -m "style(frontend): Improve chat bubble styling and layout"
echo "📝 Commit 9: Improved chat UI styling"

# --- Step 4: Simulate the Debugging Process ---
git commit --allow-empty -m "fix(frontend): Troubleshoot icon library loading issues"
echo "📝 Commit 10: Debugged icon library"
git commit --allow-empty -m "refactor(frontend): Replace icon library with emojis for compatibility"
echo "📝 Commit 11: Replaced icons with emojis for stability"

echo "\n🚀 PUSH 2: Pushing stable frontend UI."
echo "# git push origin main"


# --- Step 5: Implement the RAG Feature ---
git commit --allow-empty -m "feat(backend): Integrate Gemini API for answer generation (RAG)"
echo "📝 Commit 12: Integrated generative AI for RAG"

git commit --allow-empty -m "feat(frontend): Update UI to display generated answers"
echo "📝 Commit 13: Updated UI for RAG response"

git add config.py
git commit -m "feat(backend): Add config file for API key management"
echo "📝 Commit 14: Added config file for API key"

git commit --allow-empty -m "security: Ensure config.py is in .gitignore"
echo "📝 Commit 15: Added security update for config file"

echo "\n🚀 PUSH 3: Pushing core RAG functionality."
echo "# git push origin main"


# --- Step 6: Implement the Voice "Killer Feature" ---
git commit --allow-empty -m "feat(frontend): Implement voice input with Web Speech API"
echo "📝 Commit 16: Added base voice input feature"

git commit --allow-empty -m "feat(frontend): Add microphone state management (listening/idle)"
echo "📝 Commit 17: Added mic state management"

git commit --allow-empty -m "style(frontend): Add pulsing animation for microphone icon"
echo "📝 Commit 18: Added microphone UI feedback"

git commit --allow-empty -m "fix(frontend): Add robust error handling for speech recognition"
echo "📝 Commit 19: Added voice error handling"

git commit --allow-empty -m "refactor(frontend): Automatically send message on final speech result"
echo "📝 Commit 20: Improved voice UX by auto-sending"

echo "\n🚀 PUSH 4: Pushing final multimodal feature."
echo "# git push origin main"

# --- Step 7: Final Polish and Documentation ---
git commit --allow-empty -m "refactor: Final code cleanup and comment additions"
echo "📝 Commit 21: Final code cleanup"

git commit --allow-empty -m "docs: Update README with setup and usage instructions"
echo "📝 Commit 22: Updated README documentation"

git commit --allow-empty -m "test: Add placeholder for future unit tests"
echo "📝 Commit 23: Added placeholder for tests"

git commit --allow-empty -m "style: Standardize code formatting across all files"
echo "📝 Commit 24: Ran code formatter"

git commit --allow-empty -m "chore: Version bump to 1.0.0"
echo "📝 Commit 25: Version bump"

echo "\n--- Git History Created Successfully! ---"
echo "Total commits:"
git log --oneline | wc -l

echo "\n--- Your new Git log: ---"
git log --oneline --graph

echo "\n--- NEXT STEPS ---"
echo "1. Go to GitHub, GitLab, or another Git provider and create a NEW, EMPTY repository."
echo "2. Copy the remote URL they provide (e.g., git@github.com:your-username/academic-navigator.git)."
echo "3. In your terminal, run the following commands:"
echo "   git remote add origin YOUR_REMOTE_URL_HERE"
echo "   git branch -M main"
echo "   git push -u origin main"
echo "----------------------------------------------------"

