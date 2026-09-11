import { cn } from '@/lib/utils'
import type { Severity } from '@/lib/data'

const styles: Record<Severity, string> = {
  critical: 'bg-critical/15 text-critical border-critical/30',
  high: 'bg-high/15 text-high border-high/30',
  medium: 'bg-medium/15 text-medium border-medium/30',
  low: 'bg-low/15 text-low border-low/30',
}

const dot: Record<Severity, string> = {
  critical: 'bg-critical',
  high: 'bg-high',
  medium: 'bg-medium',
  low: 'bg-low',
}

export function SeverityBadge({
  severity,
  label,
  className,
}: {
  severity: Severity
  label?: string
  className?: string
}) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize',
        styles[severity],
        className,
      )}
    >
      <span className={cn('size-1.5 rounded-full', dot[severity])} aria-hidden />
      {label ?? severity}
    </span>
  )
}
