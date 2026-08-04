from automation.core.autonomy_controller import AutonomyController

def test_autonomy_controller_enforces_confidence_and_money_limits():
    controller=AutonomyController(dry_run=False,minimum_confidence=.9,financial_limit_cad=100)
    assert controller.decide(risk="read",confidence=.5).approval_required
    assert controller.decide(risk="financial",amount_cad=150,approved=True).reason=="financial_limit_exceeded"
