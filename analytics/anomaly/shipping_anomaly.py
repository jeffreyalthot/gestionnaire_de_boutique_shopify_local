from analytics.anomaly.base import RobustAnomalyDetector


class ShippingAnomaly(RobustAnomalyDetector):
    metric = "shipping"
    expected_direction = "up"
