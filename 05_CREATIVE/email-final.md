# email-final — approval-email template for the daily run

Owner-supplied 2026-09-04. This is the HTML template the daily run renders the **approval
email** from (spec §9B). The raw file also lives at `05_CREATIVE/email-final.html` locally;
it is kept here in Markdown form because the GitHub API sync only carries `.md` files.

## How the run uses it

1. Build the run summary (spec §9).
2. Replace every `{{TOKEN}}` below with this run's values. Repeat the prompt-card block once
   per prompt in the approval PR, the finding-card block once per material finding, and the
   file-row block once per changed file.
3. Send as the `htmlBody` of the plain-text summary email to `posinsidernow@gmail.com`
   (Gmail MCP `send_message`), subject `Marketing Brain daily run — <YYYY-MM-DD>`.
4. If no prompts were drafted, drop section 1 and say "no approval PR this run".

## Placeholder key

| Token | Value |
|---|---|
| `{{LOGO_URL}}` / `{{ILLUSTRATION_URL}}` | hosted image URLs; if none, drop the two `<img>` rows and use a text logo |
| `{{HEADLINE}}` | e.g. "Two prompts need your decision" |
| `{{INTRO_PARAGRAPH}}` | the strategist read in 2–3 sentences (from `strategy_brief_<date>.md` §1–3) |
| `{{RUN_DATE}}` | YYYY-MM-DD |
| `{{APPROVE_ALL_URL}}` / `{{REJECT_ALL_URL}}` / `{{PR_URL}}` | the approval PR URL (merge = approve, close = reject) |
| `{{PROMPT_COUNT}}` / `{{FINDING_COUNT}}` / `{{FILE_COUNT}}` | counts |
| per prompt: `{{POST_ID}}` `{{PLATFORM}}` `{{POST_DATE}}` `{{TITLE}}` `{{HOOK}}` `{{CAPTION}}` `{{SHOT_LIST}}` `{{EXCLUSIONS}}` `{{HYPOTHESIS}}` `{{FILE_PATH}}` `{{FILE_DIFF_URL}}` `{{DENY_URL}}` | |
| per finding: `{{FINDING_TITLE}}` `{{FINDING_SUMMARY}}` `{{SOURCE_NAME}}` `{{SOURCE_DATE}}` `{{SOURCE_URL}}` `{{EVIDENCE_CLASS}}` `{{CONFIDENCE}}` `{{TARGET_FILE}}` `{{ADDED_OR_UPDATED}}` `{{IMPLICATION}}` | |
| `{{COMPETITOR_PASS_RESULT}}` `{{FRESHNESS_AUDIT_RESULT}}` `{{CONFLICTS_RESULT}}` | one line each |
| per file: `{{CHANGE_TYPE}}` `{{FILE_PATH}}` `{{WHAT_CHANGED}}` `{{WHY_CHANGED}}` `{{DIFF_URL}}` | |
| `{{COMMIT_URL}}` / `{{COMMIT_SHA_SHORT}}` | the main-branch commit for this run |
| `{{PROPOSALS_SUMMARY}}` / `{{BLOCKERS_SUMMARY}}` | from `brain_update_proposals.md` and the CLAUDE.md "what is blocking quality" list |

## First render

The 2026-09-04 (fifth run) approval email for PR #2 was rendered from this template and
sent to `posinsidernow@gmail.com` — see `06_PERFORMANCE/learning_log.md` / the run summary.

## Template (HTML)

```html
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <title>Mysoft MES Marketing Brain — Daily run</title>
  <!--[if mso]>
  <noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
  <![endif]-->
</head>
<body style="margin:0; padding:0; background-color:#0f0f0f; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%;">

  <div style="display:none; max-height:0; overflow:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#0f0f0f;">
    Prompts awaiting your approval. Research and file changes for this run are inside.
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#0f0f0f; margin:0; padding:0;">
    <tr>
      <td align="center" style="padding:32px 16px;">

        <!--[if mso]>
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"><tr><td>
        <![endif]-->

        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" align="center" style="width:100%; max-width:600px; margin:0 auto; background-color:#1a1a1a; border-radius:16px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">

          <tr>
            <td style="padding:28px 32px 16px 32px;">
              <img src="{{LOGO_URL}}" alt="Mysoft MES" width="132" style="display:block; border:0; outline:none; text-decoration:none; height:auto;" />
            </td>
          </tr>

          <tr>
            <td style="padding:0 32px;">
              <img src="{{ILLUSTRATION_URL}}" alt="" width="536" style="display:block; width:100%; max-width:536px; height:auto; border:0; outline:none; text-decoration:none; border-radius:12px;" />
            </td>
          </tr>

          <tr>
            <td style="padding:28px 32px 0 32px;">
              <h1 style="margin:0; color:#f5f5f0; font-family:Georgia,'Times New Roman',Times,serif; font-size:30px; line-height:1.25; font-weight:400;">{{HEADLINE}}</h1>
            </td>
          </tr>

          <tr>
            <td style="padding:16px 32px 0 32px;">
              <p style="margin:0; color:#b8b8b3; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:15px; line-height:1.6;">{{INTRO_PARAGRAPH}}</p>
              <p style="margin:12px 0 0 0; color:#8a8a85; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:1.6;">
                Run date {{RUN_DATE}} &nbsp;&middot;&nbsp; Research below is already pushed to <span style="font-family:Consolas,'Courier New',monospace;">main</span>. Only the prompts need your decision. Merging the PR authorises assets to be produced &mdash; it publishes nothing.
              </p>
            </td>
          </tr>

          <tr>
            <td style="padding:24px 32px 0 32px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="border-radius:10px; background-color:#d97706;">
                    <a href="{{APPROVE_ALL_URL}}" target="_blank" style="display:inline-block; padding:14px 26px; color:#1a1a1a; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:15px; font-weight:bold; text-decoration:none; border-radius:10px;">Approve all &amp; push &rarr;</a>
                  </td>
                  <td style="width:12px; font-size:0; line-height:0;">&nbsp;</td>
                  <td style="border-radius:10px; border:1px solid #5a3a3a; background-color:#241c1c;">
                    <a href="{{REJECT_ALL_URL}}" target="_blank" style="display:inline-block; padding:13px 24px; color:#e0968a; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:15px; font-weight:bold; text-decoration:none; border-radius:10px;">Reject all</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding:12px 32px 0 32px;">
              <p style="margin:0; color:#8a8a85; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:1.7;">
                One click &rarr; a confirm page &rarr; done. <strong style="color:#b8b8b3;">Approve all</strong> merges the PR (authorises assets, publishes nothing). <strong style="color:#b8b8b3;">Reject all</strong> closes it and the prompts are regenerated. To reject just one, use its <strong style="color:#b8b8b3;">Reject this prompt</strong> link below.
              </p>
              <p style="margin:10px 0 0 0; color:#6a6a65; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:12px; line-height:1.7;">
                Buttons not working? <a href="{{PR_URL}}" target="_blank" style="color:#e0a56d; text-decoration:none;">Open the PR on GitHub</a> &mdash; <em>Merge</em> to approve all, comment <span style="font-family:Consolas,'Courier New',monospace;">deny &lt;POST-ID&gt;: &lt;reason&gt;</span> then merge to reject some, <em>Close</em> to reject all.
              </p>
            </td>
          </tr>

          <tr>
            <td style="padding:28px 32px 0 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid #333330; font-size:0; line-height:0; height:1px;">&nbsp;</td></tr></table>
            </td>
          </tr>

          <tr>
            <td style="padding:18px 32px 0 32px;">
              <h2 style="margin:0; color:#f5f5f0; font-family:Georgia,'Times New Roman',Times,serif; font-size:20px; font-weight:400;">1 &nbsp;Prompts awaiting your approval</h2>
              <p style="margin:6px 0 0 0; color:#8a8a85; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:1.6;">{{PROMPT_COUNT}} in PR &nbsp;&middot;&nbsp; <a href="{{PR_URL}}" target="_blank" style="color:#e0a56d; text-decoration:none;">open the PR</a></p>
            </td>
          </tr>

          <tr>
            <td style="padding:14px 32px 0 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#212121; border-radius:12px;">
                <tr>
                  <td style="padding:18px 20px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
                    <p style="margin:0; color:#f5f5f0; font-size:15px; font-weight:bold; line-height:1.4;">{{POST_ID}} &nbsp;&middot;&nbsp; <span style="color:#b8b8b3; font-weight:normal;">{{PLATFORM}}</span> &nbsp;&middot;&nbsp; <span style="color:#8a8a85; font-weight:normal;">{{POST_DATE}}</span></p>
                    <p style="margin:8px 0 0 0; color:#d8d8d3; font-size:14px; line-height:1.55;"><strong style="color:#f5f5f0;">Title:</strong> {{TITLE}}</p>
                    <p style="margin:8px 0 0 0; color:#b8b8b3; font-size:13px; line-height:1.6;"><strong style="color:#d8d8d3;">Hook / angle:</strong> {{HOOK}}</p>
                    <p style="margin:8px 0 0 0; color:#b8b8b3; font-size:13px; line-height:1.6;"><strong style="color:#d8d8d3;">Caption:</strong> {{CAPTION}}</p>
                    <p style="margin:8px 0 0 0; color:#b8b8b3; font-size:13px; line-height:1.6;"><strong style="color:#d8d8d3;">Shot list:</strong> {{SHOT_LIST}}</p>
                    <p style="margin:8px 0 0 0; color:#b8b8b3; font-size:13px; line-height:1.6;"><strong style="color:#d8d8d3;">Must NOT appear:</strong> {{EXCLUSIONS}}</p>
                    <p style="margin:8px 0 0 0; color:#b8b8b3; font-size:13px; line-height:1.6;"><strong style="color:#d8d8d3;">Hypothesis:</strong> {{HYPOTHESIS}}</p>
                    <p style="margin:10px 0 0 0; font-size:13px; line-height:1.6;">
                      <a href="{{FILE_DIFF_URL}}" target="_blank" style="color:#e0a56d; text-decoration:none;">View file diff &rarr;</a>
                      <span style="color:#5a5a55;"> &nbsp;|&nbsp; </span><span style="color:#8a8a85;">{{FILE_PATH}}</span>
                    </p>
                    <p style="margin:12px 0 0 0; font-size:13px; line-height:1.6;">
                      <a href="{{DENY_URL}}" target="_blank" style="display:inline-block; padding:8px 16px; border:1px solid #5a3a3a; border-radius:8px; background-color:#241c1c; color:#e0968a; font-weight:bold; text-decoration:none;">Reject this prompt</a>
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:28px 32px 0 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid #333330; font-size:0; line-height:0; height:1px;">&nbsp;</td></tr></table>
            </td>
          </tr>

          <tr>
            <td style="padding:18px 32px 0 32px;">
              <h2 style="margin:0; color:#f5f5f0; font-family:Georgia,'Times New Roman',Times,serif; font-size:20px; font-weight:400;">2 &nbsp;Research this run</h2>
              <p style="margin:6px 0 0 0; color:#8a8a85; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:1.6;">{{FINDING_COUNT}} findings that changed the Brain's understanding. If a sweep found nothing, that is stated &mdash; a quiet day is a valid outcome.</p>
            </td>
          </tr>

          <tr>
            <td style="padding:14px 32px 0 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#212121; border-radius:12px;">
                <tr>
                  <td style="padding:18px 20px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
                    <p style="margin:0; color:#f5f5f0; font-size:15px; font-weight:bold; line-height:1.4;">{{FINDING_TITLE}}</p>
                    <p style="margin:8px 0 0 0; color:#d8d8d3; font-size:13px; line-height:1.6;">{{FINDING_SUMMARY}}</p>
                    <p style="margin:10px 0 0 0; color:#b8b8b3; font-size:12px; line-height:1.7;">
                      <strong style="color:#d8d8d3;">Source:</strong> {{SOURCE_NAME}}, {{SOURCE_DATE}} &nbsp;&middot;&nbsp; <a href="{{SOURCE_URL}}" target="_blank" style="color:#e0a56d; text-decoration:none;">link</a><br />
                      <strong style="color:#d8d8d3;">Evidence class:</strong> {{EVIDENCE_CLASS}} &nbsp;&middot;&nbsp; <strong style="color:#d8d8d3;">Confidence:</strong> {{CONFIDENCE}}<br />
                      <strong style="color:#d8d8d3;">Routed to:</strong> <span style="color:#8a8a85;">{{TARGET_FILE}}</span> &nbsp;&middot;&nbsp; <strong style="color:#d8d8d3;">Action:</strong> {{ADDED_OR_UPDATED}}
                    </p>
                    <p style="margin:8px 0 0 0; color:#b8b8b3; font-size:12px; line-height:1.6;"><strong style="color:#d8d8d3;">So what:</strong> {{IMPLICATION}}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:16px 32px 0 32px;">
              <p style="margin:0; color:#b8b8b3; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:1.7;">
                <strong style="color:#d8d8d3;">Competitor pass:</strong> {{COMPETITOR_PASS_RESULT}}<br />
                <strong style="color:#d8d8d3;">Freshness audit:</strong> {{FRESHNESS_AUDIT_RESULT}}<br />
                <strong style="color:#d8d8d3;">Knowledge conflicts:</strong> {{CONFLICTS_RESULT}}
              </p>
            </td>
          </tr>

          <tr>
            <td style="padding:28px 32px 0 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid #333330; font-size:0; line-height:0; height:1px;">&nbsp;</td></tr></table>
            </td>
          </tr>

          <tr>
            <td style="padding:18px 32px 0 32px;">
              <h2 style="margin:0; color:#f5f5f0; font-family:Georgia,'Times New Roman',Times,serif; font-size:20px; font-weight:400;">3 &nbsp;Files added &amp; changed</h2>
              <p style="margin:6px 0 0 0; color:#8a8a85; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:1.6;">
                {{FILE_COUNT}} files in commit <a href="{{COMMIT_URL}}" target="_blank" style="color:#e0a56d; text-decoration:none;">{{COMMIT_SHA_SHORT}}</a> on <span style="font-family:Consolas,'Courier New',monospace;">main</span>. Deletions are never automated &mdash; they stay a human action on GitHub.
              </p>
            </td>
          </tr>

          <tr>
            <td style="padding:14px 32px 0 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#212121; border-radius:12px;">
                <tr>
                  <td style="padding:16px 20px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
                    <p style="margin:0; font-size:13px; line-height:1.5;">
                      <span style="display:inline-block; padding:2px 8px; border-radius:6px; background-color:#2f3b2f; color:#8fce8f; font-size:11px; font-weight:bold; letter-spacing:0.04em;">{{CHANGE_TYPE}}</span>
                      &nbsp; <span style="font-family:Consolas,'Courier New',monospace; color:#d8d8d3;">{{FILE_PATH}}</span>
                    </p>
                    <p style="margin:8px 0 0 0; color:#b8b8b3; font-size:13px; line-height:1.6;">{{WHAT_CHANGED}}</p>
                    <p style="margin:6px 0 0 0; color:#8a8a85; font-size:12px; line-height:1.6;"><strong style="color:#b8b8b3;">Why:</strong> {{WHY_CHANGED}} &nbsp;&middot;&nbsp; <a href="{{DIFF_URL}}" target="_blank" style="color:#e0a56d; text-decoration:none;">diff</a></p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:28px 32px 0 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid #333330; font-size:0; line-height:0; height:1px;">&nbsp;</td></tr></table>
            </td>
          </tr>

          <tr>
            <td style="padding:18px 32px 0 32px;">
              <h2 style="margin:0; color:#f5f5f0; font-family:Georgia,'Times New Roman',Times,serif; font-size:20px; font-weight:400;">4 &nbsp;Proposals &amp; blockers</h2>
              <p style="margin:8px 0 0 0; color:#b8b8b3; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:1.7;">
                <strong style="color:#d8d8d3;">New brain-update proposals:</strong> {{PROPOSALS_SUMMARY}}<br />
                <span style="color:#8a8a85;">(00_SYSTEM / 01_BUSINESS are read-only to the run &mdash; these need your review in <span style="font-family:Consolas,'Courier New',monospace;">08_DECISIONS/brain_update_proposals.md</span>.)</span>
              </p>
              <p style="margin:10px 0 0 0; color:#b8b8b3; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:1.7;">
                <strong style="color:#d8d8d3;">Still blocking quality:</strong> {{BLOCKERS_SUMMARY}}
              </p>
            </td>
          </tr>

          <tr>
            <td style="padding:28px 32px 32px 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid #333330; font-size:0; line-height:0; height:1px;">&nbsp;</td></tr></table>
              <p style="margin:16px 0 0 0; color:#6a6a65; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:12px; line-height:1.6;">
                Mysoft MES Marketing Intelligence &amp; Content Decision Brain &nbsp;&middot;&nbsp; automated daily run {{RUN_DATE}}.<br />
                An AI recommendation is not a decision until a human approves it. Publishing to any social platform still needs a separate explicit step.
              </p>
            </td>
          </tr>

        </table>

        <!--[if mso]>
        </td></tr></table>
        <![endif]-->

      </td>
    </tr>
  </table>

</body>
</html>
```
