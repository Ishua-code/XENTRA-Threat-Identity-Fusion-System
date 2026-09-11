'use client'

import { Bar, BarChart, Cell, XAxis, YAxis, CartesianGrid } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ChartContainer, ChartTooltip } from '@/components/ui/chart'
import { topRiskFindings, severityFromScore } from '@/lib/data'

const severityColor: Record<string, string> = {
  critical: 'var(--critical)',
  high: 'var(--high)',
  medium: 'var(--medium)',
  low: 'var(--low)',
}

const chartData = topRiskFindings.map((f) => ({
  cve: f.cve,
  score: f.score,
  severity: severityFromScore(f.score),
}))

export function RiskScoreChart() {
  return (
    <Card className="h-full">
      <CardHeader>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <CardTitle>Unified Risk Score</CardTitle>
            <CardDescription>Top 10 findings ranked by fused risk (0–1)</CardDescription>
          </div>
          <div className="flex items-center gap-3 text-[11px] text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <span className="size-2 rounded-full bg-critical" /> &gt; 0.7
            </span>
            <span className="flex items-center gap-1.5">
              <span className="size-2 rounded-full bg-high" /> 0.5–0.7
            </span>
            <span className="flex items-center gap-1.5">
              <span className="size-2 rounded-full bg-low" /> &lt; 0.5
            </span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <ChartContainer
          config={{ score: { label: 'Risk Score' } }}
          className="h-[360px] w-full"
        >
          <BarChart
            accessibilityLayer
            data={chartData}
            layout="vertical"
            margin={{ left: 8, right: 28, top: 4, bottom: 4 }}
          >
            <CartesianGrid horizontal={false} stroke="var(--border)" strokeDasharray="3 3" />
            <XAxis
              type="number"
              domain={[0, 1]}
              tickLine={false}
              axisLine={false}
              tick={{ fill: 'var(--muted-foreground)', fontSize: 11 }}
              tickFormatter={(v) => v.toFixed(1)}
            />
            <YAxis
              type="category"
              dataKey="cve"
              width={116}
              tickLine={false}
              axisLine={false}
              tick={{ fill: 'var(--muted-foreground)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
            />
            <ChartTooltip
              cursor={{ fill: 'var(--accent)', opacity: 0.4 }}
              content={({ active, payload }) => {
                if (!active || !payload?.length) return null
                const d = payload[0].payload as (typeof chartData)[number]
                return (
                  <div className="rounded-lg border border-border bg-popover px-3 py-2 shadow-xl">
                    <p className="font-mono text-xs font-medium text-popover-foreground">{d.cve}</p>
                    <p className="mt-1 flex items-center gap-1.5 text-xs text-muted-foreground">
                      <span
                        className="size-2 rounded-full"
                        style={{ background: severityColor[d.severity] }}
                      />
                      Risk score <span className="font-mono font-semibold text-foreground">{d.score.toFixed(2)}</span>
                    </p>
                  </div>
                )
              }}
            />
            <Bar dataKey="score" radius={[0, 4, 4, 0]} barSize={20}>
              {chartData.map((d) => (
                <Cell key={d.cve} fill={severityColor[d.severity]} />
              ))}
            </Bar>
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
