from analytics.anomaly.base import RobustAnomalyDetector


class RefundAnomaly(RobustAnomalyDetector):
    metric = "refunds"
    expected_direction = "up"
