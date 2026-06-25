# Examples

## `MinimalModel.java`

A tiny COMSOL Java API model used for smoke testing compile and batch execution.

It creates a 3D block, prints a small stdout section, and saves `MinimalModel.mph`.

Run:

```bash
comsol-tool compile examples/MinimalModel.java
mkdir -p outputs
comsol-tool batch examples/MinimalModel.class outputs/minimal_stdout.txt --batch-log outputs/minimal_batch.log --stderr-file outputs/minimal_stderr.log
```

## `project_adapter.yaml`

A sketch of how a project can describe its Java entrypoint, output locations, and packaging rules.

The generic MCP server does not yet load this file automatically. It is included to show the intended adapter direction.

## `mcp_config.json`

Example MCP client configuration.

Update `COMSOL_HOME` for your machine before use.

