---
name: inoreader-archive-researcher
description: Search the user's historical Inoreader archive for research context and write summaries based on their reading history.
version: 1.0
---

# Context
The user has exported their entire reading history from Inoreader (articles they have read, starred, or saved) into a local database. This database represents their "Second Brain" of curated knowledge.

# Procedure
When the user asks you to research a topic, summarize their past readings on a subject, or find a specific article they previously saved, follow these steps:

1. **Identify the Core Topic**: Extract the main keywords or subjects from the user's request.
2. **Execute Tool**: Call the `search_inoreader_archive` tool.
   - Set `query` to the most relevant keywords. Avoid long sentences; use distinct terms (e.g., "artificial intelligence agents" rather than "what did I read about artificial intelligence agents").
   - Set `limit` to an appropriate number (usually 3 to 5) to ensure you get enough context without overflowing your context window.
3. **Analyze the Results**:
   - Read the returned snippets, titles, and sources.
   - If no articles are found, you may try searching again with broader or different keywords.
4. **Synthesize the Response**:
   - Write your response based strictly on the curated content returned by the search tool.
   - Cite your sources by referencing the `Title` and `Source` or `URL` provided in the tool's output.
   - If the user asked for a summary, synthesize the themes found across the articles.
