import raw from './source/dashboard.json'

export type Severity = 'critical' | 'high' | 'medium' | 'low'

export function severityFromScore(score: number): Severity {
  if (score >= 0.7) return 'critical'
  if (score >= 0.5) return 'high'
  if (score >= 0.3) return 'medium'
  return 'low'
}

type RawFinding = {
  cve_id: string
  host: string
  owner: string
  epss_score: string
  identity_exposure_score: string
  graph_proximity_score: string
  betweenness_centrality: string
  unified_risk_score: string
}

type RawAttackPath = {
  account: string
  path: string[]
  hops: number
}

type RawData = {
  generated_at: string
  stats: {
    total_vulnerabilities: number
    identities_monitored: number
    critical_findings: number
    active_incidents: number
  }
  findings: RawFinding[]
  attack_paths: RawAttackPath[]
}

const data = raw as RawData

export type RiskFinding = {
  cve: string
  score: number
}

export const topRiskFindings: RiskFinding[] = [...data.findings]
  .sort((a, b) => Number(b.unified_risk_score) - Number(a.unified_risk_score))
  .slice(0, 10)
  .map((f) => ({ cve: f.cve_id, score: Number(f.unified_risk_score) }))

export type VulnStatus = 'Critical' | 'High' | 'Medium'

export type Vulnerability = {
  cve: string
  name: string
  host: string
  owner: string
  epss: number
  identityRisk: number
  unified: number
  status: VulnStatus
  description: string
  vector: string
}

function statusFromScore(score: number): VulnStatus {
  if (score >= 0.7) return 'Critical'
  if (score >= 0.5) return 'High'
  return 'Medium'
}

export const vulnerabilities: Vulnerability[] = data.findings.map((f) => {
  const unified = Number(f.unified_risk_score)
  return {
    cve: f.cve_id,
    name: f.cve_id,
    host: f.host,
    owner: f.owner,
    epss: Number(f.epss_score),
    identityRisk: Number(f.identity_exposure_score),
    unified,
    status: statusFromScore(unified),
    description: `Finding for ${f.cve_id} on ${f.host}, owned by ${f.owner}.`,
    vector: 'N/A',
  }
})

export type Identity = {
  username: string
  privilege: 'Domain Admin' | 'Server Admin' | 'Privileged' | 'Standard'
  mfa: boolean
  hops: number
  risk: number
}

const uniqueOwners = Array.from(new Set(data.findings.map((f) => f.owner)))

export const topIdentities: Identity[] = uniqueOwners
  .map((owner) => {
    const findingsForOwner = data.findings.filter((f) => f.owner === owner)
    const risk = Math.max(...findingsForOwner.map((f) => Number(f.identity_exposure_score)))
    const pathMatch = data.attack_paths.find((p) => p.account === owner)
    return {
      username: owner,
      privilege: 'Standard' as const,
      mfa: false,
      hops: pathMatch ? pathMatch.hops : 0,
      risk,
    }
  })
  .sort((a, b) => b.risk - a.risk)
  .slice(0, 5)

export type Incident = {
  id: string
  title: string
  severity: Severity
  minutesAgo: number
}

export const incidents: Incident[] = data.findings.slice(0, 6).map((f, i) => ({
  id: `INC-${4821 - i}`,
  title: `${f.cve_id} exposure detected on ${f.host} (${f.owner})`,
  severity: severityFromScore(Number(f.unified_risk_score)),
  minutesAgo: (i + 1) * 12,
}))

export type GraphNode = {
  id: string
  label: string
  kind: 'entry' | 'pivot' | 'server' | 'target'
  x: number
  y: number
}

export type GraphEdge = { from: string; to: string }

const firstPath = data.attack_paths[0]

export const attackPath: { nodes: GraphNode[]; edges: GraphEdge[] } = firstPath
  ? {
      nodes: [
        { id: firstPath.path[0], label: firstPath.path[0], kind: 'entry', x: 14, y: 22 },
        { id: firstPath.path[1], label: firstPath.path[1], kind: 'server', x: 55, y: 45 },
        { id: firstPath.path[2], label: firstPath.path[2], kind: 'target', x: 90, y: 70 },
      ],
      edges: [
        { from: firstPath.path[0], to: firstPath.path[1] },
        { from: firstPath.path[1], to: firstPath.path[2] },
      ],
    }
  : { nodes: [], edges: [] }

export const stats = data.stats
export const generatedAt = data.generated_at
