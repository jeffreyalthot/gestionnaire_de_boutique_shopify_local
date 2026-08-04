from dashboard.panels.base_panel import PanelField, StatePanel


class CatalogMediaPanel(StatePanel):
    title = 'Catalog Media'
    fields = (
        PanelField('Queued', 'queued', 'integer'),
        PanelField('Downloaded', 'downloaded', 'integer'),
        PanelField('Rejected', 'rejected', 'integer'),
        PanelField('Cache', 'cache_bytes', 'bytes'),
    )
