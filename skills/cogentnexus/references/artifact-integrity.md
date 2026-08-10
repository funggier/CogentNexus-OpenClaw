# Artifact Integrity

Repeated --hash accepts files and directories. Files use byte SHA-256. Directories use a deterministic manifest of sorted relative paths, sizes, hashes, and symlink targets while excluding .git, .cogent, __pycache__, and .pytest_cache. Completion recomputes fingerprints and rejects missing, changed, or differently typed artifacts.
