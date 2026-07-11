# XENTRA — Threat Identity Fusion System

**Fusing vulnerability exploitability and identity risk into one unified, actionable score.**

---

## Overview

XENTRA is a blue-team security project that bridges a critical gap in modern cybersecurity: vulnerability management tools tell you *what* is exploitable, while identity/IAM tools tell you *who* is risky — but nothing fuses the two into a single decision.

XENTRA correlates real-world exploit probability (via the EPSS API) with the identity risk of the account tied to each vulnerable asset (privilege level, MFA status, account staleness) to produce one **Unified Risk Score** per asset. High-risk findings are then validated using BloodHound attack-path simulation and automatically escalated into an incident ticket — turning a static vulnerability report into a full **Detect → Prioritize → Validate → Respond** pipeline.

This project directly addresses a gap named in IBM's 2026 X-Force Threat Intelligence Index, which found that 56% of nearly 40,000 vulnerabilities tracked in 2025 could be exploited without any authentication — and frames the resulting "identity vs. patching" trade-off as an unresolved industry debate. XENTRA removes that trade-off by giving security teams one combined number instead of two disconnected lists.

---

## Problem Statement

Security teams today run two separate categories of tools that never talk to each other:
- **Vulnerability management tools** (CVSS/EPSS-based scanners) tell you what is exploitable.
- **Identity/IAM tools** (conditional access, ITDR, least-privilege monitoring) tell you who is risky.

No widely available tool fuses these two data sets into a single, ranked, actionable score. XENTRA builds that missing fusion layer.

---

## Architecture

```
DETECT → PRIORITIZE → VALIDATE → RESPOND → VISUALIZE
(Scan)    (Score)      (Prove)    (Ticket)   (Dashboard)
```

| Stage | Tool | Purpose |
|---|---|---|
| Detect | OpenVAS / Nessus + Samba AD Lab | Scan for CVEs; collect identity/account data |
| Prioritize | EPSS API + Python | Correlate exploitability × identity exposure into a Unified Risk Score |
| Validate | BloodHound + SharpHound | Prove real attack paths from risky accounts |
| Respond | TheHive / Shuffle | Auto-generate incident tickets with evidence attached |
| Visualize | Grafana / Flask Dashboard | Display ranked risks, trends, and drill-down evidence |

---

## Core Formula

```
Unified Risk Score = f(EPSS_score, asset_criticality, identity_exposure_of_owner, MFA_status)
```

A medium-severity CVE owned by a non-MFA'd domain admin scores **higher** than a critical CVE on an isolated, well-guarded, low-privilege machine — a correlation neither vulnerability scanners nor identity tools perform on their own today.

---

## Tools Used

- **OpenVAS / Nessus Essentials** — vulnerability scanning
- **Samba AD Lab / Windows Server (eval)** — simulated identity environment
- **EPSS API (FIRST.org)** — real-world exploit probability
- **Python** — correlation and scoring engine
- **BloodHound + SharpHound** — attack path validation
- **TheHive / Shuffle** — SOAR / automated incident response
- **Grafana / Flask** — dashboard and visualization
- **PostgreSQL / SQLite** — data storage

---

## Repository Structure

```
/docs           → Report, diagrams, screenshots, references
/lab-setup      → VM setup notes, AD lab configuration, identity data
/scanner        → OpenVAS/Nessus configuration and scan outputs
/engine         → Python correlation engine (EPSS + identity fusion)
/validation     → BloodHound/SharpHound outputs, attack path evidence
/response       → TheHive/Shuffle automation configs
/dashboard      → Grafana/Flask dashboard code
README.md       → Project overview (this file)
```

---

## Team

| Member | Role |
|---|---|
| [Your Name] | Vulnerability scanning, correlation engine |
| [Teammate Name] | Identity/AD lab, BloodHound validation |

---

## Roadmap (5-Week Build Plan)

- **Week 1:** Lab setup — VMs, AD domain, vulnerability scanning
- **Week 2:** EPSS integration + Python correlation engine
- **Week 3:** BloodHound attack-path validation
- **Week 4:** TheHive/Shuffle automated response
- **Week 5:** Dashboard, full pipeline integration, final report

---

## References

1. Shimizu, N. & Hashimoto, M. (2025). *Vulnerability Management Chaining: An Integrated Framework for Efficient Cybersecurity Risk Prioritization.* arXiv:2506.01220
2. Janani, K. (2025). *The Human-Machine Identity Blur: A Unified Framework for Cybersecurity Risk Management in 2025.* arXiv:2503.18255
3. IBM (2026). *X-Force Threat Intelligence Index 2026.* IBM Security.
4. Additional references — see `/docs/references.md`

---

## License

This project is for academic/educational purposes.