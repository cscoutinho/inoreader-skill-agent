import json
import sqlite3
import re
import os

def strip_html(text):
    """Remove HTML tags from a string."""
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).replace('&nbsp;', ' ').replace('\n', ' ').strip()

def build_database(json_path, db_path="inoreader_archive.db"):
    print(f"Reading JSON file from {json_path}...")
    if not os.path.exists(json_path):
        print("File not found!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    items = data.get("items", [])
    print(f"Found {len(items)} items. Building database...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a Virtual Table using FTS5 for fast full-text search
    cursor.execute("DROP TABLE IF EXISTS articles")
    cursor.execute("""
        CREATE VIRTUAL TABLE articles USING fts5(
            id, 
            title, 
            author, 
            source, 
            url, 
            content,
            published_ts UNINDEXED
        )
    """)

    count = 0
    for item in items:
        item_id = item.get("id", "")
        title = item.get("title", "No Title")
        author = item.get("author", "")
        
        # Get source title
        origin = item.get("origin", {})
        source = origin.get("title", "")
        
        # Get URL
        url = ""
        canonical = item.get("canonical", [])
        alternate = item.get("alternate", [])
        if canonical and len(canonical) > 0:
            url = canonical[0].get("href", "")
        elif alternate and len(alternate) > 0:
            url = alternate[0].get("href", "")
            
        # Get Content and strip HTML
        summary = item.get("summary", {})
        content_html = summary.get("content", "")
        clean_content = strip_html(content_html)
        
        published_ts = item.get("published", 0)

        cursor.execute("""
            INSERT INTO articles (id, title, author, source, url, content, published_ts)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (item_id, title, author, source, url, clean_content, published_ts))
        
        count += 1

    conn.commit()
    conn.close()
    print(f"Successfully inserted {count} articles into {db_path}!")

if __name__ == "__main__":
    # Point this to the correct path
    JSON_FILE_PATH = r"C:\Users\csc\Downloads\Inoreader\starred.json"
    build_database(JSON_FILE_PATH)
