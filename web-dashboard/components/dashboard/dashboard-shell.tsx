'use client'

import { useState, useEffect } from 'react'
import { AppSidebar } from '@/components/dashboard/app-sidebar'
import { TopBar } from '@/components/dashboard/top-bar'
import { StatCards } from '@/components/dashboard/stat-cards'
import { RiskScoreChart } from '@/components/dashboard/risk-score-chart'
import { AttackPathGraph } from '@/components/dashboard/attack-path-graph'
import { VulnerabilityTable } from '@/components/dashboard/vulnerability-table'
import { IdentityRiskPanel } from '@/components/dashboard/identity-risk-panel'
import { IncidentFeed } from '@/components/dashboard/incident-feed'
import { DashboardSkeleton } from '@/components/dashboard/dashboard-skeletons'

const viewCopy: Record<string, { title: string; desc: string }> = {
  Overview: {
    title: 'Security Overview',
    desc: 'Unified vulnerability, identity, and attack-path risk across your estate.',
  },
  Vulnerabilities: {
    title: 'Vulnerabilities',
    desc: 'All fused vulnerability findings across monitored hosts.',
  },
  Identities: {
    title: 'Identities',
    desc: 'Identity exposure and privilege risk across monitored accounts.',
  },
  'Attack Paths': {
    title: 'Attack Paths',
    desc: 'Shortest paths from compromised accounts to Domain Admin.',
  },
  Incidents: {
    title: 'Incidents',
    desc: 'Recent incidents generated from fused risk findings.',
  },
  Settings: {
    title: 'Settings',
    desc: 'Fusion engine configuration.',
  },
}

export function DashboardShell() {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('Overview')

  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 900)
    return () => clearTimeout(t)
  }, [])

  const copy = viewCopy[view] ?? viewCopy.Overview

  return (
    <div className="flex min-h-screen bg-background">
      <AppSidebar
        collapsed={collapsed}
        onToggle={() => setCollapsed((c) => !c)}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
        active={view}
        onSelect={setView}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar onToggleSidebar={() => setMobileOpen((o) => !o)} />

        <main className="flex-1 overflow-x-hidden p-4 md:p-6">
          <div className="mx-auto flex max-w-[1600px] flex-col gap-4">
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-semibold text-foreground">{copy.title}</h1>
                <span className="rounded-full border border-primary/30 bg-primary/10 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-primary">
                  Fusion Engine v3.2
                </span>
              </div>
              <p className="text-sm text-muted-foreground">{copy.desc}</p>
            </div>

            {loading ? (
              <DashboardSkeleton />
            ) : view === 'Overview' ? (
              <>
                <StatCards />

                <div className="grid grid-cols-1 gap-4 xl:grid-cols-3">
                  <div className="xl:col-span-2">
                    <RiskScoreChart />
                  </div>
                  <div>
                    <AttackPathGraph onViewFullGraph={() => setView('Attack Paths')} />
                  </div>
                </div>

                <VulnerabilityTable />

                <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                  <IdentityRiskPanel />
                  <IncidentFeed />
                </div>
              </>
            ) : view === 'Vulnerabilities' ? (
              <VulnerabilityTable />
            ) : view === 'Identities' ? (
              <IdentityRiskPanel />
            ) : view === 'Attack Paths' ? (
              <AttackPathGraph onViewFullGraph={() => setView('Attack Paths')} expanded />
            ) : view === 'Incidents' ? (
              <IncidentFeed />
            ) : (
              <div className="rounded-lg border border-border/60 bg-card p-6 text-sm text-muted-foreground">
                Settings panel not yet implemented.
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
