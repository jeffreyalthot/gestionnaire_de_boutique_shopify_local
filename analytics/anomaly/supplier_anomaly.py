from analytics.anomaly.base import RobustAnomalyDetector


class SupplierAnomaly(RobustAnomalyDetector):
    metric = "supplier"
    expected_direction = "up"
