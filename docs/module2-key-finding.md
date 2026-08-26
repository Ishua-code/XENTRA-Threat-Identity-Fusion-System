# Key Finding — Module 2

Our correlation engine produced a striking, defensible result using real EPSS 
data: CVE-2021-44228 (Log4Shell), one of the most critical and widely-exploited 
vulnerabilities in recent history (EPSS score: 0.99999, near the maximum 
possible), was ranked LOWEST among five findings — because the account 
associated with the affected asset (admin_sara) has MFA enabled.

Conversely, CVE-2020-1472 (Zerologon) was ranked HIGHEST despite a marginally 
lower EPSS score, because it is tied to a service account (service_backup) 
with no MFA and 90 days of inactivity — a significantly more exposed identity.

This demonstrates the core value proposition of this project: identity context 
can and does override raw vulnerability severity/exploitability in determining 
real-world risk — a correlation no existing single-source tool (CVSS, EPSS, or 
identity/IAM platforms alone) currently performs.
