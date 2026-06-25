# Compatibility

## Tested Locally

| Component | Status |
| --- | --- |
| Python 3.13 | Basic tests pass |
| Windows PowerShell | Basic CLI tested |
| COMSOL 6.3 | Install discovery and completion XML search tested |

## Expected

| Component | Expected Support |
| --- | --- |
| Python 3.10+ | Supported by package metadata |
| Windows | Primary target for early versions |
| Linux | Expected with correct COMSOL paths, needs more testing |
| macOS | Not yet tested |
| COMSOL 6.x | Expected with minor path/API differences |
| COMSOL 5.x | Unknown |

## MCP SDK

The core toolkit does not require MCP. The MCP server entrypoint requires the optional dependency:

```bash
python -m pip install -e ".[mcp]"
```

If MCP imports fail, use the standalone CLI while diagnosing dependency issues.

## COMSOL Java API Variability

COMSOL Java API names and properties can vary across physics interfaces and versions. Prefer:

- `feature.properties()` runtime probes;
- `getAllowedPropertyValues()`;
- `comsol_search_feature`;
- small compile/run probes before full sweeps.

