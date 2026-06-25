# Contributing

Thanks for helping improve COMSOL Codex MCP.

This project is meant to stay generic. Contributions should improve the reusable COMSOL automation layer, not add one-off simulation models.

## Development Setup

```bash
git clone https://github.com/XiaoSe532/Comsol-Codex-mcp
cd comsol-codex-mcp
python -m pip install -e ".[dev]"
```

Run the standard-library test suite:

```bash
python -m unittest discover -s tests -p "test_*.py"
python -m compileall -q src
```

If you have COMSOL installed, also run:

```bash
comsol-tool find-install
comsol-tool search-feature ThermalContact
```

## Contribution Types

Good contributions include:

- new generic MCP tools;
- safer compile/run/monitor behavior;
- better COMSOL install discovery;
- log diagnosis rules;
- Java API feature/property discovery helpers;
- documentation and recipes;
- compatibility notes for COMSOL versions and operating systems.

Avoid:

- project-specific geometry or physics hard-coded into the server;
- committing `.mph`, `.class`, raw stdout, large field CSVs, or batch logs;
- tool behavior that silently runs arbitrary generated code without explicit user action.

## Tool Design Guidelines

- Keep core logic in plain Python modules first.
- Wrap core logic in `server.py` only after it is testable without MCP.
- Return structured JSON-compatible dictionaries.
- Include command lines, return codes, log paths, and short log tails.
- Use `subprocess.run([...], shell=False)`.
- Add tests for parsing, packaging, and safety behavior whenever possible.

## Pull Request Checklist

- [ ] Tests pass with `python -m unittest discover -s tests -p "test_*.py"`.
- [ ] `python -m compileall -q src` passes.
- [ ] New tools are documented in `docs/tool_reference.md`.
- [ ] New recipes are documented in `docs/recipes.md` or `recipes.py`.
- [ ] No generated COMSOL artifacts are committed.
- [ ] Safety implications are mentioned when relevant.

