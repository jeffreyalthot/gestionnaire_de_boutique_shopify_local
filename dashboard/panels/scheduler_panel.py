from dashboard.panels.base_panel import PanelField, StatePanel


class SchedulerPanel(StatePanel):
    title = 'Scheduler'
    fields = (
        PanelField('Jobs', 'jobs', 'integer'),
        PanelField('Running', 'running', 'integer'),
        PanelField('Missed', 'missed', 'integer'),
        PanelField('Next', 'next_run', 'text'),
    )
