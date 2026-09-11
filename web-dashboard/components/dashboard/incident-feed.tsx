import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { SeverityBadge } from '@/components/dashboard/severity-badge'
import { incidents } from '@/lib/data'

function timeAgo(minutes: number) {
  if (minutes < 60) return `${minutes} min ago`
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return m === 0 ? `${h}h ago` : `${h}h ${m}m ago`
}

export function IncidentFeed() {
  return (
    <Card className="flex h-full flex-col">
      <CardHeader>
        <div className="flex items-center justify-between gap-2">
          <div>
            <CardTitle>Incident Feed</CardTitle>
            <CardDescription>Auto-generated response tickets</CardDescription>
          </div>
          <span className="flex items-center gap-1.5 rounded-full border border-high/30 bg-high/10 px-2.5 py-0.5 text-xs font-medium text-high">
            <span className="size-1.5 animate-pulse rounded-full bg-high" />
            Live
          </span>
        </div>
      </CardHeader>
      <CardContent className="flex-1">
        <ScrollArea className="h-[300px] pr-3">
          <div className="flex flex-col gap-2">
            {incidents.map((inc) => (
              <div
                key={inc.id}
                className="flex flex-col gap-2 rounded-lg border border-border/60 bg-secondary/25 p-3 transition-colors hover:border-border"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-xs font-medium text-primary">{inc.id}</span>
                  <SeverityBadge severity={inc.severity} />
                </div>
                <p className="text-sm text-foreground">{inc.title}</p>
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] text-muted-foreground">{timeAgo(inc.minutesAgo)}</span>
                  <Button size="sm" variant="ghost" className="h-7 px-2 text-xs">
                    View
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
