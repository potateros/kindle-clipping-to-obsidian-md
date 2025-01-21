import re
import os
from collections import defaultdict

'''Output structure:
---
title: "Book Title"
author: "Author Name"
type: kindle highlight
tags: kindle
---

# Book Title

> [!quote] Page: 123 | Location: 456-789 | Added: May 21, 2022
> Highlight text here

> [!quote] Page: 124 | Location: 790-795 | Added: May 21, 2022
> Another highlight text
'''

def parse_clippings(clippings_text):
    entries = clippings_text.split('==========')
    books = defaultdict(list)

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        lines = entry.split('\n')
        if len(lines) < 3:
            continue

        book_line = lines[0].strip()
        if ' (' not in book_line:
            title = book_line
            author = 'Unknown'
        else:
            title_part, author_part = book_line.rsplit(' (', 1)
            title = title_part.strip()
            author = author_part.strip().rstrip(')')

        metadata_line = lines[1].strip()
        if not metadata_line.startswith('- Your Highlight'):
            continue

        metadata_str = metadata_line.replace("- Your Highlight on ", "", 1).strip()
        metadata_parts = metadata_str.split(' | ')
        page, location, date = None, None, None

        for part in metadata_parts:
            if part.startswith('page '):
                page = part[len('page '):].strip()
            elif part.startswith('Location '):
                location = part[len('Location '):].strip()
            elif part.startswith('Added on '):
                date = part[len('Added on '):].strip()

        text = '\n'.join(lines[2:]).strip()

        books[(title, author)].append({
            'text': text,
            'page': page,
            'location': location,
            'date': date
        })

    return books

def remove_duplicates(highlights):
    sorted_highlights = sorted(highlights, key=lambda x: -len(x['text']))
    unique = []

    for h in sorted_highlights:
        if not any(h['text'] in u['text'] for u in unique):
            unique.append(h)
    return unique

def process_title(title):
    title_part = title.split(':', 1)[0].strip()
    title_part = re.sub(r'[^\w\s]', '', title_part)
    return re.sub(r'\s+', ' ', title_part)

def process_author(author_str):
    authors = [a.strip() for a in author_str.split(';')]
    last_names = []
    for author in authors:
        parts = author.split()
        if parts:
            last_name = parts[-1].rstrip('.')
            last_names.append(last_name)
    return ', '.join(last_names)

def sanitize_filename(title, author):
    clean_title = process_title(title)
    clean_author = process_author(author)
    return f"{clean_title} - {clean_author}.md"

def sort_by_location(highlights):
    def get_location_number(hl):
        location_str = hl.get('location', '0') or '0'
        try:
            return int(location_str.split('-')[0])
        except (ValueError, AttributeError):
            return 0

    return sorted(highlights, key=lambda x: get_location_number(x))

def generate_markdown(book_key, highlights, output_dir='output'):
    title, author = book_key
    filename = sanitize_filename(title, author)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'---\ntitle: "{title}"\nauthor: "{author}"\ntype: kindle highlight\ntags: kindle\n---\n\n')
        f.write(f'# {title}\n\n')
        sorted_highlights = sort_by_location(highlights)

        for h in sorted_highlights:
            f.write(f"> [!quote] Page: {h['page']} | Location: {h['location']} | Added: {h['date']}\n")
            f.write(f"> {h['text']}\n\n")

def main():
    with open('My Clippings.txt', 'r', encoding='utf-8') as f:
        clippings = f.read()

    books = parse_clippings(clippings)
    os.makedirs('output', exist_ok=True)

    for book_key, highlights in books.items():
        unique_highlights = remove_duplicates(highlights)
        generate_markdown(book_key, unique_highlights)

if __name__ == '__main__':
    main()
