import json
import sqlite3
import re

def clean_html(raw_html):
    """Remove HTML tags to make the text more readable and searchable."""
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # Also replace multiple spaces/newlines with a single space
    return " ".join(cleantext.split())

def build_database(json_path: str, db_path: str):
    print(f"Loading JSON from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('items', [])
    print(f"Found {len(items)} items. Building database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a Full-Text Search (FTS5) table for ultra-fast text querying
    cursor.execute('DROP TABLE IF EXISTS articles')
    cursor.execute('''
        CREATE VIRTUAL TABLE articles USING fts5(
            item_id,
            title,
            url,
            content,
            published_date
        )
    ''')
    
    for item in items:
        item_id = item.get('id', '')
        title = item.get('title', 'No Title')
        
        # Get URL
        url = ""
        canonical = item.get('canonical', [])
        if canonical and len(canonical) > 0:
            url = canonical[0].get('href', '')
            
        # Get content (summary or full content if available)
        content_html = ""
        summary = item.get('summary', {})
        if summary:
            content_html = summary.get('content', '')
            
        clean_content = clean_html(content_html)
        published_date = str(item.get('published', ''))
        
        cursor.execute(
            'INSERT INTO articles (item_id, title, url, content, published_date) VALUES (?, ?, ?, ?, ?)',
            (item_id, title, url, clean_content, published_date)
        )
        
    conn.commit()
    conn.close()
    print(f"Successfully built SQLite database at {db_path} with {len(items)} articles!")

if __name__ == "__main__":
    JSON_FILE = r"C:\Users\csc\Downloads\Inoreader\starred.json"
    DB_FILE = r"C:\Users\csc\Documents\Antigravity\inoreader-skill-agent\inoreader_archive.db"
    build_database(JSON_FILE, DB_FILE)
