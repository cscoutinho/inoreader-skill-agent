---
name: inoreader-library-manager
description: Save or remove articles from the user's Inoreader library (Starred Items)
version: 1.0
---

# Context
Inoreader manages saved items through its tagging system. Specifically, saving an item to the library is equivalent to adding the system tag `user/-/state/com.google/starred`. Removing it means removing that tag.

# Procedure
When the user asks to save or remove an article from their Inoreader library, follow these steps:

1. **Identify the Item ID**: Extract the Inoreader item ID from the user's request. Shortened IDs (e.g., `123456789`) are preferred over long `tag:` formats.
2. **Determine the Action**:
   - If **saving** to the library, set the tool parameters to add the star tag.
   - If **removing** from the library, set the tool parameters to remove the star tag.
3. **Execute Tool**: Use the `inoreader_edit_tag` tool with the following parameters:
   - `item_id`: The ID of the article.
   - `action`: Either `"save"` (to star) or `"remove"` (to un-star).
4. **Confirm Success**: If the tool returns a success message (200 OK), inform the user that the item was successfully updated in their Inoreader library. If it fails, report the error.
