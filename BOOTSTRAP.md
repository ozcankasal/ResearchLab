# Bootstrap: using the Research Lab in a project

Instructions for an agent the user points at this folder ("use my lab at ~/Documents/ResearchLab for this project").

The lab assists a researcher; it does not do their research or write their papers for them. Before working with it, read `ETHICS.md`: the researcher is the author, AI help that reaches a project output is logged as an AI-USE entry in the notebook, and nothing is fabricated.

This repository is the lab's **source**. It stays read-only while you work on a project: never create, edit or delete files here during project work. Everything a project produces lands in the project folder:
- briefs, plans, notebooks and casts;
- room memories;
- papers;
- config answers.

## Who you are setting it up for

Many people who use the lab are researchers, not programmers. While you set it up:

- explain each step in one plain sentence before you run it, and what it changed afterwards;
- ask before installing anything on the computer, and say what it is for;
- never ask the user to edit files or type commands themselves: run them, with their permission;
- when something fails, say what went wrong in plain words and what you will try next.

## Set up a project

0. **Check the two tools the installer needs.** Run `uv --version` and `npx --version`.
   - `uv` runs the lab's small Python scripts. If it is missing, offer to install it with the official installer from <https://docs.astral.sh/uv/getting-started/installation/>:
     - macOS and Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
     - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - `npx` comes with Node.js and fetches BMad. If it is missing, offer the LTS installer from <https://nodejs.org>, or the user's package manager (for example `brew install node` on macOS or `winget install OpenJS.NodeJS.LTS` on Windows).
   - Install only after the user agrees. A new terminal may be needed before the tool is found.
1. **Find the project folder.** It is normally the current working directory. Confirm it with the user if unsure, and create it if it does not exist. It must not be this repository or lie inside it.
2. **Gather the author details.** Ask for the author name, affiliation and ORCID, or reuse values the user has already given in this session.
3. **Run the installer** with that information:

   ```
   uv run <this folder>/tools/install_lab.py <project folder> --author "<name>" --affiliation "<affiliation>" --orcid "<orcid>"
   ```

   It does four things:
   - installs BMad in the project if it is missing (the core tools and the method modules from GitHub);
   - links every lab skill into the project's shared `.agents/skills/` folder, and into each AI assistant's own skills folder that BMad set up there;
   - registers the `lab` module with those answers;
   - gives `bmad-build` the lab's research-software standards.

   It prints a JSON summary, and every step must show success. Use `--dry-run` first if the user wants to see the plan. Use `--copy` instead of links when the project must stand alone, for example on another machine. Where the system does not allow links (Windows without Developer Mode), the installer copies the skills by itself and says so; such a project picks up a newer lab only when the installer runs again. Running the installer again is always safe: it keeps earlier answers and removes its own links to skills the lab has retired.
4. **Confirm the module is registered:**

   ```
   uv run <project>/_bmad/scripts/roster.py --project-root <project> --skill <project>/.agents/skills/bmod-lab
   ```

   The output should list the lab's eight core assistants, the eight guests and guardians, and six rooms, with no problems.
5. **Start the project.**
   - Set an initiative for the project with the `bmad` skill.
   - Talk to Nadia, the PI, who runs `lab-cast` first. It classifies the project by field, method, outputs and sensitivities, and brings in the specialists, guardians and rooms the classification calls for. These live in the project's `_bmad/custom/bmad-party-mode.toml`.
   - From there, follow the Lab Method (`skills/bmod-lab/help/lab-method.md`).
6. **Hand over in plain words.** Tell the user that the lab is ready, that everything it writes stays in this folder, and what to say next, for example:
   - "Talk to Nadia. I want to study …" to start, in any language;
   - "Has anyone done this before?" for a prior-art search;
   - "Try to break my idea" for a kill test;
   - "Where were we?" at the start of a later session.

## When the user wants to change the lab itself

That is framework work, not project work. Do it here, in this repository, only when the user asks for it:

- **Core personas and menus:** edit `tools/cast.py` and `tools/workflows.py`, then run `uv run tools/build_cast.py`.
- **Method specialists, domain packs and classification rules:** edit `skills/lab-cast/catalogue/`. A new domain pack is one TOML file in `catalogue/packs/`.
- **Workflow skills:** edit their `SKILL.md`, references and assets under `skills/`.
- **After any change:** run `tools/check.sh` until it is clean.

Projects that link the lab pick the change up at once. Projects that copied it need the installer run again with `--copy`.
