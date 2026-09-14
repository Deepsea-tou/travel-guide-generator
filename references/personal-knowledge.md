# Personal knowledge adapter

The local profile is optional. The current request always has higher priority than derived preferences.

Pass a knowledge directory explicitly with `--knowledge-root`. The adapter reads only the documented, direct Markdown filenames and ignores every other file. Missing and empty allowlisted files do not block generation. An explicitly supplied path that is not an accessible directory produces a clear error.

The adapter returns a compact vocabulary of preference signals, weights, and decision rules. It never returns raw Markdown, snippets, filenames, resolved paths, names, events, or account data. The generator must also work with the empty profile returned by `empty_profile()`.

Personalized recommendations should record the rule that influenced them. Explicit user choices may override soft profile preferences. Safety rules remain hard constraints.

The public repository may contain this adapter and synthetic fixtures only. Real knowledge files, derived personal profiles, and personal output bundles stay local.
