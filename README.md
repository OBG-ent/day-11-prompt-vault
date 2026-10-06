# 🗝️ Prompt Vault

**Stop losing your best AI prompts in chat history.** Prompt Vault is a tiny Python CLI that saves, tags, searches, favorites, and exports the prompts you actually reuse — all in plain JSON you own.

*Day 11 (featured build) of my daily coding journey — one bigger project, shipped every day.*

## Features

- **Save prompts** with a title, body, and tags (`add`)
- **Instant search** across titles, text, and tags
- **Favorites** — star the prompts you reach for daily
- **Tagging** — organize by `coding`, `writing`, `learning`… whatever fits
- **Stats** — see your totals and most-used tags at a glance
- **Markdown export** — back up or share your whole vault as one readable file
- **8 starter prompts included** — useful on the very first run (debugger, code reviewer, study planner, email writer, and more)
- **Zero dependencies** — pure Python standard library, data in `~/.prompt_vault.json`

## Run it in 30 seconds

```bash
# Save a prompt (paste the body interactively, or pass --text)
python prompt_vault.py add "Debug helper" --tags coding,debug

# List everything, search, and view one in full
python prompt_vault.py list
python prompt_vault.py search "email"
python prompt_vault.py show 3

# Star a favorite, add tags, see stats, export
python prompt_vault.py fav 3
python prompt_vault.py tag 3 writing,work
python prompt_vault.py stats
python prompt_vault.py export my-prompts.md
```

### Example session

```
$ python prompt_vault.py add "Polite but firm email" --tags writing,email
Saved as prompt #3: Polite but firm email

$ python prompt_vault.py search "email"
1 match(es) for 'email':

[3] Polite but firm email
     #email, #writing · added 2026-10-06

$ python prompt_vault.py stats
Total prompts : 11
Favorites     : 2
Top tags      : #coding (4), #writing (3), #learning (2)
```

## Project layout

| File | What it does |
|---|---|
| `prompt_vault.py` | The CLI — parses commands, prints output |
| `vault.py` | The `PromptVault` class — JSON storage, search, stats, export |
| `starter_prompts.json` | 8 genuinely useful prompts loaded on first run |
| `README.md` | You're reading it 🙂 |

## What I practiced

- Splitting a project into a **storage layer** (`vault.py`) and a **presentation layer** (`prompt_vault.py`) — the CLI never touches the JSON file directly
- `argparse` subcommands (one clean CLI, many commands)
- JSON persistence with auto-incrementing IDs
- Designing a data model (prompts with tags, favorites, timestamps) and operations on it (search, export, stats)
