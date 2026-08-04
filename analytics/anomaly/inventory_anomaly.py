from analytics.anomaly.base import RobustAnomalyDetector


class InventoryAnomaly(RobustAnomalyDetector):
    metric = "inventory"
    expected_direction = "both"
