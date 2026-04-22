import sqlite3
import os
import re

def sanitize_filename(title, item_id):
    """Creates a safe filename from the article title, falling back to ID if needed."""
    if not title or title.strip() == "":
        return f"article_{item_id.replace(':', '_').replace('/', '_')}.md"
    
    # Remove invalid characters for Windows/Linux filenames
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    # Truncate to avoid path length limits
    safe_title = safe_title[:50].strip()
    return f"{safe_title}_{item_id[-8:]}.md" if safe_title else f"article_{item_id[-8:]}.md"

def export_db_to_markdown(db_path: str, output_dir: str):
    print(f"Exporting articles from {db_path} to {output_dir}/...")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT item_id, title, url, content, published_date FROM articles")
        articles = cursor.fetchall()
        
        for item_id, title, url, content, published_date in articles:
            filename = sanitize_filename(title, item_id)
            filepath = os.path.join(output_dir, filename)
            
            # Format the markdown file specifically to help Graphify understand the context
            md_content = f"""# {title}

**Source URL:** {url}
**Date:** {published_date}
**Inoreader ID:** {item_id}

---

## Content Summary
{content}
"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
        print(f"Successfully exported {len(articles)} articles to {output_dir}/")
        print("You can now run Graphify on this folder using: /graphify " + output_dir)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    DB_FILE = r"C:\Users\csc\Documents\Antigravity\inoreader-skill-agent\inoreader_archive.db"
    OUTPUT_FOLDER = r"C:\Users\csc\Documents\Antigravity\inoreader-skill-agent\inoreader_graph_corpus"
    
    export_db_to_markdown(DB_FILE, OUTPUT_FOLDER)
