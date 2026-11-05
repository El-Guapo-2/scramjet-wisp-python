#!/usr/bin/env python3
"""Run the Scramjet proxy template and Wisp server without Node.js."""

import argparse
import asyncio
import os
import sys
from types import SimpleNamespace
from pathlib import Path


PUBLIC = (
    Path(__file__).resolve().parent
    / "packages"
    / "create-proxy-app"
    / "templates"
    / "default"
    / "public"
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Scramjet and Wisp using Python only."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3030)
    parser.add_argument(
        "--public",
        type=Path,
        default=PUBLIC,
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
    args = parser.parse_args()

    public = args.public.resolve()
    if not public.is_dir():
        parser.error(f"static directory does not exist: {public}")

    if sys.version_info >= (3, 14):
        # wisp-python currently selects subinterpreters on 3.14, but native
        # dependencies such as psutil cannot be loaded in subinterpreters.
        from wisp.server import http

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
        return

    command = [
        sys.executable,
        "-m",
        "wisp.server",
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--static",
        str(public),
    ]
    if args.allow_loopback:
        command.append("--allow-loopback")
    if args.allow_private:
        command.append("--allow-private")

    os.execv(sys.executable, command)


if __name__ == "__main__":
    main()
