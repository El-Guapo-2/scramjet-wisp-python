#!/usr/bin/env python3
"""Build a dependency-bundled Windows-friendly Scramjet .pyz archive."""

import argparse
import importlib.util
import shutil
import tempfile
import zipapp
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PACKAGES = ("wisp", "websockets", "asyncudp", "python_socks")
PUBLIC = ROOT / "packages" / "create-proxy-app" / "templates" / "default" / "public"


def ignore_bytecode(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name == "__pycache__" or name.endswith((".pyc", ".pyo"))
    }


def package_source(name: str) -> Path:
    spec = importlib.util.find_spec(name)
    if spec is None or spec.submodule_search_locations is None:
        raise RuntimeError(f"Could not find installed package: {name}")
    return Path(next(iter(spec.submodule_search_locations)))


def build(output: Path) -> None:
    if not PUBLIC.is_dir():
        raise RuntimeError(f"Frontend assets do not exist: {PUBLIC}")

    with tempfile.TemporaryDirectory(prefix="scramjet-pyz-") as directory:
        staging = Path(directory)
        shutil.copy2(ROOT / "python_server.py", staging / "__main__.py")

        for package in PACKAGES:
            shutil.copytree(
                package_source(package),
                staging / package,
                ignore=ignore_bytecode,
            )

        public = staging / "scramjet_public"
        public.mkdir()
        (public / "__init__.py").write_text("", encoding="utf-8")
        for source in PUBLIC.iterdir():
            destination = public / source.name
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

        # Wisp only uses psutil for the optional --outbound-iface flag. Avoid
        # bundling its native extension so this archive runs on Windows.
        (staging / "psutil.py").write_text(
            "def net_if_addrs():\n"
            "    return {}\n",
            encoding="utf-8",
        )

        output.parent.mkdir(parents=True, exist_ok=True)
        zipapp.create_archive(
            staging,
            output,
            interpreter="/usr/bin/env python3",
            compressed=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=ROOT / "python_server.pyz",
        help="output archive path",
    )
    args = parser.parse_args()
    build(args.output.resolve())
    print(f"Created {args.output.resolve()}")


if __name__ == "__main__":
    main()
