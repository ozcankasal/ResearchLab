"""Customization and module membership of the lab's workflow skills.

`tools/build_cast.py` renders these into each workflow's `customize.toml` and `bmod.toml`
(the SKILL.md bodies are written by hand). Edit here, then rebuild.
"""

# skill -> (artifact type or None, recommended skills from this module, recommended skills from BMad)
WORKFLOWS = {
    "lab-cast": ("cast", ["lab-notebook", "lab-spark"], ["bmad-party-mode", "bmad-customize"]),
    "lab-spark": ("ideas", ["lab-survey", "lab-notebook"], ["bmad-party-mode"]),
    "lab-survey": ("survey", ["lab-killtest", "lab-frame", "lab-notebook"], []),
    "lab-frame": ("brief", ["lab-plan", "lab-notebook"], ["bmad-party-mode"]),
    "lab-plan": ("plan", ["lab-frame", "lab-notebook"], ["bmad-build"]),
    "lab-prove": ("proof", ["lab-notebook"], []),
    "lab-experiment": ("experiment", ["lab-notebook"], []),
    "lab-killtest": ("killtest", ["lab-notebook", "lab-frame"], ["bmad-party-mode"]),
    "lab-factcheck": ("factcheck", ["lab-notebook"], []),
    "lab-referee": ("referee", ["lab-write", "lab-notebook"], []),
    "lab-write": (None, ["lab-factcheck", "lab-referee"], []),
    "lab-release": (None, ["lab-notebook"], []),
    "lab-notebook": ("notebook", ["lab-plan"], []),
    "lab-voice": ("voice", ["lab-write"], []),
}

# Extra customization keys a workflow declares and reads, as TOML lines appended to its [workflow] table.
EXTRA = {
    "lab-voice": (
        "\n# Where language packs for tells.py live: one <code>.toml per language, written by this skill\n"
        "# when it meets a language for the first time and reused afterwards. A project folder, so the\n"
        "# shared lab source stays read-only.\n"
        'packs_path = "{output_folder}/voice-packs"\n'
    ),
}
