#!/usr/bin/env python3
"""Checks for this repository. Standard library only.

python3 scripts/check.py          offline checks
python3 scripts/check.py --live   also compare with the published docs
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "https://app.proofage.net/mcp/admin"
TOOLS_URL = "https://docs.proofage.net/integration/mcp/tools.md"
PROMPT_URL = "https://docs.proofage.net/integration/integration-prompt.md"
ROLE_NAMES = {"administrator": "Administrator", "developer": "Developer", "support_specialist": "Support specialist"}
errors = []


def fail(msg):
    errors.append(msg)
    print("FAIL " + msg)


def load_json(rel):
    try:
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        fail(f"{rel}: {e}")
        return None


def offline():
    files = [".mcp.json", ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
             ".cursor-plugin/plugin.json", "server.json", "tools.json", "tools.meta.json"]
    data = {f: load_json(f) for f in files}

    # versions
    versions = {
        ".claude-plugin/plugin.json": (data[".claude-plugin/plugin.json"] or {}).get("version"),
        ".cursor-plugin/plugin.json": (data[".cursor-plugin/plugin.json"] or {}).get("version"),
        "server.json": (data["server.json"] or {}).get("version"),
    }
    if len(set(versions.values())) != 1 or None in versions.values():
        fail(f"versions differ: {versions}")

    # endpoint
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    mcp = data[".mcp.json"] or {}
    urls = {
        ".mcp.json": (mcp.get("mcpServers", {}).get("proofage") or {}).get("url"),
        "server.json": ((data["server.json"] or {}).get("remotes") or [{}])[0].get("url"),
        "README.md": ENDPOINT if ENDPOINT in readme else None,
    }
    for f, u in urls.items():
        if u != ENDPOINT:
            fail(f"{f}: endpoint is {u!r}, expected {ENDPOINT}")

    # tools vs meta
    tools, meta = data["tools.json"], data["tools.meta.json"]
    if tools is not None and meta is not None:
        names = {t["name"] for t in tools}
        for n in sorted(names - set(meta)):
            fail(f"tools.meta.json has no entry for tool {n}")
        for n in sorted(set(meta) - names):
            fail(f"tools.meta.json has an entry for unknown tool {n}")
        for n, m in meta.items():
            if not m.get("group") or not m.get("summary"):
                fail(f"tools.meta.json: {n} needs group and summary")
            elif len(m["summary"]) > 100:
                fail(f"tools.meta.json: summary of {n} is over 100 characters")

    # generated files
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "render.py"), "--check"], capture_output=True, text=True)
    if r.returncode != 0:
        fail("render.py --check: " + (r.stdout + r.stderr).strip())

    # skills
    for d in sorted((ROOT / "skills").iterdir()):
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        fm = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M)) if m else {}
        for k in ("name", "description"):
            if not fm.get(k):
                fail(f"{d.name}/SKILL.md: missing {k}")
        if fm.get("name") and fm["name"] != d.name:
            fail(f"{d.name}/SKILL.md: name {fm['name']!r} differs from folder")

    # rule
    if not re.match(r"---\n.*description:.*\n---\n", (ROOT / "rules" / "proofage.mdc").read_text(encoding="utf-8"), re.S):
        fail("rules/proofage.mdc: missing description frontmatter")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proofage-mcp-repo-check"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def norm(s):
    """Drop markdown escaping and whitespace so rendered and raw text compare equal."""
    s = s.replace("\\", "").replace("*", "").replace("_", "")
    return re.sub(r"\s+", "", s)


def live():
    try:
        md = fetch(TOOLS_URL)
        prompt_md = fetch(PROMPT_URL)
    except Exception as e:  # noqa: BLE001
        fail(f"live fetch failed: {e}")
        return
    rows = {}
    for line in md.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) != 3:
            fail(f"live tools page: cannot parse row {line[:60]!r}")
            continue
        rows[cells[0].strip("`")] = (cells[1], cells[2])
    tools = json.loads((ROOT / "tools.json").read_text(encoding="utf-8"))
    local = {t["name"]: t for t in tools}
    for n in sorted(set(rows) - set(local)):
        fail(f"live docs list tool {n}, tools.json does not")
    for n in sorted(set(local) - set(rows)):
        fail(f"tools.json has tool {n}, live docs do not")
    for n in sorted(set(local) & set(rows)):
        desc, roles = rows[n]
        if norm(desc) != norm(local[n]["description"]):
            fail(f"{n}: description differs from live docs")
        want = ", ".join(ROLE_NAMES.get(r, r) for r in local[n]["roles"])
        if norm(roles) != norm(want):
            fail(f"{n}: roles differ from live docs ({roles!r} vs {want!r})")
    print(f"live: compared {len(rows)} tools on the docs page")

    # integration prompt
    m = re.search(r"```text[^\n]*\n(.*?)```", prompt_md, re.S)
    if not m or "Use the ProofAge MCP server and follow" not in m.group(1):
        fail("live prompt: code block not found")
        return
    published = m.group(1)
    published = published[published.index("Use the ProofAge MCP server and follow"):]
    skill = (ROOT / "skills" / "integrate-proofage" / "SKILL.md").read_text(encoding="utf-8")
    s = re.search(r"<!-- prompt:start -->\n(.*?)\n<!-- prompt:end -->", skill, re.S)
    if not s:
        fail("integrate-proofage/SKILL.md: prompt markers not found")
        return
    lines = lambda t: [re.sub(r"\s+", " ", x).strip() for x in t.strip().splitlines()]  # noqa: E731
    if lines(s.group(1)) != lines(published):
        fail("integrate-proofage: steps differ from the published integration prompt")
    else:
        print("live: skill steps match the published integration prompt")


def main():
    offline()
    if "--live" in sys.argv:
        live()
    if errors:
        print(f"{len(errors)} problem(s)")
        sys.exit(1)
    print("check: ok" + (" (live)" if "--live" in sys.argv else ""))


if __name__ == "__main__":
    main()
