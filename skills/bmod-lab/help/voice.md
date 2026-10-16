# The lab's voice

Read this before writing anything another person will read, and when the user asks about tone, AI tells, natural language or the author's style, in any language.

The goal is clear writing in the author's own voice: plain, specific, varied and accountable. Generic and machine-style prose has recognisable habits in every language. They matter as bad writing, because they replace content with gesture. Fixing the gesture means putting the author's content back. The voice pass is an editing aid. It is never a way to pass AI-generated text off as the author's (`help/responsible-use.md`).

Two limits apply to every edit:

- **Claims keep their strength.** A rewrite never makes a claim stronger or weaker than its evidence (`help/lab-method.md`, evidence levels). When a vague word hides a missing fact, mark `[specific needed]` rather than inventing one.
- **Clarity is the aim, not concealment.** When a journal, a repository or an employer asks how AI tools were used, the answer is truthful. `lab-release` drafts it from the notebook's AI-USE entries.

## Habits to replace, in any language

Each habit takes its own words in each language. The English phrases below only illustrate the pattern.

| Habit | What it does | Illustration (English) | Write instead |
|---|---|---|---|
| Significance inflation | grades importance instead of stating it | pivotal, crucial role, a testament to, paves the way | The specific consequence: what changes, for whom, by how much |
| Avoiding the plain verb | uses a grand verb where "is" or "has" would do | serves as, stands as, boasts | The plain verb |
| Trailing commentary | adds a participle clause that comments on its own sentence | "…, highlighting the importance of X" | Cut it, or make it a sentence with its evidence |
| Vague authority | leans on unnamed sources | experts argue, studies show | Name and cite the source, or cut |
| Set-piece structures | uses reflexive rhetorical frames | not only X but also Y; lists of exactly three | Say the things plainly, and list as many as there are |
| Signposting | starts sentence after sentence with a connective | Additionally, Moreover, Furthermore | Start with the content |
| Summary closers | ends every paragraph by restating it | Overall, …; In summary, … | End when the point is made |
| Hedge stacks | piles up qualifiers | may potentially, could possibly | One hedge, on the uncertain part |
| Throat-clearing and sign-offs | opens with no content, closes with chat | In this paper we delve into; I hope this helps | Start with the result; stop when done |
| Uniform cadence | makes every sentence and paragraph the same length | sentence length spread (CV) below about 0.35 | Vary them; a short sentence lands a point |
| Decorative formatting | formats prose as a slide | bold lead-ins on every bullet, Title Case Headings, emoji, bullets for an argument | Sentence-case headings; bullets only for parallel items; prose for reasoning |
| Dash habit | uses an em dash in sentence after sentence | — | Commas, colons, parentheses or two sentences |

The last three are checked the same way in every language. The rest depend on the language's own vocabulary and grammar.

## Other languages: packs

`lab-voice` keeps each language's habits in a pack: a TOML file in the project's packs folder, one per language. When it meets a text in a language that has no pack, it writes one in the same run. The pack holds:

- the language's frequent words, used to recognise it;
- its sentence rules;
- the phrases machine writing overuses in that language, for every habit above;
- examples that must and must not trigger the pack.

The pack is checked against those examples before it is used. It grows whenever a text shows a habit it misses. It is marked unreviewed until the user or a fluent reader has read it. The lab's source ships no vocabulary of any language, only the pack format (`lab-voice/assets/pack-template.toml`).

## The author's own voice

This guide applies when the user has no style sheet. When one exists (`voice-*` in the project, written by `lab-voice` from the author's own texts), it wins wherever the two disagree. The sheet records:

- the languages the author writes in;
- their sentence length;
- their choice of "we" or "I";
- their spelling variety;
- their favourite constructions;
- the words they never use.

## Source

Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup), opened 2026-10-16: <https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing>. It warns that these signs are not proof of AI use, that people also write this way, and that fixing surface signs is not enough when the content underneath is wrong.
