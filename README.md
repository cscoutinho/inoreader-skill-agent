# Inoreader Agent Skill

This repository contains a skill and tool implementation designed to allow an AI Agent (e.g., using the Hermes Agent harness) to interact with a user's Inoreader library.

## Components

The architecture is split into two components:

1. **`inoreader-skill.md`**: The Procedural Memory (Skill). This markdown file teaches the agent *how* to save or remove an article from the Inoreader library. It outlines the procedure, determining if an article should be starred (saved) or unstarred (removed), and maps it to the tool execution.
2. **`inoreader_skill.py`**: The Deterministic Tool. This Python script implements the actual API request to Inoreader. It handles authentication and the network request to the `edit-tag` endpoint.

## Setup

1. **Agent Skill Registry**: Place `inoreader-skill.md` in your agent's `skills/` folder so it can learn the procedural workflow.
2. **Agent Tool Registry**: Expose the logic inside `inoreader_skill.py` to your agent using OpenAI-style JSON function calling. 
3. **Authentication**: You will need to supply three credentials to the Python tool:
   - `APP_ID`: Your Inoreader Developer App ID.
   - `APP_KEY`: Your Inoreader Developer App Key.
   - `ACCESS_TOKEN`: The user's OAuth 2.0 access token.

## How it Works

When a user asks to "save" an article, the agent loads the skill, figures out the necessary parameters, and executes the python tool, adding the system tag `user/-/state/com.google/starred` to the item in Inoreader.
