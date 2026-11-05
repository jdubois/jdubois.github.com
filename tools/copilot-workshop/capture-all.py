#!/usr/bin/env python3
"""Capture four pinned Git revisions, with one owned JVM at a time."""
import argparse
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "tools/copilot-workshop/.build"
STAGES = ("start", "after-bugfix", "after-feature", "after-performance")
REFERENCES = ROOT / "workshops/copilot-app/assets/references.json"


def get_java_runtime(java):
    properties = subprocess.run([java, "-XshowSettings:properties", "-version"],
                                check=True, capture_output=True, text=True)
    settings = {}
    for line in (properties.stdout + properties.stderr).splitlines():
        name, separator, value = line.partition(" = ")
        if separator:
            settings[name.strip()] = value.strip()
    runtime = {}
    for key, name in (("version", "java.version"), ("vendor", "java.vendor"), ("vm", "java.vm.name")):
        if not settings.get(name):
            raise RuntimeError(f"Missing capture JVM property: {name}")
        runtime[key] = settings[name]
    return runtime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=18765)
    args = parser.parse_args()
    references = json.loads(REFERENCES.read_text())
    java = shutil.which("java")
    if java is None:
        raise RuntimeError("Java is required for real runtime captures")
    java_runtime = get_java_runtime(java)
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    base = f"http://127.0.0.1:{args.port}"
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", args.port)) == 0:
            raise RuntimeError(f"Port {args.port} is occupied. Choose --port or stop only your named workshop process.")
    for stage in STAGES:
        destination = BUILD / "captures" / stage
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir(parents=True)
        project = destination / "shopping-cart"
        reference = references["checkpoints"][stage]
        subprocess.run(["git", "clone", "--quiet", "--no-checkout",
                        references["repository"] + ".git", str(project)], check=True)
        revision = subprocess.check_output(
            ["git", "-C", str(project), "rev-parse", reference["tag"] + "^{commit}"],
            text=True).strip()
        if revision != reference["commit"]:
            raise RuntimeError(f"Published tag moved: {reference['tag']}")
        subprocess.run(["git", "-C", str(project), "checkout", "--quiet", "--detach",
                        revision], check=True)
        with (BUILD / f"capture-{stage}.log").open("w") as log:
            subprocess.run(["./mvnw", "-q", "-DskipTests", "package"],
                           cwd=project, stdout=log, stderr=subprocess.STDOUT, check=True)
            process = subprocess.Popen(
                [java, "-jar", "target/shopping-cart-1.0.0.jar",
                 f"--workshop.revision={revision}", f"--server.port={args.port}"],
                cwd=project, stdout=log, stderr=subprocess.STDOUT)
            try:
                deadline = time.monotonic() + 90
                while True:
                    if process.poll() is not None:
                        raise RuntimeError(f"{stage} stopped during startup; see its capture log")
                    try:
                        with urlopen(f"{base}/api/workshop", timeout=1) as response:
                            if response.status == 200:
                                identity = json.load(response)
                                expected = {"application": "shopping-cart",
                                            "revision": revision,
                                            "processId": process.pid}
                                if identity != expected:
                                    raise RuntimeError(f"Port {args.port} belongs to another process: {identity}")
                                break
                    except URLError:
                        if time.monotonic() >= deadline:
                            raise RuntimeError(f"{stage} did not become ready in 90 seconds")
                        time.sleep(.25)
                env = {**os.environ, "WORKSHOP_STAGE": stage,
                       "WORKSHOP_URL": base, "WORKSHOP_JAVA_RUNTIME": json.dumps(java_runtime)}
                subprocess.run(["npm", "--prefix", "tools/copilot-workshop", "run", "capture"],
                               cwd=ROOT, env=env, check=True)
            finally:
                process.terminate()
                try:
                    process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        print(f"Captured and stopped {stage}", flush=True)


if __name__ == "__main__":
    main()
