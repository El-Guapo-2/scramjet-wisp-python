<h1 align="center">Scramjet</h1>
<div align="center">
  <img src="assets/scramjet.png" height="200" />
</div>

<div align="center">
  <a href="https://www.npmjs.com/package/@mercuryworkshop/scramjet"><img src="https://img.shields.io/npm/v/@mercuryworkshop/scramjet.svg?maxAge=3600" alt="npm version" /></a>
  <img src="https://img.shields.io/github/issues/MercuryWorkshop/scramjet?style=flat&color=orange" />
  <img src="https://img.shields.io/github/stars/MercuryWorkshop/scramjet?style=flat&color=orange" />
</div>

---

Scramjet is an experimental interception-based web proxy designed to evade internet censorship and bypass arbitrary browser restrictions.<br><br>
Scramjet allows you to sandbox arbitrary web content, bypass CORS restrictions on loading websites, and instrument and debug websites inside the browser itself. This is accomplished through a combination of interception, rewriting, and sandboxing techniques. You can learn more about the technical details <a href="https://developer.puter.com/blog/how-I-ported-the-web-to-the-web/"><strong>here</strong></a>.<br><br>

<div align="center">
 <a href="https://github.com/MercuryWorkshop/scramjet/wiki">Documentation</a> | <a href="https://scramjet.mercurywork.shop">Playground</a> | <a href="https://discord.gg/tmApqGqfX2">Discord</a>
</div>

## Supported Sites

Some of the popular websites that Scramjet supports include:

- [Google](https://google.com)
- [Youtube](https://youtube.com)
- [Instagram](https://instagram.com)
- [ChatGPT](https://chatgpt.com)
- [Reddit](https://reddit.com)
- [Twitter](https://twitter.com)
- [Discord](https://discord.com)
- [Spotify](https://spotify.com)
- [GeForce NOW](https://play.geforcenow.com/)
- [now.gg](https://now.gg)

## Running Without Node.js

The included Python launcher runs both the static Scramjet proxy page and the
Wisp server. Node.js, npm, pnpm, Rust, and a frontend build are not required.
CPython 3.11 through 3.14.2 is supported. On Python 3.14, the launcher uses
a single interpreter because `wisp-python` currently attempts to load native
dependencies such as `psutil` in subinterpreters, which Python 3.14 does not
allow.

Install the maintained Python Wisp implementation in a virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install wisp-python
```

Start the proxy:

```sh
python python_server.py --allow-loopback --allow-private
```

Open <http://127.0.0.1:3030>. The Wisp WebSocket endpoint uses the same
origin. The included `service-worker.js` registers the Scramjet service worker,
and the browser bootstrap bundle is loaded from jsDelivr. The first page load
may ask the browser to reload once while the service worker activates. To use a
different port:

```sh
python python_server.py --port 8080 --allow-loopback --allow-private
```

The `--allow-loopback` and `--allow-private` options are useful for local
development only. Do not enable them on a publicly reachable server unless
you intentionally want to allow access to private network addresses.

The included service worker also applies a compatibility fix for the published
Scramjet bootstrap bundle, which otherwise cannot resolve the current
controller's Scramjet peer dependency.

The launcher opens `http://127.0.0.1:3030/` in the default browser
automatically. Use `--no-browser` to disable this behavior.

## Windows executable

The repository includes a console-mode Windows x64 build workflow. Run the
`Build Windows executable` workflow manually from GitHub Actions and download
the `scramjet-python-server-windows-x64` artifact. The executable keeps its
terminal window open while the server runs and opens the default browser
automatically. The workflow bundles the Python runtime, Wisp dependencies, and
frontend assets; Python does not need to be installed on the target machine.
