# One-click approval Worker

Makes the **Approve / Reject** buttons in the daily-run email actually do the thing
in one click, instead of opening the PR for you to merge by hand.

```
email button  ──GET──▶  Worker confirm page  ──POST──▶  GitHub API
                                                         approve → merge PR
                                                         reject  → close PR
                                                         deny ID → comment on PR
```

The GET → confirm-page → POST hop is deliberate: mail clients and link scanners
pre-fetch URLs, and we don't want a scanner merging your PR. One real tap on the
confirm page does it.

Both mechanisms ship together. Until the Worker is deployed and tested, the email
also carries plain GitHub deep links (Option A) that always work with no infra.

---

## Setup (once, ~10 min)

**1. GitHub token**
Create a *fine-grained* personal access token:
- Resource owner: `Mysoft-MES`
- Repository access: only `Marketing-Intelligence-Content-Decision-Brain`
- Permissions: **Contents → Read and write**, **Pull requests → Read and write**
- Copy the token (starts `github_pat_…`)

**2. Signing secret**
Generate a long random string, e.g. `python -c "import secrets;print(secrets.token_urlsafe(48))"`.
Keep it — both the Worker and the daily run need the *same* value.

**3. Deploy the Worker**
```bash
cd 00_SYSTEM/approval_worker
npm install -g wrangler        # or: npx wrangler ...
wrangler login
wrangler secret put GH_TOKEN            # paste the fine-grained PAT
wrangler secret put SIGNING_SECRET      # paste the random string
wrangler deploy
```
Note the deployed URL, e.g. `https://mysoft-approval.<your-subdomain>.workers.dev`.

**4. Tell the daily run**
Add to the environment the `marketing-brain-daily` task runs in:
```
APPROVAL_WORKER_URL=https://mysoft-approval.<your-subdomain>.workers.dev
APPROVAL_SIGNING_SECRET=<the same random string>
```

**5. Wire the email**
In the notification step, after `open_prompt_approval_pr` returns `pr_number` and
`post_ids`:
```python
from approval_worker.sign_links import approval_links
links = approval_links(pr_number, post_ids)
```
Fill the template's `{{APPROVE_ALL_URL}}`, `{{REJECT_ALL_URL}}`,
`{{DENY_URL(<POST-ID>)}}` from `links`. Leave the Option-A deep links in as a fallback.

---

## Test

```bash
# mint links for a throwaway PR
APPROVAL_WORKER_URL=https://…workers.dev APPROVAL_SIGNING_SECRET=… \
  python sign_links.py 999 FB-01 IG-02
```
Open an `approve` link against a real open PR you don't mind merging. Expect the
confirm page → tap → "Approved ✓".

Tamper test: change one character of `sig` in the URL → "Invalid signature".
Expiry: links stop working after 7 days (`TTL_SECONDS` in `sign_links.py`).

---

## Security notes

- The token lives only in Cloudflare's secret store, never in the repo or the email.
- Links are HMAC-signed and expire, so an intercepted email can't be replayed forever
  and a guessed URL won't merge anything.
- The Worker can only touch this one repo (fine-grained PAT scope).
- Merging still **publishes nothing** — it only authorises asset production, exactly
  as in `APPROVAL_UI.md`.
- To revoke: delete the token on GitHub, or `wrangler delete` the Worker. The email
  falls back to the Option-A deep links.
