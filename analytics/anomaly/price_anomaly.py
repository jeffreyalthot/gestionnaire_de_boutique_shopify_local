from analytics.anomaly.base import RobustAnomalyDetector


class PriceAnomaly(RobustAnomalyDetector):
    metric = "price"
    expected_direction = "both"
