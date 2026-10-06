#!/usr/bin/env python3
"""
Day 11 (featured) of my daily coding journey - Prompt Vault CLI.

Stop losing your best AI prompts in chat history. Prompt Vault saves,
tags, searches, favorites, and exports the prompts you actually reuse.

Usage:
    python prompt_vault.py add "Debug helper" --tags coding,debug
    python prompt_vault.py list
    python prompt_vault.py search "email"
    python prompt_vault.py show 3
    python prompt_vault.py fav 3
    python prompt_vault.py stats
    python prompt_vault.py export my-prompts.md

Your prompts live in ~/.prompt_vault.json - plain JSON, yours forever.
"""

import argparse
import json
import os
import sys

from vault import PromptVault

# Starter prompts shipped with the repo, loaded on first run.
SEED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "starter_prompts.json")


def print_card(p):
    """Print one prompt as a compact card."""
    star = " ⭐" if p["favorite"] else ""
    tags = ", ".join("#" + t for t in p["tags"]) or "no tags"
    print(f"[{p['id']}] {p['title']}{star}")
    print(f"     {tags} · added {p['created']}")


def cmd_add(vault, args):
    """Add a prompt; read the body from --text or interactively."""
    text = args.text
    if text is None:
        print("Paste your prompt (Ctrl+D / Ctrl+Z when done):")
        text = sys.stdin.read().strip()
    if not text:
        print("Nothing to save - prompt text was empty.")
        return
    tags = args.tags.split(",") if args.tags else []
    p = vault.add(args.title, text, tags)
    print(f"Saved as prompt #{p['id']}: {p['title']}")


def cmd_list(vault, args):
    prompts = vault.all(favorites_first=args.favorites)
    if not prompts:
        print("Vault is empty. Add one with: python prompt_vault.py add \"Title\"")
        return
    for p in prompts:
        print_card(p)


def cmd_search(vault, args):
    results = vault.search(args.query)
    if not results:
        print(f"No prompts matched '{args.query}'.")
        return
    print(f"{len(results)} match(es) for '{args.query}':\n")
    for p in results:
        print_card(p)


def cmd_show(vault, args):
    p = vault.get(args.id)
    if not p:
        print(f"No prompt with id {args.id}.")
        return
    star = " ⭐" if p["favorite"] else ""
    print(f"[{p['id']}] {p['title']}{star}")
    print(f"Tags: {', '.join(p['tags']) or 'none'} · Added {p['created']}\n")
    print(p["text"])


def cmd_delete(vault, args):
    if vault.delete(args.id):
        print(f"Deleted prompt #{args.id}.")
    else:
        print(f"No prompt with id {args.id}.")


def cmd_fav(vault, args):
    p = vault.toggle_favorite(args.id)
    if not p:
        print(f"No prompt with id {args.id}.")
    elif p["favorite"]:
        print(f"⭐ Prompt #{args.id} favorited.")
    else:
        print(f"Prompt #{args.id} un-favorited.")


def cmd_tag(vault, args):
    p = vault.tag(args.id, args.tags.split(","))
    if not p:
        print(f"No prompt with id {args.id}.")
    else:
        print(f"Prompt #{args.id} tags: {', '.join(p['tags'])}")


def cmd_stats(vault, args):
    s = vault.stats()
    print(f"Total prompts : {s['total']}")
    print(f"Favorites     : {s['favorites']}")
    if s["top_tags"]:
        print("Top tags      : " + ", ".join(f"#{t} ({n})" for t, n in s["top_tags"]))
    else:
        print("Top tags      : none yet")


def cmd_export(vault, args):
    path = vault.export_markdown(args.file)
    print(f"Exported {vault.stats()['total']} prompt(s) to {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Prompt Vault - save, find, and reuse your best AI prompts."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="Save a new prompt")
    a.add_argument("title", help="Short name for the prompt")
    a.add_argument("--text", help="The prompt text (or paste interactively)")
    a.add_argument("--tags", help="Comma-separated tags, e.g. coding,debug")

    l = sub.add_parser("list", help="List all prompts")
    l.add_argument("--favorites", action="store_true", help="Favorites first")

    s = sub.add_parser("search", help="Search titles, text, and tags")
    s.add_argument("query")

    sh = sub.add_parser("show", help="Show one prompt's full text")
    sh.add_argument("id", type=int)

    d = sub.add_parser("delete", help="Delete a prompt")
    d.add_argument("id", type=int)

    f = sub.add_parser("fav", help="Toggle a prompt's favorite star")
    f.add_argument("id", type=int)

    t = sub.add_parser("tag", help="Add tags to a prompt")
    t.add_argument("id", type=int)
    t.add_argument("tags", help="Comma-separated tags to add")

    sub.add_parser("stats", help="Show vault statistics")

    e = sub.add_parser("export", help="Export the vault to Markdown")
    e.add_argument("file", help="Output .md file path")

    args = parser.parse_args()

    vault = PromptVault()

    # First run: seed the vault with starter prompts from the repo.
    if not vault.prompts and os.path.exists(SEED_FILE):
        with open(SEED_FILE, encoding="utf-8") as f:
            seeds = json.load(f)
        n = vault.seed(seeds)
        print(f"Welcome to Prompt Vault! Loaded {n} starter prompts to explore.\n")

    commands = {
        "add": cmd_add, "list": cmd_list, "search": cmd_search,
        "show": cmd_show, "delete": cmd_delete, "fav": cmd_fav,
        "tag": cmd_tag, "stats": cmd_stats, "export": cmd_export,
    }
    commands[args.command](vault, args)


if __name__ == "__main__":
    main()
