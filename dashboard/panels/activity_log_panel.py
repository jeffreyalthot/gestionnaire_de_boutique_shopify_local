from dashboard.panels.base_panel import PanelField, StatePanel


class ActivityLogPanel(StatePanel):
    title = 'Activity'
    fields = (
        PanelField('Events', 'events', 'integer'),
        PanelField('Last event', 'last_event', 'text'),
        PanelField('Errors', 'errors', 'integer'),
    )
