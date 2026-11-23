---
name: proofage-support
description: Look up ProofAge verifications and handle support requests through the ProofAge MCP server. Use when the user asks why a verification was declined, for approval figures, to send a verification link, to check or replay webhook deliveries, to correct a misread document field, to block or unblock a face, or to erase a person's data.
---

# ProofAge support

Use the `proofage` MCP server. If it is not connected, tell the user to sign in: `/mcp` in Claude Code, MCP settings in Cursor.

## Which tool answers which request

| Request | Tool |
| --- | --- |
| Why was a verification declined? | `get-verification`. Read `decision.final_reason`, with `reason_label`, `severity` and `scope`. Do not read the reason from `result_summary`: it can be stale. |
| Approval rate or other dashboard figures | `get-verification-stats`. It gives the same numbers as the console's dashboard, for live workspaces. |
| Did someone verify more than once? Find verifications for a user | `list-verifications`, filtered by `external_id`. |
| Send a verification link | `create-verification` in the right workspace (see `list-workspaces`). It returns the URL to send. |
| A webhook did not arrive or the handler fails | `list-webhook-deliveries`. To send a failed delivery again, `retry-webhook-delivery`. In a test workspace, `get-webhook-delivery-request` returns the exact signed request to replay against a local handler. The last two need the Administrator or Developer role. |
| A document field was read wrongly | `correct-document-fields`. The status stays the same and no check is re-run. Administrator or Support specialist role. |

## Blocking, unblocking and erasing

Blocking a face, unblocking a face and erasing a person's data take two steps each.

1. Call the `prepare-` tool. It changes nothing and returns a preview and a short-lived token.
2. Show the preview to the user and wait for their agreement.
3. Call the matching `confirm-` tool with the token, the exact confirmation phrase and a reason.

Erasing personal data cannot be undone. Use it only for a real request to erase, never to tidy up.

## If a tool is missing

The server lists only the tools the user's role may use. If a tool you need is not listed, the user's role does not allow it. Say so and do not look for a way around it.
