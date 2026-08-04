from analytics.anomaly.base import RobustAnomalyDetector


class OrderAnomaly(RobustAnomalyDetector):
    metric = "orders"
    expected_direction = "both"
