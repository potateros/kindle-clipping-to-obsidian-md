# Kindle Clippings to Markdown Converter

Convert Kindle "My Clippings.txt" into organized markdown files with metadata preservation and deduplication.

## Features
- Creates individual markdown files per book
- Removes duplicate highlights
- Preserves page numbers, locations & dates
- Sorts highlights by location
- Generates valid YAML frontmatter
- Handles special characters in titles

## Prerequisites
- Python 3.x
- Your Kindle's `My Clippings.txt` file

## Usage

1. Place `clippings_converter.py` and `My Clippings.txt` in the same directory
2. Run:
```bash
python clippings_converter.py
```

Find generated markdown files in the output/ directory

Sample Output
output/The Pleasure of Finding Things Out - Feynman.md:

```markdown
---
title: "﻿The Pleasure of Finding Things Out: The Best Short Works of Richard P. Feynman"
author: "Richard P. Feynman"
type: kindle highlight
tags: kindle
---

# ﻿The Pleasure of Finding Things Out: The Best Short Works of Richard P. Feynman

> [!quote] Page: 13 | Location: 191-194 | Added: Saturday, May 21, 2022 10:36:30 PM
> “You see? That’s why scientists persist in their investigations, why we struggle so desperately for every bit of knowledge, stay up nights seeking the answer to a problem, climb the steepest obstacles to the next fragment of understanding, to finally reach that joyous moment of the kick in the discovery, which is part of the pleasure of finding things out.”

> [!quote] Page: 87 | Location: 1327-1329 | Added: Saturday, May 21, 2022 10:38:35 PM
> the computer disease, that anybody who works with computers now knows about. It’s a very serious disease and it interferes completely with the work. It was a serious problem that we were trying to do. The disease with computers is you play with them. They are so wonderful
```

Note: Generated filenames are sanitized versions of book titles

