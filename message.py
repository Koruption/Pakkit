messages = {
    "welcome": [
        "📦 Nerapakker",
        "",
        "This tool helps you turn audio directories into ready-to-broadcast .pak files.",
        "Just drag and drop a pak structured folder, and Nerapakker will validate, pack, and prime it",
        "for transmission.",
        "",
        "📂 Expected folder structure:",
        "  - /tracks         → your music or audio content (.mp3)",
        "  - /sfx            → optional sound effects (.mp3)",
        "  - /interrupts     → optional interludes or voice lines (.mp3)",
        "  - metadata.json   → required metadata",
        "  - cover.png/gif   → optional cover art",
        "  - intro.mp3       → optional intro track",
        "  - README.md       → optional notes",
        "",
        "🛠️  After importing, you'll be able to:",
        "  [play] → play and preview tracks",
        "  [pack]        → package into .pak format",
        "  [upload]        → upload to Neraverse",
        "  [new]         → start over with a new folder",
        "  [prune]       → remove files from the folder",
        "",
        "🎛️  Use your keyboard to control playback and actions:",
        "  ← / →        skip tracks",
        "  ↑ / ↓        raise/lower volume",
        "  space        pause/play",
        "  q            quit playback",
        "",
    ],
    "start_prompt": "Ready? Drop in your audio folder to begin...",
    "default_mode_prompt": """🛠️  Type any of the following commands: \n
    [play] → play and preview tracks \n
    [pack] → package into .pak format \n
    [upload] → upload to Neraverse \n
    [new] → start over with a new folder \n \n
    [prune] → remove files from the folder \n \n
     ----------------------------------------
     | or type 'menu' to select from options |
     ----------------------------------------
    """,
    "playback_mode_prompt": """
    🎵  Use your keyboard to control playback and actions \n
    ← / →        skip tracks \n
    ↑ / ↓        raise/lower volume \n
    [space]        pause/play \n
    [q]            quit playback \n
    """,
    "pruning_mode_prompt": """
    📊  Use your keyboard to control playback and actions \n
    ↑ [up]           select previous file \n
    ↓ [down]         select next file \n
    [delete]       delete selected file \n
    [q]         exit pruning mode \n
    """,
}
