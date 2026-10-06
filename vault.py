"""
Day 11 (featured) of my daily coding journey - Prompt Vault, storage layer.

The PromptVault class owns everything about saving and loading prompts:
it reads/writes a single JSON file, assigns IDs, and offers search,
favorites, stats, and Markdown export. The CLI in prompt_vault.py only
handles user input and pretty-printing - all the data logic lives here.
"""

import json
import os
from datetime import datetime


class PromptVault:
    """A tiny JSON-backed database of reusable AI prompts."""

    def __init__(self, path=None):
        # Default to a hidden file in the user's home folder so the
        # vault survives no matter which directory you run the CLI from.
        self.path = path or os.path.expanduser("~/.prompt_vault.json")
        self.prompts = self._load()

    # ---- persistence -------------------------------------------------

    def _load(self):
        """Read the JSON file; return [] if it doesn't exist yet."""
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self):
        """Write the whole vault back to disk."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.prompts, f, indent=2, ensure_ascii=False)

    def _next_id(self):
        """IDs are just 1, 2, 3... based on the biggest one so far."""
        if not self.prompts:
            return 1
        return max(p["id"] for p in self.prompts) + 1

    # ---- core operations ---------------------------------------------

    def add(self, title, text, tags):
        """Save a new prompt; returns the prompt dict (with its new id)."""
        prompt = {
            "id": self._next_id(),
            "title": title,
            "text": text,
            # Normalize tags: lowercase, no empties, no duplicates.
            "tags": sorted({t.strip().lower() for t in tags if t.strip()}),
            "favorite": False,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }
        self.prompts.append(prompt)
        self._save()
        return prompt

    def all(self, favorites_first=False):
        """Return every prompt, newest first (favorites first if asked)."""
        ordered = sorted(self.prompts, key=lambda p: p["id"], reverse=True)
        if favorites_first:
            ordered.sort(key=lambda p: not p["favorite"])
        return ordered

    def search(self, query):
        """Case-insensitive search across titles, text, and tags."""
        q = query.lower()
        return [
            p
            for p in self.prompts
            if q in p["title"].lower()
            or q in p["text"].lower()
            or any(q in tag for tag in p["tags"])
        ]

    def get(self, prompt_id):
        """Return one prompt by id, or None if it doesn't exist."""
        for p in self.prompts:
            if p["id"] == prompt_id:
                return p
        return None

    def delete(self, prompt_id):
        """Delete a prompt; returns True if something was deleted."""
        before = len(self.prompts)
        self.prompts = [p for p in self.prompts if p["id"] != prompt_id]
        if len(self.prompts) != before:
            self._save()
            return True
        return False

    def toggle_favorite(self, prompt_id):
        """Flip the favorite flag; returns the prompt or None."""
        prompt = self.get(prompt_id)
        if prompt:
            prompt["favorite"] = not prompt["favorite"]
            self._save()
        return prompt

    def tag(self, prompt_id, new_tags):
        """Add tags to a prompt; returns the prompt or None."""
        prompt = self.get(prompt_id)
        if prompt:
            merged = set(prompt["tags"]) | {t.strip().lower() for t in new_tags}
            prompt["tags"] = sorted(t for t in merged if t)
            self._save()
        return prompt

    # ---- insights & export -------------------------------------------

    def stats(self):
        """A quick summary: counts, favorites, and top tags."""
        tag_counts = {}
        for p in self.prompts:
            for tag in p["tags"]:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return {
            "total": len(self.prompts),
            "favorites": sum(1 for p in self.prompts if p["favorite"]),
            "top_tags": sorted(tag_counts.items(), key=lambda kv: kv[1], reverse=True)[:5],
        }

    def export_markdown(self, out_path):
        """Write the whole vault as a readable Markdown document."""
        lines = ["# Prompt Vault Export", ""]
        for p in self.all():
            star = " ⭐" if p["favorite"] else ""
            lines.append(f"## {p['id']}. {p['title']}{star}")
            lines.append("")
            lines.append(f"*Tags: {', '.join(p['tags']) or 'none'} · Added {p['created']}*")
            lines.append("")
            lines.append("```")
            lines.append(p["text"])
            lines.append("```")
            lines.append("")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return out_path

    def seed(self, seed_prompts):
        """Load starter prompts on first run; returns how many were added."""
        added = 0
        for s in seed_prompts:
            self.add(s["title"], s["text"], s.get("tags", []))
            added += 1
        return added
