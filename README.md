# Inoreader Agent Skills

This repository contains skills and tools to integrate your AI agent (specifically designed for Hermes Agent framework) with your Inoreader account.

There are currently two distinct skills included:

## 1. Online Library Manager (API Based)
A skill that connects to the live Inoreader API, allowing the agent to save (star) or remove articles from your library on the fly.
* **Skill**: `inoreader-skill.md`
* **Tool**: `inoreader_skill.py`
* **Requires**: Inoreader Premium/Pro tier (for API access).
* **Setup**: Requires `INOREADER_APP_ID`, `INOREADER_APP_KEY`, and `INOREADER_ACCESS_TOKEN` in your environment.

## 2. Offline Library Search (JSON/SQLite Based)
A skill that allows the agent to search through your entire historical reading archive locally. This is perfect for Free Tier users who cannot access the live API, or for using your Inoreader history as a RAG (Retrieval-Augmented Generation) knowledge base for research.
* **Skill**: `inoreader-search-skill.md`
* **Tool**: `inoreader_search_tool.py`
* **Requires**: A JSON export of your Inoreader "Starred" or "Read" items.

### Setup for Offline Search:
1. Export your Inoreader data to a JSON file (e.g., `starred.json`).
2. Update the `JSON_FILE` path inside `inoreader_db_builder.py` to point to your downloaded file.
3. Run the database builder script to convert the JSON into a high-speed SQLite Full-Text Search database:
   ```bash
   python inoreader_db_builder.py
   ```
4. This will generate `inoreader_archive.db`. Ensure this file is accessible to your agent's environment.
5. Register `inoreader_search_tool.py` and `inoreader-search-skill.md` with your agent.

## General Agent Setup
- **Skills**: Drop the `.md` files into your agent's `skills` folder.
- **Tools**: Register the Python functions and JSON schemas in your agent's tool registry.
