db = {
    "scenes": {
        "bootup": {
            "logo": [
                "-------------------------------------------------------------------------------------------",
                " ",
                "     .-') _   ('-.  _  .-')     ('-.             _ (`-.    ('-.    .-. .-')   .-')    ",
                "    ( OO ) )_(  OO)( \\( -O )   ( OO ).-.        ( (OO  )  ( OO ).-.\\  ( OO ) ( OO ).  ",
                ",--./ ,--,'(,------.,------.   / . --. /       _.`     \\  / . --. /,--. ,--.(_)---\\_) ",
                "|   \\ |  |\\ |  .---'|   /`. '  | \\-.  \\       (__...--''  | \\-.  \\ |  .'   //    _ |  ",
                "|    \\|  | )|  |    |  /  | |.-'-'  |  |       |  /  | |.-'-'  |  ||      /,\\  :` `.  ",
                "|  .     |/(|  '--. |  |_.' | \\| |_.'  |       |  |_.' | \\| |_.'  ||     ' _)'..`''.) ",
                "|  |\\    |  |  .--' |  .  '.'  |  .-.  |       |  .___.'  |  .-.  ||  .   \\ .-._)   \\ ",
                "|  | \\   |  |  `---.|  |\\  \\   |  | |  |       |  |       |  | |  ||  |\\   \\       / ",
                "`--'  `--'  `------'`--' '--'  `--' `--'       `--'       `--' `--'`--' '--' `-----'  ",
                " ",
                "                                         v1.0                                             ",
                "                               Corposoft© Software 2025                                    ",
                "                                  All rights reserved                                    ",
                " ",
                "-------------------------------------------------------------------------------------------",
            ],
            "logs": [
                "$ Initializing NERAVERSE kernel...",
                "$ Mounting /pak/core/",
                "$ Detecting audio nodes...",
                "$ Sourcing waveform matrix... OK",
                "$ Calibrating dynamic gain bus...",
                "$ Syncing vibrational lattice...",
                "$ Scanning for .pak structures... FOUND",
                "$ Verifying temporal harmonics... OK",
                "$ Bootstrapping Nera AudioPak Builder v1.0",
                "$ Allocating memory for transient audio fields...",
                "$ Checking integrity of spectral cache...",
                "$ Loading manifest.json... OK",
                "$ Connecting to NERAVERSE relay...",
                "$ Compiling acoustic geometry...",
                "$ Mapping signal path... OK",
                "$ Reconstructing waveform holograms...",
                "$ Initializing DSP tunnel...",
                "$ Activating meta-packet carrier...",
                "$ NeraPak interface online. Ready.",
            ],
            "credits": [
                "Welcome to NeraPak Builder v1.0",
                "Corposoft© Software 2025",
                "All rights reserved",
            ],
        },
        "home": {
            "overview": [
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
            "default_prompt": """🛠️  Type any of the following commands: \n
    [play] → play and preview tracks \n
    [pack] → package into .pak format \n
    [upload] → upload to Neraverse \n
    [new] → start over with a new folder \n \n
    [prune] → remove files from the folder \n \n
     ----------------------------------------
     | or type 'menu' to select from options |
     ----------------------------------------
    """,
            "file_size_exceeded": """
                    -----------------------------------------------------------------------------
                    |                                                                            |
                    | PAK size exceeds the 10MB limit ~ ({total_pak_size}MB)                     |
                    | Drop in a smaller pak or select prune to drop selected files               |
                    |                                                                            |
                    -----------------------------------------------------------------------------
                    """,
        },
    }
}
