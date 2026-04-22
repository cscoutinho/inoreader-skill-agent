import sqlite3
import os

def search_inoreader_archive(query: str, limit: int = 3) -> str:
    """
    Connects to the local SQLite database and performs a full-text search on the Inoreader archive.
    
    :param query: The search term or keyword to look for in the article titles and contents.
    :param limit: Number of articles to return (max 5).
    """
    # Assuming the database is in the same directory or provide an absolute path
    db_path = "inoreader_archive.db"
    
    if not os.path.exists(db_path):
        return "Error: Database 'inoreader_archive.db' not found. Please run the ingestion script first."

    # Limit maximum results to prevent token overflow
    limit = min(limit, 5)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQLite Full-Text Search query ordered by relevance (rank)
    sql = """
        SELECT title, author, source, url, content 
        FROM articles 
        WHERE articles MATCH ? 
        ORDER BY rank 
        LIMIT ?
    """
    
    try:
        cursor.execute(sql, (query, limit))
        results = cursor.fetchall()
    except sqlite3.OperationalError as e:
        return f"Database error during search: {e}"
    finally:
        conn.close()
    
    if not results:
        return f"No articles found matching '{query}' in your reading archive."
        
    formatted_results = f"Found {len(results)} articles for '{query}':\n\n"
    for title, author, source, url, content in results:
        # We truncate the content slightly to save agent context tokens
        snippet = content[:1000] + "..." if len(content) > 1000 else content
        formatted_results += f"Title: {title}\nAuthor: {author}\nSource: {source}\nURL: {url}\nContent Snippet: {snippet}\n---\n"
        
    return formatted_results

# If testing locally
if __name__ == "__main__":
    print(search_inoreader_archive("artificial intelligence", 2))
