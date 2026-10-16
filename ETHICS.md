# Responsible use

Research Lab is an assistance tool for researchers. It helps you do six things:

- plan your work;
- search the literature;
- question your own claims;
- check proofs, numbers and citations;
- organise your code and records;
- prepare honest release records.

It does not do research in your place, and it is not a paper generator. The ideas, the judgments, the conclusions and the words that go out under your name are yours, and so is the responsibility for them.

## What the lab is for

- **Challenge.** Kill tests, simulated review, a dequantization skeptic and a historian who knows who did it first. The lab is built to find weaknesses in your work before others do.
- **Verification.** Citations are counted as verified only after the source has been opened and quoted. Numbers must regenerate from a script and a seed, and every claim carries its evidence level.
- **Organisation.** Plans, stories, a lab notebook, a decision log, reproducible repositories and release bundles.
- **Editing support.** Feedback on structure, notation, clarity and tone of text you write.

## Commitments built into the lab

1. **You are the author.** AI tools cannot be authors. As ICMJE puts it, they "cannot be responsible for the accuracy, integrity, and originality of the work". arXiv makes the same rule: "generative AI language tools should not be listed as an author". The lab's agents propose; you decide, write and sign. Its writing workflow helps you structure, check and revise your text. Where it drafts anything at your request, the draft is marked for you to rewrite, and it never goes out unread.
2. **AI assistance is recorded and disclosed.**
   - **What gets logged.** Whenever the lab's AI help reaches something that will leave your project (text, code, figures, analyses), the lab notebook gets an AI-USE entry saying what was done and what you did with it.
   - **Turning the log into a statement.** At release, `lab-release` turns those entries into a disclosure statement for you to check and adapt to the venue's policy.
   - **Why it matters.** ICMJE asks authors to describe AI use "in both the cover letter and the submitted work", and notes that nondisclosure may be treated as misconduct.
3. **Nothing is fabricated.**
   - No invented data, results, quotes or references.
   - A reference an AI tool suggests is UNVERIFIED until someone opens the source.
   - A number with no script behind it does not go into a paper.
   - Authors remain responsible for errors in AI-assisted content, including "incorrect references" (arXiv).
4. **Editing is not disguise.** The voice editor flags generic and inflated phrasing and helps your own writing read clearly. It is not a tool for passing AI-generated text off as your own, or for getting around a venue's AI policy. When a venue asks how AI was used, the answer is the truthful one from the notebook.
5. **Peer review stays confidential.** The simulated referees exist for your own drafts. Many publishers forbid uploading manuscripts you are reviewing into AI tools. `lab-referee` checks the venue's rules first and declines when they say no.
6. **Personas are fictional.** The lab's characters are invented. Real researchers are cited for their published work and never voiced or quoted beyond what they wrote.
7. **Privacy and data.**
   - Requests to external services (Crossref, arXiv, DataCite) carry no personal data.
   - Real datasets stay under the data-protection rules that apply to them (for example GDPR or KVKK), and the lab does not move them out of your project.
   - Nothing is posted, deposited or sent anywhere on your behalf: uploading and submitting are your own steps.
8. **Disclosure timing and ownership.** Before anything is made public, the release gate asks three questions:
   - Does a patent or an employer's claim need settling first?
   - Do co-authors or funders need to approve?
   - Do the data carry restrictions?

## What the lab cannot do

The lab's agents can be wrong. They can miss prior work, misread a proof, or be confident about a false statement. That is why it insists on opened sources, rerunnable numbers and independent readings, and why its verdicts are inputs to your judgment, not replacements for it. Expert colleagues, real peer review and your own understanding of the work remain essential.

## Sources

- ICMJE, "AI use by authors", opened 2026-10-16: <https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html>
- arXiv, moderation policy on generative AI tools, opened 2026-10-16: <https://info.arxiv.org/help/moderation/index.html>
- Nature, "How to write a report" (referees and AI tools), opened 2026-10-16: <https://www.nature.com/nature/for-referees/how-to-write-a-report>
