from analytics.anomaly.base import RobustAnomalyDetector


class CashflowAnomaly(RobustAnomalyDetector):
    metric = "cashflow"
    expected_direction = "down"
