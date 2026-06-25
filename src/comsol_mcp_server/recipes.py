RECIPES: dict[str, str] = {
    "batch_stdout": """Use System.out for data and redirect stdout from comsolbatch.
COMSOL batch Java classes may be blocked from FileWriter/FileOutputStream by the security manager.
Call System.out.flush() after large sections so long-running jobs expose progress and data promptly.""",
    "feature_discovery": """For Java API feature names, prefer runtime feature.properties() and getAllowedPropertyValues().
If the model cannot be created yet, search data/completion/physics.xml and use the XML name attribute, not the GUI descr.""",
    "boundary_diagnostics": """Boundary IDs can change when geometry layers change.
Create small diagnostic models, apply a known force/temperature condition to candidate boundaries, and verify a scalar response before launching large sweeps.""",
    "transient_solid_performance": """Full inertial 3D Solid Mechanics transient can be dominated by elastic-wave time steps.
For PINN-style quasi-static thermo-mechanical fields, consider one transient study with Heat Transfer active and Solid rho overridden to 0 kg/m^3, while keeping physical thermal density in material properties.""",
    "output_packaging": """Keep Git repositories light.
Track Java/Python scripts, manifests, summaries, and README files. Put .mph, raw stdout, logs, and large field CSVs in releases or external object storage.""",
}


def list_recipes() -> list[str]:
    return sorted(RECIPES)


def get_recipe(name: str) -> dict[str, object]:
    if name not in RECIPES:
        return {"ok": False, "error": f"Unknown recipe: {name}", "available": list_recipes()}
    return {"ok": True, "name": name, "text": RECIPES[name]}

