# Tool Reference

The MCP server returns JSON strings so clients can display or parse structured results consistently.

## `comsol_find_install`

Locate COMSOL executables.

Inputs: none.

Returns:

- `ok`
- `root`
- `comsolcompile`
- `comsolbatch`
- `comsol`
- `source`

## `comsol_compile`

Compile a Java API script with `comsolcompile`.

Inputs:

- `java_file`: path to `.java`
- `timeout_s`: timeout in seconds, default `300`

Returns command, return code, elapsed time, output tails, and expected `.class` path.

## `comsol_batch`

Run a compiled Java class with `comsolbatch`.

Inputs:

- `class_file`: path to `.class`
- `output_file`: stdout destination
- `batch_log`: optional COMSOL batch log path
- `stderr_file`: optional stderr path
- `timeout_s`: timeout in seconds, default `3600`

Returns command, return code, elapsed time, output paths, and log tails.

## `comsol_tail_file`

Read the tail of a file.

Inputs:

- `path`
- `max_lines`, default `80`

Returns the last lines.

## `comsol_inspect_log`

Inspect COMSOL logs for common error and progress patterns.

Inputs:

- `log_file`
- `max_errors`, default `20`

Returns:

- line count;
- detected errors;
- recent progress markers;
- recent time markers;
- log tail.

## `comsol_search_feature`

Search COMSOL completion XML for Java API hints.

Inputs:

- `keyword`
- `comsol_root`, optional
- `max_matches`, default `40`

Returns matching file, line, and XML text snippets.

## `comsol_collect_outputs`

Create a lightweight zip package.

Inputs:

- `source_dir`
- `zip_file`

Default includes:

- `*.csv`
- `*.md`
- `*.json`
- `*.yaml`
- `*.yml`
- `*.py`
- `*.java`

Default excludes:

- `*.mph`
- `*.class`
- `*.log`
- `*.status`
- `*.recovery`
- `*_raw.txt`
- `all_*_data.txt`
- `__pycache__/*`

## `comsol_clean_generated`

List or remove generated files.

Inputs:

- `directory`
- `dry_run`, default `true`

Default targets:

- `*.class`
- `*.status`
- `*.recovery`
- `__pycache__`

## `comsol_list_recipes`

List built-in recipe names.

## `comsol_get_recipe`

Read a built-in recipe.

Inputs:

- `name`

