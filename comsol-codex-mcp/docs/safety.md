# Safety

COMSOL Codex MCP helps agents operate COMSOL, but it does not make generated model code inherently safe.

## Trust Boundary

Treat COMSOL Java API scripts as executable code.

Before running a generated `.java` file:

- inspect the script;
- confirm output paths;
- confirm model save paths;
- confirm simulation size and timeout;
- confirm whether it can consume license seats for long periods.

## Why `shell=False`

The toolkit uses `subprocess.run([...], shell=False)` for compile and batch operations. This avoids shell interpolation and reduces accidental command injection risk.

It does not sandbox COMSOL or Java code.

## Generated Files

COMSOL commonly creates:

- `.class`
- `.mph`
- `.log`
- `.status`
- `.recovery`
- raw stdout dumps

The default `.gitignore` and packaging tools exclude these.

## Logs

Logs can contain:

- absolute paths;
- model names;
- proprietary parameter names;
- solver details;
- error traces.

Review logs before publishing them.

## Large Jobs

Agents should run small probes first:

1. compile only;
2. one material/case;
3. one short time point;
4. full sweep only after logs and outputs look sane.

Use explicit `timeout_s` values for `comsol_batch`.

