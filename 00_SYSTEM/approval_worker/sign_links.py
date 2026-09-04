"""
Build signed one-click approval links for the daily-run email.

The daily run calls approval_links(pr_number, post_ids) and drops the returned
URLs into the email template's Option-B tokens. The Worker verifies the same
HMAC, so only links minted here work.

Env:
  APPROVAL_WORKER_URL   e.g. https://mysoft-approval.<subdomain>.workers.dev
  APPROVAL_SIGNING_SECRET   same value as the Worker's SIGNING_SECRET
"""

import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

TTL_SECONDS = 60 * 60 * 24 * 7  # links valid for 7 days


def _sign(payload: str, secret: str) -> str:
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def _link(base: str, secret: str, pr: int, action: str, post_id: str = "") -> str:
    exp = int(time.time()) + TTL_SECONDS
    payload = f"{pr}.{action}.{post_id}.{exp}"
    params = {"pr": pr, "action": action, "exp": exp, "sig": _sign(payload, secret)}
    if post_id:
        params["id"] = post_id
    return f"{base.rstrip('/')}/act?{urlencode(params)}"


def approval_links(pr_number: int, post_ids: list[str]) -> dict:
    base = os.environ["APPROVAL_WORKER_URL"]
    secret = os.environ["APPROVAL_SIGNING_SECRET"]
    return {
        "approve_all_url": _link(base, secret, pr_number, "approve"),
        "reject_all_url": _link(base, secret, pr_number, "reject"),
        "deny_urls": {pid: _link(base, secret, pr_number, "deny", pid) for pid in post_ids},
    }


if __name__ == "__main__":
    import json
    import sys

    pr = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ids = sys.argv[2:] or ["FB-01", "IG-02"]
    print(json.dumps(approval_links(pr, ids), indent=2))
