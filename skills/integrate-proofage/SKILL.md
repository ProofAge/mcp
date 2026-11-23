---
name: integrate-proofage
description: Integrate ProofAge identity (KYC) or age verification into the current project through the ProofAge MCP server. Use when the user asks to add age verification, an 18+ check, identity verification, an ID document check, KYC or ProofAge to an app, or to test or debug a ProofAge integration and its webhooks.
---

# Integrate ProofAge

## Before you start

Find out three things from the user. If the request does not state them, ask. Do not guess.

- What they want: for example an age check (18+) before checkout, or identity verification (KYC) for new sellers.
- Where the person starts it: for example the "Verify age" button on /checkout.
- What a result should change: for example set a field on approval, or block the order on decline.

If the `proofage` MCP server is not connected, tell the user to sign in: `/mcp` in Claude Code, MCP settings in Cursor.

## Steps

In the steps, "I", "me" and "our" mean the user.

<!-- prompt:start -->
Use the ProofAge MCP server and follow its onboarding order:
1. Create a TEST workspace with the right check (create-workspace, mode "test").
2. Call get-integration-guide for that workspace, and read the docs it links with read-docs-page
   (quick start, server SDKs, browser SDK, webhooks, testing).
3. Write the integration:
   - install the official ProofAge server SDK for this project's backend (@proofage/node for
     Node.js or Deno; proofage for Python; proofage/php-sdk for PHP; proofage/laravel-client
     for Laravel 12+) and use it for every API call and for webhook verification. Do not write
     your own request signing unless the backend's language has no SDK;
   - the backend creates the verification through the SDK, with external_id = our user ID
     and callback_url = a page of ours;
   - the frontend opens it with the Browser SDK (or redirects to its url);
   - a webhook endpoint verifies the signature and timestamp with the SDK's verifier, handles
     approved, declined, resubmission_requested, review, abandoned and expired, is idempotent
     on the delivery ID, and updates our data;
   - the page the person returns to never assumes the outcome.
   Keep the keys in environment variables; never commit them.
4. Create a verification (create-verification) and give me its URL: I will complete it with my camera.
5. When it is in review, set the outcome with set-test-verification-outcome and confirm our webhook
   handler processed it (list-webhook-deliveries; replay with get-webhook-delivery-request if our
   endpoint is local).
6. Show me the diff.
7. When I say the test run is done, create the LIVE workspace (create-workspace, mode "live") with
   the same check and settings as the test one and our production webhook and redirect URLs. Give
   me its public key and secret_console_url, and tell me what to set in production: I will copy
   the live secret key from the console myself.
<!-- prompt:end -->

## Before going live

Review what you wrote against the go-live checklist at https://docs.proofage.net/integration/go-live. You can create the live workspace in step 7, or the user can create it in the console. Live secret keys never pass through the MCP server: the user copies the live secret key from the console and swaps it into production.
