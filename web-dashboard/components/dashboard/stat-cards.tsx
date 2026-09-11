import { Bug, Fingerprint, ShieldAlert, Siren, TrendingUp, TrendingDown } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { cn } from '@/lib/utils'

type Stat = {
  label: string
  value: string
  icon: LucideIcon
  trend: string
  trendUp: boolean
  trendGood: boolean
  accent: string
  iconWrap: string
}

const stats: Stat[] = [
  {
    label: 'Total Vulnerabilities Scanned',
    value: '30',
    icon: Bug,
    trend: '+4 today',
    trendUp: true,
    trendGood: false,
    accent: 'text-foreground',
    iconWrap: 'bg-primary/15 text-primary ring-primary/25',
  },
  {
    label: 'Identities Monitored',
    value: '30',
    icon: Fingerprint,
    trend: '+2 this week',
    trendUp: true,
    trendGood: true,
    accent: 'text-foreground',
    iconWrap: 'bg-chart-2/15 text-chart-2 ring-chart-2/25',
  },
  {
    label: 'Critical Risk Findings',
    value: '8',
    icon: ShieldAlert,
    trend: '+3 vs last scan',
    trendUp: true,
    trendGood: false,
    accent: 'text-critical',
    iconWrap: 'bg-critical/15 text-critical ring-critical/25',
  },
  {
    label: 'Active Incidents',
    value: '24',
    icon: Siren,
    trend: '-5 vs yesterday',
    trendUp: false,
    trendGood: true,
    accent: 'text-high',
    iconWrap: 'bg-high/15 text-high ring-high/25',
  },
]

export function StatCards() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.label} className="relative overflow-hidden transition-colors hover:border-border">
          <CardContent className="flex items-start justify-between gap-4">
            <div className="flex flex-col gap-3">
              <p className="text-xs font-medium text-muted-foreground">{stat.label}</p>
              <p className={cn('font-mono text-3xl font-semibold tabular-nums', stat.accent)}>
                {stat.value}
              </p>
              <div
                className={cn(
                  'flex items-center gap-1 text-xs font-medium',
                  stat.trendGood ? 'text-low' : 'text-high',
                )}
              >
                {stat.trendUp ? (
                  <TrendingUp className="size-3.5" />
                ) : (
                  <TrendingDown className="size-3.5" />
                )}
                {stat.trend}
              </div>
            </div>
            <div
              className={cn(
                'flex size-11 shrink-0 items-center justify-center rounded-xl ring-1',
                stat.iconWrap,
              )}
            >
              <stat.icon className="size-5" />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
