from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ComsolInstall:
    root: Path | None
    comsolcompile: Path | None
    comsolbatch: Path | None
    comsol: Path | None
    source: str

    @property
    def ok(self) -> bool:
        return bool(self.comsolcompile and self.comsolbatch)

    def as_dict(self) -> dict[str, str | bool | None]:
        return {
            "ok": self.ok,
            "root": str(self.root) if self.root else None,
            "comsolcompile": str(self.comsolcompile) if self.comsolcompile else None,
            "comsolbatch": str(self.comsolbatch) if self.comsolbatch else None,
            "comsol": str(self.comsol) if self.comsol else None,
            "source": self.source,
        }


def _exe_name(name: str) -> str:
    return f"{name}.exe" if os.name == "nt" else name


def _candidate_roots() -> list[tuple[str, Path]]:
    roots: list[tuple[str, Path]] = []
    for env_name in ("COMSOL_HOME", "COMSOL_ROOT"):
        value = os.environ.get(env_name)
        if value:
            roots.append((env_name, Path(value)))
    if os.name == "nt":
        roots.extend(
            [
                ("windows-default", Path(r"C:\Program Files\COMSOL")),
                ("windows-default", Path(r"E:\Program Files\COMSOL")),
            ]
        )
    else:
        roots.extend(
            [
                ("unix-default", Path("/usr/local/comsol")),
                ("unix-default", Path("/opt/comsol")),
            ]
        )
    return roots


def _find_under_root(root: Path, exe: str) -> Path | None:
    names = [
        root / "Multiphysics" / "bin" / "win64" / exe,
        root / "Multiphysics" / "bin" / "glnxa64" / exe,
        root / "bin" / "win64" / exe,
        root / "bin" / "glnxa64" / exe,
        root / exe,
    ]
    for path in names:
        if path.exists():
            return path
    if root.exists():
        matches = list(root.glob(f"**/{exe}"))
        if matches:
            return matches[0]
    return None


def find_comsol_install() -> ComsolInstall:
    compile_exe = _exe_name("comsolcompile")
    batch_exe = _exe_name("comsolbatch")
    gui_exe = _exe_name("comsol")

    path_compile = shutil.which(compile_exe)
    path_batch = shutil.which(batch_exe)
    path_gui = shutil.which(gui_exe)
    if path_compile or path_batch:
        return ComsolInstall(
            root=None,
            comsolcompile=Path(path_compile) if path_compile else None,
            comsolbatch=Path(path_batch) if path_batch else None,
            comsol=Path(path_gui) if path_gui else None,
            source="PATH",
        )

    for source, root in _candidate_roots():
        if not root.exists():
            continue
        if root.name.lower().startswith("comsol") and (root / "Multiphysics").exists():
            roots = [root]
        else:
            roots = sorted(root.glob("COMSOL*"), reverse=True) + [root]
        for candidate in roots:
            compile_path = _find_under_root(candidate, compile_exe)
            batch_path = _find_under_root(candidate, batch_exe)
            gui_path = _find_under_root(candidate, gui_exe)
            if compile_path or batch_path:
                return ComsolInstall(candidate, compile_path, batch_path, gui_path, source)

    return ComsolInstall(None, None, None, None, "not-found")

