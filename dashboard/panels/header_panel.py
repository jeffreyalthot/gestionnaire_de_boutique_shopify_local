from dashboard.panels.base_panel import PanelField, StatePanel


class HeaderPanel(StatePanel):
    title = 'Runtime'
    fields = (
        PanelField('Mode', 'mode', 'status'),
        PanelField('Profile', 'profile', 'text'),
        PanelField('Uptime', 'uptime_seconds', 'integer'),
        PanelField('Version', 'version', 'text'),
    )
