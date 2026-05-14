---
layout: post
type: blog
title: "The Trivy supply chain attack had a simple root cause: a long-lived Personal"
date: 2026-04-06
permalink: /the-trivy-supply-chain-attack-had-a-simple-root/
li_id: "7446939802056163329"
resources:
  - text: "LinkedIn"
    link: "https://www.linkedin.com/feed/update/urn:li:activity:7446939802056163329/"
---

The Trivy supply chain attack had a simple root cause: a long-lived Personal Access Token (PAT). 😮‍💨 

One leaked PAT ➡️ persistent access ➡️ 75 malicious tags force-pushed ➡️ a trusted security tool weaponized for credential harvesting. 

This is a pattern we see repeatedly. Long-lived credentials create blast radii that linger for weeks after a breach. 

That's why we created Octo STS, our open source Security Token Service for GitHub. It replaces PATs with OIDC-federated tokens that are:
* Short-lived (~1 hour expiry)
* Narrowly scoped to the workflow
* Automatically revoked on completion

If you're running PATs in CI/CD, be sure to watch Patrick Smyth's quick demo of the setup + check out the full documentation on Chainguard Academy: https://lnkd.in/dXwRpq3g
