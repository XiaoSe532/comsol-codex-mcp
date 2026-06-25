# Security Policy

## Supported Versions

This project is currently pre-1.0. Security fixes are applied to the latest main branch until release branches are introduced.

## Reporting a Vulnerability

Please open a private security advisory on GitHub if available, or contact the maintainers privately before publishing exploit details.

Include:

- affected version or commit;
- operating system;
- COMSOL version;
- exact tool call or CLI command;
- expected and observed behavior;
- whether untrusted Java, model files, or logs were involved.

## Security Model

COMSOL Codex MCP can compile and run COMSOL Java API code. Treat COMSOL Java scripts as executable code.

Risks include:

- Java code creating, modifying, or saving files;
- COMSOL models consuming large CPU, memory, license seats, or disk space;
- generated scripts running long simulations;
- logs and outputs containing sensitive local paths or proprietary model details.

The toolkit reduces accidental risk by:

- using `subprocess.run([...], shell=False)`;
- requiring explicit compile and batch tool calls;
- separating stdout, stderr, and batch logs;
- excluding heavy/generated files from packaging by default;
- making command lines and log paths visible.

It does not sandbox COMSOL itself. Run only trusted COMSOL Java scripts and review generated code before executing it.

## Data Handling

Do not publish:

- proprietary `.mph` models;
- license files;
- private COMSOL installation paths if they reveal sensitive information;
- raw logs or stdout dumps that include confidential project data.

Use `comsol_collect_outputs` or the documented packaging patterns to create lightweight, reviewable archives.

