# `bam-core`

Re-usable functions and settings for automations.

## how to install:

Run the following

```bash
python3.9 -m venv .venv # create a virtualenv
source .venv/bin/activate # activate it
pip3.9 install -e .
pip install pytest
```

## what's in here?

* [`bam_core.lib`](bam_core/lib/): classes for interacting with common services.
* [`bam_core.utils`](bam_core/utils/): assorted utilities.
* [`bam_core.function`](bam_core/function.py): the main class to inherit from when creating a digital ocean function
* [`bam_core.settings`](bam_core/settings.py): Shared constants and env-based settings.
* [`tests`](tests/): tests run via `pytest -vv .`