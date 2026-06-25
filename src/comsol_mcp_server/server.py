from __future__ import annotations

import json
from typing import Any

from .config import find_comsol_install
from .recipes import get_recipe, list_recipes
from .tools import (
    clean_generated,
    collect_outputs,
    compile_java_model,
    inspect_batch_log,
    run_comsol_batch,
    search_completion_xml,
    tail_file,
)


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def main() -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "The MCP SDK is not installed. Install with: pip install 'comsol-codex-mcp[mcp]'\n"
            f"Import error: {exc}"
        )

    mcp = FastMCP("comsol-codex-mcp")

    @mcp.tool()
    def comsol_find_install() -> str:
        """Locate COMSOL compile and batch executables."""
        return _json(find_comsol_install().as_dict())

    @mcp.tool()
    def comsol_compile(java_file: str, timeout_s: int = 300) -> str:
        """Compile a COMSOL Java API model with comsolcompile."""
        return _json(compile_java_model(java_file, timeout_s))

    @mcp.tool()
    def comsol_batch(
        class_file: str,
        output_file: str,
        batch_log: str | None = None,
        stderr_file: str | None = None,
        timeout_s: int = 3600,
    ) -> str:
        """Run a compiled COMSOL Java class with comsolbatch."""
        return _json(run_comsol_batch(class_file, output_file, batch_log, stderr_file, timeout_s))

    @mcp.tool()
    def comsol_tail_file(path: str, max_lines: int = 80) -> str:
        """Read the tail of a COMSOL log or output file."""
        return _json(tail_file(path, max_lines))

    @mcp.tool()
    def comsol_inspect_log(log_file: str, max_errors: int = 20) -> str:
        """Inspect a COMSOL batch log for common errors and progress markers."""
        return _json(inspect_batch_log(log_file, max_errors))

    @mcp.tool()
    def comsol_search_feature(keyword: str, comsol_root: str | None = None, max_matches: int = 40) -> str:
        """Search COMSOL completion XML for Java API feature/property hints."""
        return _json(search_completion_xml(keyword, comsol_root, max_matches))

    @mcp.tool()
    def comsol_collect_outputs(source_dir: str, zip_file: str) -> str:
        """Create a lightweight zip of scripts, summaries, and CSV outputs."""
        return _json(collect_outputs(source_dir, zip_file))

    @mcp.tool()
    def comsol_clean_generated(directory: str, dry_run: bool = True) -> str:
        """List or remove generated class/status/recovery/cache files."""
        return _json(clean_generated(directory, dry_run=dry_run))

    @mcp.tool()
    def comsol_list_recipes() -> str:
        """List built-in COMSOL agent workflow recipes."""
        return _json({"recipes": list_recipes()})

    @mcp.tool()
    def comsol_get_recipe(name: str) -> str:
        """Read a built-in COMSOL agent workflow recipe."""
        return _json(get_recipe(name))

    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()

