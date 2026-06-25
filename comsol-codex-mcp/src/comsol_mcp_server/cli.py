from __future__ import annotations

import argparse
import json

from .config import find_comsol_install
from .recipes import get_recipe, list_recipes
from .tools import collect_outputs, compile_java_model, inspect_batch_log, run_comsol_batch, search_completion_xml


def dump(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(prog="comsol-tool")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("find-install")

    p = sub.add_parser("compile")
    p.add_argument("java_file")
    p.add_argument("--timeout-s", type=int, default=300)

    p = sub.add_parser("batch")
    p.add_argument("class_file")
    p.add_argument("output_file")
    p.add_argument("--batch-log")
    p.add_argument("--stderr-file")
    p.add_argument("--timeout-s", type=int, default=3600)

    p = sub.add_parser("inspect-log")
    p.add_argument("log_file")

    p = sub.add_parser("search-feature")
    p.add_argument("keyword")
    p.add_argument("--comsol-root")

    p = sub.add_parser("collect")
    p.add_argument("source_dir")
    p.add_argument("zip_file")

    p = sub.add_parser("recipe")
    p.add_argument("name", nargs="?")

    args = parser.parse_args()
    if args.cmd == "find-install":
        dump(find_comsol_install().as_dict())
    elif args.cmd == "compile":
        dump(compile_java_model(args.java_file, args.timeout_s))
    elif args.cmd == "batch":
        dump(run_comsol_batch(args.class_file, args.output_file, args.batch_log, args.stderr_file, args.timeout_s))
    elif args.cmd == "inspect-log":
        dump(inspect_batch_log(args.log_file))
    elif args.cmd == "search-feature":
        dump(search_completion_xml(args.keyword, args.comsol_root))
    elif args.cmd == "collect":
        dump(collect_outputs(args.source_dir, args.zip_file))
    elif args.cmd == "recipe":
        dump({"recipes": list_recipes()} if not args.name else get_recipe(args.name))


if __name__ == "__main__":
    main()

