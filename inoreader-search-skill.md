---
name: inoreader-library-search
description: Searches the user's offline Inoreader library archive for research context.
version: 1.0
---

# Context
The user has exported their entire Inoreader saved items library to an offline SQLite database. This database contains all the articles they have read and starred, including the title, URL, and content snippets.

# Procedure
When the user asks you to research a topic, find an article they read, or summarize what they know about a subject, follow these steps:

1. **Identify the Query**: Extract the core search term or keyword from the user's request.
2. **Execute Tool**: Call the `search_library_archive` tool with the `query` parameter. You may optionally specify a `limit` if you need more or fewer results (default is 3).
3. **Synthesize**: Read the returned article titles and snippets. If they contain relevant information, synthesize that into your response. If not, state that you couldn't find anything relevant in their personal archive.
4. **Cite Sources**: Whenever you use information from the search results, cite the Article Title and URL so the user knows where the information came from.
