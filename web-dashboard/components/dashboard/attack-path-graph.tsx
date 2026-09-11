import { ArrowRight, Crosshair, Server, User, GitBranch } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { attackPath, type GraphNode } from '@/lib/data'
import { cn } from '@/lib/utils'

const nodeStyle: Record<GraphNode['kind'], { ring: string; icon: LucideIcon; color: string }> = {
  entry: { ring: 'border-primary/50 bg-primary/15 text-primary', icon: User, color: 'var(--primary)' },
  pivot: { ring: 'border-high/50 bg-high/15 text-high', icon: GitBranch, color: 'var(--high)' },
  server: { ring: 'border-chart-2/50 bg-chart-2/15 text-chart-2', icon: Server, color: 'var(--chart-2)' },
  target: { ring: 'border-critical/60 bg-critical/15 text-critical', icon: Crosshair, color: 'var(--critical)' },
}

export function AttackPathGraph({
  onViewFullGraph,
  expanded = false,
}: {
  onViewFullGraph?: () => void
  expanded?: boolean
}) {
  const { nodes, edges } = attackPath
  const nodeById = (id: string) => nodes.find((n) => n.id === id)!
  const hops = Math.max(edges.length, 0)

  return (
    <Card className="flex h-full flex-col">
      <CardHeader>
        <CardTitle>Attack Path Preview</CardTitle>
        <CardDescription>Shortest route to Domain Admin</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-1 flex-col gap-4">
        <div
          className={cn(
            'relative flex-1 overflow-hidden rounded-lg border border-border/60 bg-[radial-gradient(circle_at_1px_1px,var(--border)_1px,transparent_0)] [background-size:16px_16px]',
            expanded ? 'min-h-[520px]' : 'min-h-[240px]',
          )}
        >
          <svg
            className="absolute inset-0 size-full"
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
            aria-hidden
          >
            <defs>
              <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="var(--muted-foreground)" />
              </marker>
            </defs>
            {edges.map((e) => {
              const from = nodeById(e.from)
              const to = nodeById(e.to)
              return (
                <line
                  key={`${e.from}-${e.to}`}
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                  stroke="var(--muted-foreground)"
                  strokeWidth={1.2}
                  strokeDasharray="4 3"
                  vectorEffect="non-scaling-stroke"
                  markerEnd="url(#arrow)"
                  opacity={0.55}
                />
              )
            })}
          </svg>

          {nodes.map((node) => {
            const style = nodeStyle[node.kind]
            const Icon = style.icon
            return (
              <div
                key={node.id}
                className="absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center gap-1.5"
                style={{ left: `${node.x}%`, top: `${node.y}%` }}
              >
                <div
                  className={cn(
                    'flex size-11 items-center justify-center rounded-full border shadow-lg transition-transform hover:scale-110',
                    style.ring,
                  )}
                  style={
                    node.kind === 'target'
                      ? { boxShadow: `0 0 16px ${style.color}55` }
                      : undefined
                  }
                >
                  <Icon className="size-5" />
                </div>
                <span className="whitespace-nowrap rounded bg-background/80 px-1.5 py-0.5 font-mono text-[10px] font-medium text-foreground backdrop-blur-sm">
                  {node.label}
                </span>
              </div>
            )
          })}
        </div>

        <div className="flex items-center justify-between rounded-lg border border-critical/25 bg-critical/10 px-3 py-2">
          <div className="flex items-center gap-2 text-xs">
            <Crosshair className="size-4 text-critical" />
            <span className="text-muted-foreground">
              <span className="font-semibold text-critical">{hops} hops</span> to Domain Admin
            </span>
          </div>
        </div>

        {!expanded && (
          <Button variant="outline" className="w-full" onClick={onViewFullGraph}>
            View Full Graph
            <ArrowRight data-icon="inline-end" />
          </Button>
        )}
      </CardContent>
    </Card>
  )
}
