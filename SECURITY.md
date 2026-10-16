# Security policy

## Reporting a problem

Please report security problems privately, through **Security → Report a vulnerability** on this repository, not in a public issue. Leave out personal data and unpublished research content. You will get a reply, and a fix will be credited to you unless you prefer otherwise.

## What counts

- A skill or script that writes outside the project folder, or into the lab's own folder during project work.
- `tools/install_lab.py` doing anything beyond what its documentation says.
- A script sending personal data, or anything beyond bibliographic queries, over the network. `refcheck.py` is the only script that should reach the network, and it should contact only Crossref, DataCite and arXiv.
- `bundle.py` letting private files, secrets or personal data into a deposit.
- A prompt or skill that can be steered into hiding AI use or fabricating evidence.

## Supported versions

Fixes go into the latest release. Projects that link the lab get them when they update their copy. Projects that copied it get them when the installer runs again.
