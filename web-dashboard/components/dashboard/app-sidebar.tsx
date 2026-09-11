'use client'

import {
  ShieldHalf,
  LayoutDashboard,
  Bug,
  Fingerprint,
  Route,
  Siren,
  Settings,
  PanelLeftClose,
  PanelLeftOpen,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'

export const navItems = [
  { label: 'Overview', icon: LayoutDashboard },
  { label: 'Vulnerabilities', icon: Bug, badge: '30' },
  { label: 'Identities', icon: Fingerprint, badge: '30' },
  { label: 'Attack Paths', icon: Route },
  { label: 'Incidents', icon: Siren, badge: '24' },
  { label: 'Settings', icon: Settings },
]

export function AppSidebar({
  collapsed,
  onToggle,
  mobileOpen,
  onCloseMobile,
  active,
  onSelect,
}: {
  collapsed: boolean
  onToggle: () => void
  mobileOpen: boolean
  onCloseMobile: () => void
  active: string
  onSelect: (label: string) => void
}) {
  return (
    <>
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-background/70 backdrop-blur-sm lg:hidden"
          onClick={onCloseMobile}
          aria-hidden
        />
      )}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 flex flex-col border-r border-sidebar-border bg-sidebar transition-all duration-300 lg:static lg:z-auto',
          collapsed ? 'w-[72px]' : 'w-64',
          mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
        )}
      >
        <div
          className={cn(
            'flex h-16 items-center gap-2.5 border-b border-sidebar-border px-4',
            collapsed && 'justify-center px-0',
          )}
        >
          <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/15 text-primary ring-1 ring-primary/30">
            <ShieldHalf className="size-5" />
          </div>
          {!collapsed && (
            <div className="flex flex-col leading-none">
              <span className="text-sm font-semibold tracking-[0.2em] text-sidebar-foreground">
                XENTRA
              </span>
              <span className="mt-1 text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
                Threat Fusion
              </span>
            </div>
          )}
        </div>

        <nav className="flex flex-1 flex-col gap-1 p-3">
          {navItems.map((item) => {
            const isActive = active === item.label
            const link = (
              <button
                key={item.label}
                type="button"
                onClick={() => {
                  onSelect(item.label)
                  onCloseMobile()
                }}
                className={cn(
                  'group relative flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
                  collapsed && 'justify-center px-0',
                  isActive
                    ? 'bg-sidebar-accent text-sidebar-accent-foreground'
                    : 'text-muted-foreground hover:bg-sidebar-accent/60 hover:text-sidebar-foreground',
                )}
              >
                {isActive && (
                  <span className="absolute left-0 top-1/2 h-5 w-0.5 -translate-y-1/2 rounded-r bg-primary" />
                )}
                <item.icon className="size-[18px] shrink-0" />
                {!collapsed && <span className="flex-1 text-left">{item.label}</span>}
                {!collapsed && item.badge && (
                  <span className="rounded-full bg-secondary px-2 py-0.5 text-[10px] font-semibold text-secondary-foreground">
                    {item.badge}
                  </span>
                )}
              </button>
            )

            return collapsed ? (
              <Tooltip key={item.label}>
                <TooltipTrigger render={link} />
                <TooltipContent side="right">{item.label}</TooltipContent>
              </Tooltip>
            ) : (
              link
            )
          })}
        </nav>

        <div className="border-t border-sidebar-border p-3">
          <button
            type="button"
            onClick={onToggle}
            className={cn(
              'hidden w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-sidebar-accent/60 hover:text-sidebar-foreground lg:flex',
              collapsed && 'justify-center px-0',
            )}
          >
            {collapsed ? (
              <PanelLeftOpen className="size-[18px]" />
            ) : (
              <>
                <PanelLeftClose className="size-[18px]" />
                <span>Collapse</span>
              </>
            )}
          </button>
          {!collapsed && (
            <div className="mt-3 rounded-lg border border-low/25 bg-low/10 px-3 py-2.5">
              <div className="flex items-center gap-2">
                <span className="size-2 rounded-full bg-low shadow-[0_0_8px] shadow-low/60" />
                <span className="text-xs font-medium text-low">Sensors online</span>
              </div>
              <p className="mt-1 text-[11px] text-muted-foreground">
                Last sync 12s ago · 42 sources
              </p>
            </div>
          )}
        </div>
      </aside>
    </>
  )
}
