#!/usr/bin/env python3
"""Run the Scramjet proxy template and Wisp server without Node.js."""

import argparse
import atexit
import asyncio
import shutil
import sys
import tempfile
import threading
import webbrowser
from types import SimpleNamespace
from pathlib import Path
from urllib.parse import urlsplit
from importlib import resources


PUBLIC = (
    Path(__file__).resolve().parent
    / "packages"
    / "create-proxy-app"
    / "templates"
    / "default"
    / "public"
)
_BUNDLED_PUBLIC = None


def default_public() -> Path:
    frozen_public = Path(getattr(sys, "_MEIPASS", "")) / "scramjet_public"
    if frozen_public.is_dir():
        return frozen_public

    if PUBLIC.is_dir():
        return PUBLIC

    global _BUNDLED_PUBLIC
    if _BUNDLED_PUBLIC is None:
        try:
            bundled = resources.files("scramjet_public")
        except ModuleNotFoundError:
            return PUBLIC

        extracted = tempfile.TemporaryDirectory(prefix="scramjet-public-")
        _BUNDLED_PUBLIC = Path(extracted.name)
        for source in bundled.iterdir():
            destination = _BUNDLED_PUBLIC / source.name
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                destination.write_bytes(source.read_bytes())
        atexit.register(extracted.cleanup)

    return _BUNDLED_PUBLIC


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Scramjet and Wisp using Python only."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3030)
    parser.add_argument(
        "--public",
        type=Path,
        default=None,
        help="directory containing the static proxy frontend",
    )
    parser.add_argument(
        "--allow-loopback",
        action="store_true",
        help="allow proxying to loopback addresses",
    )
    parser.add_argument(
        "--allow-private",
        action="store_true",
        help="allow proxying to private addresses",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="do not open the proxy in the default browser",
    )
    args = parser.parse_args()

    public = (args.public or default_public()).resolve()
    if not public.is_dir():
        parser.error(f"static directory does not exist: {public}")

    if not args.no_browser:
        browser_host = "127.0.0.1" if args.host in {"0.0.0.0", "::"} else args.host
        threading.Timer(
            0.5,
            webbrowser.open,
            args=(f"http://{browser_host}:{args.port}/",),
        ).start()

    # Calling the HTTP entry point directly keeps bundled dependencies
    # available and avoids subinterpreters, which cannot load native modules.
    from wisp.server import http

    request_handler = http.request_handler

    async def request_without_query(path, request_headers):
        return await request_handler(urlsplit(path).path, request_headers)

    http.request_handler = request_without_query

    asyncio.run(
        http.main(
            SimpleNamespace(
                static=str(public),
                limits=False,
                connections=30,
                bandwidth=1000,
                window=60,
                proxy=None,
                outbound_iface=None,
                allow_loopback=args.allow_loopback,
                allow_private=args.allow_private,
                block_udp=False,
                block_tcp=False,
                dns_order="verbatim",
                host=args.host,
                port=args.port,
            )
        )
    )


if __name__ == "__main__":
    main()
