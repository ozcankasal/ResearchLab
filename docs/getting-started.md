# Getting started, without programming

This guide takes you from nothing to your first conversation with the lab. You do not need to write code. Your AI assistant runs every command, and it asks you first.

## What you need

- **A computer** running macOS, Windows or Linux, with an internet connection for the setup.
- **An AI coding assistant that supports Agent Skills**, the open `SKILL.md` format. Several coding assistants support it, in a terminal, in code editors or in desktop apps; check your assistant's documentation for "skills". Most of them need a paid plan. The lab itself is free.

The setup also uses two free tools, `uv` and Node.js. If they are missing, your assistant offers to install them during step 3. You do not need to install anything by hand.

## Step 1: get the lab

On the lab's [GitHub page](https://github.com/ozcankasal/ResearchLab), click the green **Code** button, then **Download ZIP**. Unzip it and put the folder in your Documents folder, named `ResearchLab`.

If you use git, `git clone` it there instead. That makes updating easier later.

Keep this folder where it is. Your projects link to it, and moving it breaks the links (see [Troubleshooting](#troubleshooting)).

## Step 2: make a project folder

Create an empty folder for your research project, anywhere outside `ResearchLab`, for example `Documents/credit-scores`. Open that folder in your AI assistant:

- in VS Code: **File → Open Folder**, then start the assistant;
- in a terminal: go to the folder, then start the assistant;
- in a desktop app: choose the folder when you start a session.

## Step 3: ask your assistant to set it up

Paste this, with the path to your copy of the lab:

> Set up the Research Lab from `~/Documents/ResearchLab` in this folder. Follow its BOOTSTRAP.md, and explain each step to me in plain words.

The assistant then:

1. checks for `uv` and Node.js, and asks before installing either;
2. asks for your name, affiliation and ORCID, which are used on papers and release records;
3. installs BMad, the free framework the lab is built on, into your project folder;
4. connects the lab's assistants to your project;
5. confirms that everything works.

Your assistant asks before it runs each command. Read what it wants to run, and approve it when it matches what it said it would do. The whole setup takes a few minutes.

## Step 4: talk to Nadia

Nadia is the lab's principal investigator. Start a new session in the project folder, so the assistant sees the lab, and describe your idea in a few sentences, in any language:

> Talk to Nadia. I want to study how households read their credit scores.

> Talk to Nadia. I'm a historian. I want to trace how merchant networks in the Levant changed after 1600, using customs registers.

> Talk to Nadia. I have a conjecture about sums of unit fractions and want to know whether it is new.

> Nadia ile konuşmak istiyorum. Toprak nemi ölçümünde ucuz bir sensörün standart sensörün yerini alıp alamayacağını test etmek istiyorum.

Nadia first **classifies** the project: its field, its methods, what it will produce, and anything sensitive, such as people, personal data or patients. You confirm or correct the classification. The lab then brings in the specialists, guardians, standards and checks that this classification calls for. After that, Nadia suggests the next step.

## Everyday use

Talk to the lab in plain sentences. You do not need to remember the names below; Nadia routes you.

| You say | Who helps | What you get |
|---|---|---|
| "Give me research ideas about …" | Spark room | idea cards: a claim, its smallest test, and what would kill it |
| "Has anyone done this before?" | 📚 Selin | a search log in your field's databases, and a verdict for each idea |
| "Try to break my idea" | ⚖️ Viktor and your field's skeptics | a kill test: ALIVE, ALIVE-NARROW or DEAD, with reasons |
| "Write the research brief with me" | 🧭 Nadia | the questions, claims and non-claims, plus a go or no-go decision that you make |
| "Plan the work" | 🧭 Nadia, 🧪 Arjun | epics and stories, riskiest first, each with checks someone else can run |
| "Design the study" or "check my statistics" | 🧪 Arjun, your method specialists | a protocol written before the data is collected |
| "Check my proof" | proof room | small cases, a hunt for gaps, an adversarial reading |
| "Check my references and numbers" | 🔎 Marta | each source opened and quoted with a page number; each number traced to its script |
| "Review my draft like a referee" | ⚖️ Viktor's referee panel | independent reports, an editor's decision, a plan for your revisions |
| "Is my writing clear?" | ✒️ Clara, 🪶 Ruth | feedback on structure and generic phrasing, in your own voice |
| "Get my code and data ready to publish" | 🛠️ Lena | a tested release bundle and an AI-use disclosure, built from the notebook |
| "Where were we?" | 🧭 Nadia | the project's state, read from the notebook, and the next step |

## Where your files go

Everything the lab writes stays in your project folder:

```
credit-scores/
├── _bmad-output/
│   └── credit-scores/                  one folder per research project
│       ├── cast-credit-scores/         classification, specialists, rooms
│       ├── ideas-credit-scores/        idea cards
│       ├── survey-credit-scores/       search log and verdicts
│       ├── brief-credit-scores/        research brief and claim register
│       ├── plan-credit-scores/         epics and stories
│       ├── killtest-…  proof-…  experiment-…  factcheck-…  referee-…
│       └── notebook-credit-scores/     decisions, results, dead ends, AI use
├── papers/                             your paper projects
├── _bmad/                              settings: you can ignore this
└── .agents/  (and your assistant's)    links to the lab: you can ignore these
```

The files are plain text (Markdown and TOML), so you can open them in any editor, keep them in git, or share them with co-authors.

## Updating the lab

Download the new version and replace your `ResearchLab` folder, keeping the same place and the same name. Projects linked to it pick up the update at once.

If the setup reported that it *copied* the lab instead of linking it, ask your assistant to set the lab up again in that project. Running the setup again is always safe: it keeps your earlier answers.

## Troubleshooting

| What you see | What to do |
|---|---|
| "uv: command not found" right after installing it | Close and reopen the terminal or the assistant, then ask again. |
| The assistant doesn't know Nadia | Check that you opened the **project** folder, not `ResearchLab`, then start a new session so the assistant sees the new skills. |
| "BMad is not set up here" | Ask your assistant to set the lab up again. It is safe to repeat. |
| The setup says links are not allowed (Windows) | Nothing to do: it copies the lab instead. To use links, turn on Developer Mode in Windows settings and run the setup again. |
| You moved or renamed `ResearchLab` | Ask your assistant to set the lab up again from the new location. |

## Words you will meet

- **Kill criterion:** the result that would show an idea is wrong. Each claim gets one before any work starts.
- **Gate:** a decision point (G1 to G5) where the lab lays out the evidence and you decide.
- **Claim register:** the list of everything the project claims, each with its evidence level.
- **Story:** one piece of work with checks that someone else can run, such as a lemma, a study, a dataset or a piece of code.
- **Notebook:** the project's dated record of decisions, results, dead ends and AI use. Entries are never edited; corrections are added as new entries.
- **Room:** a meeting of several of the lab's personas on one question.
- **BMad:** the open-source framework the lab is built on. You do not need to learn it.

Read [`ETHICS.md`](../ETHICS.md) before your first project: it says what the lab will and will not do for you.
