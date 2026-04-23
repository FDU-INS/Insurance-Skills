---
name: ask-lore
description: Query Lore, the librarian agent, to search the owner's personal knowledge base. Use when looking up stored documents, personal records, insurance, manuals, notes, vehicles, or any "do I have a document about X?" type question.
---

# ask-lore

Query Lore, the librarian agent, to search the owner's personal knowledge base.

## When to Use

- Looking up documents, files, or information the owner has stored
- Questions about personal records, insurance, manuals, notes, vehicles, etc.
- Any "do I have a document about X?" type query

## How to Use

Run the query script:

```bash
python3 /home/fera/agents/main/workspace/.claude/skills/ask-lore/query_lore.py "your question here"
```

Or use it inline from Python:

```python
import sys
sys.path.insert(0, '/home/fera/agents/main/workspace/.claude/skills/ask-lore')
from query_lore import query_lore
import asyncio

result = asyncio.run(query_lore("What insurance documents do we have?"))
print(result)
```

## Notes

- Lore runs as the `librarian` agent on the Fera gateway
- She has access to the knowledge base at `/home/fera/agents/librarian/knowledge/`
- The session is persistent (`librarian/dm-fera`) — she remembers conversation context within a session
- Responses are streamed and collected; default timeout is 120s
