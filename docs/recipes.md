# COMSOL Agent Recipes

## Batch stdout export

COMSOL batch Java classes can be restricted by the Java security manager. Direct `FileWriter` or `FileOutputStream` may fail even when `model.save()` works.

Recommended pattern:

```java
System.out.println("===SENSOR_MEAN case_001===");
System.out.println("t_s,T_mean");
System.out.printf("%.4f,%.6f%n", t, value);
System.out.flush();
```

Then redirect stdout from `comsolbatch` into a raw text file and parse it afterward.

## Feature and property discovery

Use runtime probes when possible:

```java
System.out.println(java.util.Arrays.toString(
    model.component("comp1").physics("solid").feature("lemm1").properties()));
```

If the model cannot be built yet, search:

```text
COMSOL*/Multiphysics/data/completion/physics.xml
COMSOL*/Multiphysics/data/completion/common.xml
```

Use the XML `name` attribute for Java API type names. GUI labels usually appear in `descr`.

## Boundary diagnostics

Boundary numbers are not stable across geometry changes. Before running a large sweep:

1. Build the smallest geometry.
2. Print domain and boundary counts.
3. Apply a known load or temperature to candidate boundaries.
4. Evaluate a simple scalar response.
5. Record confirmed IDs in the project adapter.

## Transient solid performance

Full inertial 3D transient Solid Mechanics can be extremely slow because elastic-wave time scales force tiny time steps.

If the validation target is quasi-static thermo-mechanical fields, consider:

```java
model.component("comp1").physics("solid").feature("lemm1").set("rho_mat", "userdef");
model.component("comp1").physics("solid").feature("lemm1").set("rho", "0[kg/m^3]");
```

Keep physical thermal density and heat capacity in material properties for Heat Transfer.

Document this clearly as inertia-free transient coupling, not dynamic wave validation.

## Packaging results

Track in Git:

- Java/Python scripts;
- manifests;
- summaries;
- README and reports;
- small scalar CSVs.

Keep out of Git:

- `.mph`;
- `.class`;
- raw stdout dumps;
- batch logs;
- large field CSVs;
- zip artifacts.

Put large datasets in GitHub Releases, Zenodo, Figshare, S3, or institutional storage.

