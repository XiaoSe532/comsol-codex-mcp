# COMSOL Codex MCP

An MCP server and agent toolkit for reproducible COMSOL Multiphysics batch workflows.

This project is intentionally generic. It does not encode one specific COMSOL model. Instead, it gives AI agents a safe, auditable way to:

- discover a local COMSOL installation;
- compile Java API model scripts with `comsolcompile`;
- run compiled classes with `comsolbatch`;
- monitor and diagnose logs;
- search COMSOL completion XML for Java API feature/property names;
- collect lightweight result packages while excluding `.mph`, raw dumps, logs, and generated classes;
- expose reusable COMSOL automation recipes to Codex/Claude-style agents through MCP tools.

## Why This Exists

Several COMSOL MCP projects focus on GUI automation or Python MPh/mphserver workflows. This project focuses on the engineering loop that coding agents often need:

```text
write Java API model -> compile -> batch run -> inspect log -> parse output -> package results
```

That loop is useful for long-running, reproducible simulation jobs where opening COMSOL Desktop is undesirable or impossible.

## Install

```bash
python -m pip install -e .
```

To run as an MCP server:

```bash
python -m pip install -e ".[mcp]"
comsol-mcp-server
```

To use the standalone CLI:

```bash
comsol-tool find-install
comsol-tool search-feature ThermalContact
comsol-tool inspect-log path/to/batch.log
```

## Documentation

- [Quickstart](docs/quickstart.md)
- [Tool reference](docs/tool_reference.md)
- [Architecture](docs/architecture.md)
- [Recipes](docs/recipes.md)
- [Safety](docs/safety.md)
- [Compatibility](docs/compatibility.md)
- [Comparison with related projects](docs/comparison.md)
- [Examples](examples/README.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## MCP Tools

The server exposes:

| Tool | Purpose |
| --- | --- |
| `comsol_find_install` | Locate `comsolcompile`, `comsolbatch`, and `comsol` |
| `comsol_compile` | Compile a COMSOL Java API model |
| `comsol_batch` | Run a compiled class with `comsolbatch` |
| `comsol_tail_file` | Read the tail of a log/output file |
| `comsol_inspect_log` | Detect common COMSOL errors and progress markers |
| `comsol_search_feature` | Search `physics.xml`/`common.xml` for Java API hints |
| `comsol_collect_outputs` | Zip lightweight scripts/summaries/CSV outputs |
| `comsol_clean_generated` | List or remove generated class/status/recovery files |
| `comsol_list_recipes` | List built-in workflow recipes |
| `comsol_get_recipe` | Read a built-in workflow recipe |

## Example Agent Workflow

1. Call `comsol_find_install`.
2. Ask the model to generate or modify a Java API script.
3. Call `comsol_compile`.
4. If compilation fails, use the compiler output and `comsol_search_feature`.
5. Call `comsol_batch` with a bounded timeout.
6. If the run is slow or fails, call `comsol_inspect_log`.
7. Parse model stdout with a project-specific parser.
8. Call `comsol_collect_outputs` to create an uploadable result bundle.

## COMSOL Setup

The install finder checks:

- `COMSOL_HOME`
- `COMSOL_ROOT`
- `PATH`
- common Windows locations such as `C:\Program Files\COMSOL` and `E:\Program Files\COMSOL`
- common Linux locations such as `/usr/local/comsol` and `/opt/comsol`

If discovery fails, set:

```bash
COMSOL_HOME=/path/to/COMSOL63
```

On Windows PowerShell:

```powershell
$env:COMSOL_HOME = "E:\Program Files\COMSOL\COMSOL63"
```

## Safety Model

This toolkit is deliberately conservative:

- it uses `subprocess.run([...], shell=False)`;
- it keeps compile/run operations explicit;
- it separates stdout, stderr, and batch logs;
- it excludes heavy/generated files from packages by default;
- it provides diagnostics rather than hiding COMSOL failures.

You should still run it only on trusted COMSOL Java scripts. A COMSOL Java class can create, solve, and save models on your machine.

## What This Is Not

- It is not a replacement for COMSOL Desktop.
- It is not a universal physics model generator.
- It does not ship COMSOL, licenses, or proprietary documentation.
- It does not guarantee that a generated Java API script is physically valid.

## Related Work

Existing public projects include GUI-driven COMSOL MCP servers, MPh/mphserver-based MCP servers, and Pythonic COMSOL scripting interfaces. This project aims to complement them with a batch-first, Codex-friendly, reproducible Java API workflow.

## Trademark Notice

COMSOL and COMSOL Multiphysics are trademarks or registered trademarks of COMSOL AB. This project is independent and unofficial. See [NOTICE.md](NOTICE.md).
