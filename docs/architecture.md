# Architecture

`comsol-codex-mcp` is split into three layers.

## 1. Core Toolkit

The core toolkit is plain Python and has no MCP dependency:

- `config.py`: local COMSOL discovery;
- `tools.py`: compile, batch run, log inspection, XML search, output packaging;
- `recipes.py`: short built-in workflow notes.

This makes the package testable on machines without COMSOL or MCP installed.

## 2. MCP Server

`server.py` wraps core functions with `mcp.server.fastmcp.FastMCP`.

The MCP layer is intentionally thin. It should not contain physics-specific logic. It exposes actions an agent can call, while the user or project provides the actual COMSOL Java model.

## 3. Project Adapter

Every COMSOL project is different. A project adapter can be:

- a Java API template;
- a YAML case matrix;
- a project-specific parser for stdout sections;
- a validation script that compares outputs against expected metrics.

Keep adapters outside the generic MCP server unless they are broadly reusable.

## Data Flow

```text
Agent
  |
  | MCP tool call
  v
COMSOL MCP server
  |
  | subprocess, shell=False
  v
comsolcompile / comsolbatch
  |
  | stdout, stderr, batch log
  v
Project parser and result packager
```

## Design Principles

- Prefer explicit batch workflows over hidden GUI state.
- Keep generated data out of Git.
- Make logs and command lines visible.
- Probe small models before launching full sweeps.
- Treat Java API feature/property discovery as a first-class workflow.

