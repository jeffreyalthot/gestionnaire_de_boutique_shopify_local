from dashboard.panels.base_panel import PanelField, StatePanel


class CatalogPanel(StatePanel):
    title = 'Catalog'
    fields = (
        PanelField('Products', 'products', 'integer'),
        PanelField('Active', 'active', 'integer'),
        PanelField('Candidates', 'candidates', 'integer'),
        PanelField('Quarantined', 'quarantined', 'integer'),
    )
