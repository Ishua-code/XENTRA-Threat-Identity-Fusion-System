import { ShieldCheck, ShieldX, Crown } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { topIdentities, severityFromScore, type Identity } from '@/lib/data'
import { cn } from '@/lib/utils'

const privilegeStyle: Record<Identity['privilege'], string> = {
  'Domain Admin': 'bg-critical/15 text-critical border-critical/30',
  'Server Admin': 'bg-high/15 text-high border-high/30',
  Privileged: 'bg-medium/15 text-medium border-medium/30',
  Standard: 'bg-secondary text-muted-foreground border-border',
}

const barColor: Record<string, string> = {
  critical: 'bg-critical',
  high: 'bg-high',
  medium: 'bg-medium',
  low: 'bg-low',
}

export function IdentityRiskPanel() {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Top Risk Identities</CardTitle>
        <CardDescription>Highest exposure to privilege abuse</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-2">
        {topIdentities.map((id) => {
          const sev = severityFromScore(id.risk)
          return (
            <div
              key={id.username}
              className="flex flex-col gap-2 rounded-lg border border-border/60 bg-secondary/25 p-3 transition-colors hover:border-border"
            >
              <div className="flex items-center justify-between gap-2">
                <div className="flex min-w-0 items-center gap-2">
                  {id.privilege === 'Domain Admin' && (
                    <Crown className="size-3.5 shrink-0 text-critical" />
                  )}
                  <span className="truncate font-mono text-sm font-medium text-foreground">
                    {id.username}
                  </span>
                </div>
                {id.mfa ? (
                  <span className="flex items-center gap-1 text-[11px] font-medium text-low">
                    <ShieldCheck className="size-3.5" /> MFA
                  </span>
                ) : (
                  <span className="flex items-center gap-1 text-[11px] font-medium text-critical">
                    <ShieldX className="size-3.5" /> No MFA
                  </span>
                )}
              </div>

              <div className="flex items-center gap-2">
                <span
                  className={cn(
                    'rounded-full border px-2 py-0.5 text-[10px] font-medium',
                    privilegeStyle[id.privilege],
                  )}
                >
                  {id.privilege}
                </span>
                <span className="text-[11px] text-muted-foreground">
                  {id.hops === 0 ? 'is Domain Admin' : `${id.hops} hop${id.hops > 1 ? 's' : ''} to DA`}
                </span>
              </div>

              <div className="flex items-center gap-2">
                <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
                  <div
                    className={cn('h-full rounded-full', barColor[sev])}
                    style={{ width: `${Math.round(id.risk * 100)}%` }}
                  />
                </div>
                <span className="w-9 shrink-0 text-right font-mono text-xs font-semibold tabular-nums text-foreground">
                  {id.risk.toFixed(2)}
                </span>
              </div>
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}
