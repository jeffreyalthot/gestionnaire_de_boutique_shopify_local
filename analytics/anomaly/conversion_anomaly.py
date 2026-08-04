from analytics.anomaly.base import RobustAnomalyDetector


class ConversionAnomaly(RobustAnomalyDetector):
    metric = "conversion"
    expected_direction = "down"
