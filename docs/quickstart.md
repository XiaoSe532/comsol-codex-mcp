# Quickstart

This guide walks through installation, local checks, and an optional COMSOL smoke test.

## 1. Install

```bash
cd comsol-codex-mcp
python -m pip install -e .
```

For MCP server support:

```bash
python -m pip install -e ".[mcp]"
```

## 2. Find COMSOL

```bash
comsol-tool find-install
```

If COMSOL is not found, set `COMSOL_HOME`.

Windows PowerShell:

```powershell
$env:COMSOL_HOME = "E:\Program Files\COMSOL\COMSOL63"
```

Linux/macOS shell:

```bash
export COMSOL_HOME=/path/to/COMSOL63
```

## 3. Search Java API Feature Names

```bash
comsol-tool search-feature ThermalContact
comsol-tool search-feature BoundaryLoad
```

This searches COMSOL completion XML for API names and topics.

## 4. Optional COMSOL Smoke Test

Compile the minimal example:

```bash
comsol-tool compile examples/MinimalModel.java
```

Run it:

```bash
mkdir -p outputs
comsol-tool batch examples/MinimalModel.class outputs/minimal_stdout.txt --batch-log outputs/minimal_batch.log --stderr-file outputs/minimal_stderr.log --timeout-s 300
```

Inspect the log:

```bash
comsol-tool inspect-log outputs/minimal_batch.log
```

Package lightweight outputs:

```bash
comsol-tool collect . outputs/minimal_package.zip
```

The package command excludes `.mph`, `.class`, logs, status/recovery files, raw stdout dumps, and other generated heavy files by default.

## 5. Run as MCP Server

```bash
comsol-mcp-server
```

Example MCP client configuration is in `examples/mcp_config.json`.

## 6. Recommended Agent Loop

1. Ask the agent to inspect COMSOL availability with `comsol_find_install`.
2. Generate or edit a Java API model script.
3. Compile with `comsol_compile`.
4. Diagnose compile errors with `comsol_search_feature`.
5. Run with `comsol_batch` using a bounded timeout.
6. Inspect logs with `comsol_inspect_log`.
7. Use a project-specific parser for stdout.
8. Package results with `comsol_collect_outputs`.

