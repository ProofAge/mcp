# Releasing

Every place that lists the ProofAge MCP server, and what to do there after a change in this repository.

## When to release

- The tool list changed: run `python3 scripts/sync.py` and `python3 scripts/render.py`.
- The plugin changed: `.mcp.json`, a skill, the rule, a description or the keywords.
- The registry entry changed: description, website, icons or the server address.

A change to the server alone (a fix, a new client allowed to sign in) needs no release unless its tools or its address changed.

## Steps

1. Bump `version` to the same value in `server.json`, `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`, and add a `CHANGELOG.md` entry.
2. Run `python3 scripts/check.py --live`. It must print `check: ok`.
3. Commit, push and tag `vX.Y.Z`.
4. **Official MCP Registry.** From this checkout: `mcp-publisher login dns --domain proofage.net --private-key <key>`, then `mcp-publisher publish`. The key is held by the ProofAge owner, not in this repository. `server.json` `description` is at most 100 characters. Check that `https://registry.modelcontextprotocol.io/v0/servers?search=net.proofage/proofage` shows the new version as latest.
5. **Cursor directory.** Sign in at cursor.directory with the owner's account, open [the listing](https://cursor.directory/plugins/proofage), choose ⋯ → Edit → Re-scan, check the detected components (1 rule, 1 MCP server, 2 skills) and the logo, and save. The listing is hidden again until the security scan passes; check it is public afterwards. Cursor does not re-read the repository by itself.
6. **mcp.so.** The overview is this README, re-read on mcp.so's own schedule. Name, category, tags and logo are edited by hand under Settings → My submissions.
7. **Glama** imports from the registry, and **Claude Code** users get the plugin from this repository: nothing to do.

## Directories not listed yet

- PulseMCP: new submissions were paused in November 2026.
- Smithery: closed to new submissions since October 2026.
