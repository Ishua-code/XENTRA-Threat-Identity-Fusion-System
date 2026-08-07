# Module 2 — EPSS Enrichment & Identity Correlation

## Objective
Enrich real OpenVAS scan CVEs with exploit-probability data (EPSS) and identity exposure scoring, then fuse both into a single unified risk score.

## 1. EPSS Enrichment
`engine/fetch_epss_real.py` reads `scanner/real-scan-results.csv` (real CVEs found by the Module 1 scan) and queries the FIRST.org EPSS API for each CVE's exploitation probability. Output: `engine/real-enriched-vulnerabilities.csv`.

Result:
| CVE | EPSS Score |
|---|---|
| CVE-2013-2566 | 0.844 |
| CVE-2015-2808 | 0.739 |
| CVE-2015-4000 | 0.999 |

## 2. Identity Exposure Scoring
`engine/score_identity.py` reads `lab-setup/identity-data.csv` (placeholder AD account data — privilege level, MFA status, last login) and computes an exposure score per identity: +0.4 for domain admin privilege, +0.4 for no MFA, +0.2 for stale login (>30 days). Output: `engine/scored-identities.csv`.

## 3. Correlation Engine
`engine/correlate.py` joins vulnerabilities to identities by host IP and computes:

`unified_risk_score = (epss_score * 0.5) + (identity_exposure_score * 0.5)`

Output: `engine/unified-risk-scores.csv`

## Result (highest risk first)
CVE-2015-4000 ranked highest (0.849) due to its near-certain exploitation probability (EPSS 0.999) combined with identity exposure.

## Known limitation
All identities in the current test data map to the same host IP (127.0.0.1), since this is single-VM lab testing. This means the correlation engine currently attributes ownership to only one identity per host. This will resolve naturally once real multi-host AD lab data is integrated in a later module.

## Screenshots
See `docs/screenshots/module2/`
