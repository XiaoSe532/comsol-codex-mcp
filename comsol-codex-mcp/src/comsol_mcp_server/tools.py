from __future__ import annotations

import fnmatch
import os
import re
import shutil
import subprocess
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .config import find_comsol_install


ERROR_PATTERNS = [
    "Exception",
    "FATAL",
    "Failed to",
    "Singular matrix",
    "Undefined variable",
    "Unknown property",
    "Invalid property",
    "AccessControlException",
    "OutOfMemory",
]


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    returncode: int
    elapsed_s: float
    stdout_tail: str
    stderr_tail: str

    def as_dict(self) -> dict[str, object]:
        return {
            "command": self.command,
            "returncode": self.returncode,
            "elapsed_s": round(self.elapsed_s, 3),
            "stdout_tail": self.stdout_tail,
            "stderr_tail": self.stderr_tail,
        }


def _resolve(path: str | Path, base_dir: str | Path | None = None) -> Path:
    p = Path(path)
    if not p.is_absolute() and base_dir:
        p = Path(base_dir) / p
    return p.resolve()


def _tail_text(path: Path, max_chars: int = 6000) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    return data[-max_chars:].decode("utf-8", errors="replace")


def tail_file(path: str, max_lines: int = 80) -> dict[str, object]:
    p = _resolve(path)
    if not p.exists():
        return {"ok": False, "error": f"File not found: {p}"}
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    return {"ok": True, "path": str(p), "lines": lines[-max_lines:]}


def compile_java_model(java_file: str, timeout_s: int = 300) -> dict[str, object]:
    install = find_comsol_install()
    if not install.comsolcompile:
        return {"ok": False, "error": "comsolcompile not found", "install": install.as_dict()}
    java_path = _resolve(java_file)
    if not java_path.exists():
        return {"ok": False, "error": f"Java file not found: {java_path}"}
    cmd = [str(install.comsolcompile), str(java_path)]
    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, cwd=str(java_path.parent))
    result = CommandResult(
        command=cmd,
        returncode=proc.returncode,
        elapsed_s=time.time() - started,
        stdout_tail=proc.stdout[-6000:],
        stderr_tail=proc.stderr[-6000:],
    ).as_dict()
    result["ok"] = proc.returncode == 0
    result["class_file"] = str(java_path.with_suffix(".class"))
    return result


def run_comsol_batch(
    class_file: str,
    output_file: str,
    batch_log: str | None = None,
    stderr_file: str | None = None,
    timeout_s: int = 3600,
) -> dict[str, object]:
    install = find_comsol_install()
    if not install.comsolbatch:
        return {"ok": False, "error": "comsolbatch not found", "install": install.as_dict()}
    class_path = _resolve(class_file)
    if not class_path.exists():
        return {"ok": False, "error": f"Class file not found: {class_path}"}

    out_path = _resolve(output_file, class_path.parent)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    log_path = _resolve(batch_log or f"{class_path.stem}_batch.log", class_path.parent)
    err_path = _resolve(stderr_file or f"{class_path.stem}_stderr.log", class_path.parent)

    cmd = [str(install.comsolbatch), "-inputfile", str(class_path), "-batchlog", str(log_path)]
    started = time.time()
    with out_path.open("w", encoding="utf-8", errors="replace") as stdout, err_path.open(
        "w", encoding="utf-8", errors="replace"
    ) as stderr:
        proc = subprocess.run(cmd, stdout=stdout, stderr=stderr, text=True, timeout=timeout_s, cwd=str(class_path.parent))

    return {
        "ok": proc.returncode == 0,
        "command": cmd,
        "returncode": proc.returncode,
        "elapsed_s": round(time.time() - started, 3),
        "output_file": str(out_path),
        "batch_log": str(log_path),
        "stderr_file": str(err_path),
        "batch_log_tail": _tail_text(log_path),
        "stderr_tail": _tail_text(err_path),
    }


def inspect_batch_log(log_file: str, max_errors: int = 20) -> dict[str, object]:
    path = _resolve(log_file)
    if not path.exists():
        return {"ok": False, "error": f"Log not found: {path}"}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    errors = [line for line in lines if any(pat.lower() in line.lower() for pat in ERROR_PATTERNS)]
    progress = [line for line in lines if "progress" in line.lower() or "当前进度" in line]
    time_markers = [line for line in lines if re.search(r"\b(t|time)\b", line, re.I)]
    return {
        "ok": True,
        "path": str(path),
        "line_count": len(lines),
        "errors": errors[-max_errors:],
        "last_progress": progress[-20:],
        "last_time_markers": time_markers[-20:],
        "tail": lines[-80:],
    }


def search_completion_xml(keyword: str, comsol_root: str | None = None, max_matches: int = 40) -> dict[str, object]:
    install = find_comsol_install()
    roots: list[Path] = []
    if comsol_root:
        roots.append(_resolve(comsol_root))
    if install.root:
        roots.append(install.root)
    for exe in (install.comsolcompile, install.comsolbatch):
        if exe:
            roots.append(exe.parents[2] if len(exe.parents) > 2 else exe.parent)
    candidates: list[Path] = []
    for root in roots:
        candidates.extend(root.glob("**/data/completion/physics.xml"))
        candidates.extend(root.glob("**/data/completion/common.xml"))
    seen: set[Path] = set()
    matches: list[dict[str, object]] = []
    for xml in candidates:
        if xml in seen or not xml.exists():
            continue
        seen.add(xml)
        for i, line in enumerate(xml.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            if keyword.lower() in line.lower():
                matches.append({"file": str(xml), "line": i, "text": line.strip()})
                if len(matches) >= max_matches:
                    return {"ok": True, "matches": matches}
    return {"ok": True, "matches": matches}


def collect_outputs(
    source_dir: str,
    zip_file: str,
    include: Iterable[str] | None = None,
    exclude: Iterable[str] | None = None,
) -> dict[str, object]:
    src = _resolve(source_dir)
    if not src.is_dir():
        return {"ok": False, "error": f"Source directory not found: {src}"}
    dst = _resolve(zip_file, src.parent)
    dst.parent.mkdir(parents=True, exist_ok=True)
    include_patterns = list(include or ["*.csv", "*.md", "*.json", "*.yaml", "*.yml", "*.py", "*.java"])
    exclude_patterns = list(
        exclude
        or ["*.mph", "*.class", "*.log", "*.status", "*.recovery", "*_raw.txt", "all_*_data.txt", "__pycache__/*"]
    )

    def keep(rel: str) -> bool:
        rel_norm = rel.replace(os.sep, "/")
        if not any(fnmatch.fnmatch(rel_norm, pat) or fnmatch.fnmatch(Path(rel_norm).name, pat) for pat in include_patterns):
            return False
        if any(fnmatch.fnmatch(rel_norm, pat) or fnmatch.fnmatch(Path(rel_norm).name, pat) for pat in exclude_patterns):
            return False
        return True

    count = 0
    total_bytes = 0
    with zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for file in src.rglob("*"):
            if not file.is_file():
                continue
            rel = str(file.relative_to(src))
            if keep(rel):
                zf.write(file, rel)
                count += 1
                total_bytes += file.stat().st_size
    return {
        "ok": True,
        "zip_file": str(dst),
        "file_count": count,
        "source_size_mb": round(total_bytes / (1024 * 1024), 3),
        "zip_size_mb": round(dst.stat().st_size / (1024 * 1024), 3),
    }


def clean_generated(directory: str, patterns: Iterable[str] | None = None, dry_run: bool = True) -> dict[str, object]:
    root = _resolve(directory)
    if not root.is_dir():
        return {"ok": False, "error": f"Directory not found: {root}"}
    pats = list(patterns or ["*.class", "*.status", "*.recovery", "__pycache__"])
    targets: list[Path] = []
    for pat in pats:
        targets.extend(root.rglob(pat))
    targets = sorted(set(targets))
    if not dry_run:
        for target in targets:
            if target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
    return {"ok": True, "dry_run": dry_run, "targets": [str(t) for t in targets]}

