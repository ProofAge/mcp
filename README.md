# ProofAge MCP server

The ProofAge MCP server lets an AI assistant work with your ProofAge account: integrate identity (KYC) and age verification into an app, look up a verification, send a verification link, replay a webhook, block a face, or erase a person's data on request. It is a hosted server at `https://app.proofage.net/mcp/admin` (Streamable HTTP, OAuth sign-in). There is nothing to install or run.

This repository holds the plugin for Cursor and Claude Code and the tool reference. The server runs at ProofAge; its source code is not public.

[Docs](https://docs.proofage.net/integration/mcp/overview) · [Product page](https://proofage.net/mcp-server) · support@proofage.net

## Connect

Your client opens a browser window, you sign in with your ProofAge console account and approve access. There are no API keys to paste.

| Client | How |
| --- | --- |
| Claude Code | Run `claude mcp add --transport http proofage https://app.proofage.net/mcp/admin`, then `/mcp` and choose **proofage** to sign in. |
| Claude.ai | In **Settings → Connectors**, add a custom connector with the URL `https://app.proofage.net/mcp/admin`, then connect it and sign in. |
| Cursor | [Install in Cursor](https://cursor.com/install-mcp?name=proofage&config=eyJ1cmwiOiJodHRwczovL2FwcC5wcm9vZmFnZS5uZXQvbWNwL2FkbWluIn0=), or add `{ "mcpServers": { "proofage": { "url": "https://app.proofage.net/mcp/admin" } } }` to `~/.cursor/mcp.json`. |
| VS Code | In `.vscode/mcp.json`, add `{ "servers": { "proofage": { "type": "http", "url": "https://app.proofage.net/mcp/admin" } } }`. |
| Grok | On grok.com, open **Connectors → New connector → Custom**, enter the URL, then sign in. On Business and Enterprise plans an admin may have to add the connector first. |
| Perplexity | In **Settings → Connectors**, add a custom remote connector with the URL and OAuth authentication, then sign in. Custom connectors need a Pro, Max or Enterprise plan. |
| Other clients | Point the client at the URL. The server supports OAuth discovery and dynamic client registration with public clients (no client secret). It lets these clients register: Claude, ChatGPT, Cursor, VS Code and GitHub Copilot, Grok, Perplexity, Mistral Le Chat, the Gemini app, Gemini CLI, Copilot Studio, Superhuman and Coda, Amazon Quick, n8n Cloud, and clients that sign in through a local callback such as Claude Code and Codex. Any other client can register too: after you sign in, ProofAge shows that the app is not connected yet and the client gets no access, and the request is logged. Once we add the client, the same connection works the next time you sign in. You can also write to support@proofage.net with its name. |

## Install as a plugin

Claude Code:

```text
/plugin marketplace add ProofAge/mcp
/plugin install proofage@proofage
```

Then run `/mcp` to sign in. If you added the server by hand before, remove that entry first, or it will be listed twice.

Cursor: open [ProofAge in the Cursor directory](https://cursor.directory/plugins/proofage) and choose **Add to Cursor**, then sign in from the MCP settings.

The plugin is the server address, two skills and, in Cursor, one rule. Nothing in it runs on your machine.

## Where to find it

| Directory | Listing | Updated |
| --- | --- | --- |
| Official MCP Registry | [`net.proofage/proofage`](https://registry.modelcontextprotocol.io/v0/servers?search=net.proofage/proofage) | By hand, from `server.json` |
| Cursor directory | [ProofAge](https://cursor.directory/plugins/proofage) | By hand, in the listing's edit form |
| mcp.so | [ProofAge: KYC and age verification](https://mcp.so/servers/proofage-kyc-and-age-verification) | By hand, in the submission's edit form (the overview carries the tool list) |
| Glama | [ProofAge](https://glama.ai/mcp/connectors/net.proofage/proofage) | Imported from the registry |
| Claude Code | `/plugin marketplace add ProofAge/mcp` | From this repository |

How to release a change: [RELEASING.md](RELEASING.md).

## What it can do

**Integrate.** Create a test workspace, read its keys and URLs, create verifications, set test outcomes and replay webhooks against a local handler. Then create the live workspace.

**Investigate.** Look up verifications, their decision and reason, images, webhook deliveries and statistics, with the same data as the console.

**Support.** Send a verification link, block or unblock a face, erase a person's data on request.

**Read the docs.** The assistant reads the developer documentation and the OpenAPI spec through the server, so it writes code against the real API.

## Tools

The server lists only the tools your role may use. `prepare-` and `confirm-` tools are the two steps of a destructive action.

<!-- tools:start -->
The server has 26 tools.

### Workspaces and keys

| Tool | What it does | Type | Roles |
| --- | --- | --- | --- |
| `list-workspaces` | List the available workspaces. | read | Administrator, Developer, Support specialist |
| `create-workspace` | Create a test or live workspace and return its integration guide. | write | Administrator, Developer |
| `update-workspace` | Change a workspace's settings; on a live workspace this only returns a preview. | write | Administrator, Developer |
| `confirm-live-workspace-change` | Apply a live workspace change that was previewed, after the person agrees. | write | Administrator, Developer |
| `get-integration-guide` | Get what is needed to integrate one workspace: keys, URLs, SDK and webhook signing. | read | Administrator, Developer |
| `create-secret-key` | Create an inactive secret key in a workspace, for rotating keys. | write | Administrator, Developer |
| `activate-secret-key` | Make a secret key the active one; webhooks are signed with it. | write | Administrator, Developer |
| `delete-secret-key` | Delete an inactive secret key; requests signed with it stop being accepted. | write | Administrator, Developer |

### Verifications

| Tool | What it does | Type | Roles |
| --- | --- | --- | --- |
| `list-verifications` | List verifications with filters, or count them by status. | read | Administrator, Developer, Support specialist |
| `get-verification` | Get the full detail of one verification, as shown in the admin UI. | read | Administrator, Developer, Support specialist |
| `get-verification-stats` | Get the dashboard's figures: volumes and how people's attempts ended. | read | Administrator, Developer, Support specialist |
| `create-verification` | Create a verification session and return the URL the person opens. | write | Administrator, Developer, Support specialist |
| `correct-document-fields` | Correct document fields the reader got wrong on a verification. | write | Administrator, Support specialist |
| `set-test-verification-outcome` | Set the final status of a verification in a test workspace and send its webhook. | write | Administrator, Developer |

### Webhooks

| Tool | What it does | Type | Roles |
| --- | --- | --- | --- |
| `list-webhook-deliveries` | List the webhook deliveries sent to your endpoints, newest first. | read | Administrator, Developer, Support specialist |
| `retry-webhook-delivery` | Queue a failed webhook delivery to be sent again to the same endpoint. | write | Administrator, Developer |
| `resend-webhook-delivery` | Send a fresh copy of a webhook delivery to the same endpoint. | write | Administrator, Developer |
| `get-webhook-delivery-request` | Return the exact signed request of a test delivery, to replay against localhost. | read | Administrator, Developer |

### Blocklist

| Tool | What it does | Type | Roles |
| --- | --- | --- | --- |
| `list-blocked-faces` | List blocked faces, including who blocked them and why. | read | Administrator, Developer, Support specialist |
| `prepare-block-verification-face` | Preview blocking a verification face and get a one-time challenge token. | read | Administrator, Developer, Support specialist |
| `confirm-block-verification-face` | Block a verification face with the challenge token, the phrase and a reason. | write | Administrator, Developer, Support specialist |
| `prepare-unblock-verification-face` | Preview unblocking a verification face and get a one-time challenge token. | read | Administrator, Developer, Support specialist |
| `confirm-unblock-verification-face` | Unblock a verification face with the challenge token, the phrase and a reason. | write | Administrator, Developer, Support specialist |

### Personal data

| Tool | What it does | Type | Roles |
| --- | --- | --- | --- |
| `prepare-purge-personal-data` | Preview erasing a verification's personal data and get a challenge token. | read | Administrator, Support specialist |
| `confirm-purge-personal-data` | Erase a verification's personal data, irreversibly, for a real erasure request. | write | Administrator, Support specialist |

### Docs

| Tool | What it does | Type | Roles |
| --- | --- | --- | --- |
| `read-docs-page` | Read a page of the ProofAge developer docs, or list every page. | read | Administrator, Developer, Support specialist |

Full descriptions, as your assistant reads them: [docs/TOOLS.md](docs/TOOLS.md).
<!-- tools:end -->

## Roles

The assistant acts as you, in the account you are working in in the console, and sees the tools your role allows.

| Role | Tools |
| --- | --- |
| Administrator | All tools. |
| Developer | Everything except erasing personal data and correcting document fields. |
| Support specialist | Verifications and statistics, verification links, the blocklist, the list of workspaces and webhook deliveries, correcting document fields, and erasing personal data. Not creating or changing workspaces, keys, webhook retries or test outcomes. |

Every action is recorded under your name, as it is in the console.

## Safety

- **Destructive actions take two steps.** Blocking or unblocking a face and erasing personal data first return a preview and a short-lived token. The assistant must then confirm with an exact phrase and a reason.
- **Live workspaces are protected.** Changing a live workspace or its keys only returns a preview; nothing is applied until you confirm. Live secret keys are never returned: you copy them from the console.
- **Creation is rate-limited per user**: verifications, workspaces, test outcomes and erasures.

To remove access, disconnect the server in your MCP client, or in the ProofAge console under [Connected apps](https://app.proofage.net/profile?tab=apps).

## Cost

The server is included in every account at no extra cost. Verifications it creates are billed as usual; a test workspace is free. See [pricing](https://proofage.net/pricing).

## Example prompts

> Integrate ProofAge age verification into this app. Use a test workspace, the Browser SDK on the checkout page, and a webhook handler that marks the user as verified.

> Why was verification 550e8400-… declined?

> Send a verification link for customer 8812 in the "Checkout" workspace and give me the URL.

> My webhook handler returns 401 for ProofAge webhooks. Fetch the last delivery for verification 550e8400-… and replay it against http://localhost:3000/webhooks/proofage.

The full, reusable version of the first one is the [integration prompt](https://docs.proofage.net/integration/integration-prompt). More examples are in the [docs](https://docs.proofage.net/integration/mcp/examples).

## About this repository

The tool list is generated. `scripts/sync.py` copies it from the docs repository's data into `tools.json`, `scripts/render.py` writes the table above and `docs/TOOLS.md`, and `scripts/check.py` checks everything, including a comparison with the live docs. The scripts use the Python 3 standard library only.

Issues about the server are welcome here. Licensed under the [MIT license](LICENSE), which covers the files in this repository. The ProofAge name and logo are not part of the license.
