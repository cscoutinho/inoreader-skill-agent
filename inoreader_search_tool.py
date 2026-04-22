import sqlite3

def search_library_archive(query: str, limit: int = 3, db_path: str = "inoreader_archive.db") -> str:
    """
    Connects to the local SQLite database and performs a full-text search 
    on the user's historical Inoreader archive.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # SQLite Full-Text Search query
        sql = """
            SELECT title, url, content 
            FROM articles 
            WHERE articles MATCH ? 
            ORDER BY rank 
            LIMIT ?
        """
        
        cursor.execute(sql, (query, limit))
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return f"No articles found matching '{query}' in the archive."
            
        formatted_results = f"Found {len(results)} articles for '{query}':\n\n"
        for title, url, content in results:
            # We truncate the content slightly to save agent context tokens
            snippet = content[:800] + "..." if len(content) > 800 else content
            formatted_results += f"Title: {title}\nURL: {url}\nContent Snippet: {snippet}\n---\n"
            
        return formatted_results
        
    except sqlite3.Error as e:
        return f"Database error occurred: {e}"

# Tool Schema for Agent Registration
SEARCH_LIBRARY_SCHEMA = {
  "name": "search_library_archive",
  "description": "Searches the user's historical Inoreader archive for research context.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search term or keyword to look for in the article titles and contents."
      },
      "limit": {
        "type": "integer",
        "description": "Number of articles to return (max 5)."
      }
    },
    "required": ["query"]
  }
}
