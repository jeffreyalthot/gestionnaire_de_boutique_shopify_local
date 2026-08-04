from security.command_authorizer import CommandAuthorizer

def test_sensitive_command_requires_role_and_approval():
    auth=CommandAuthorizer()
    assert not auth.authorize("viewer","inventory-sync").allowed
    assert not auth.authorize("administrator","supplier-pay",sensitive=True).allowed
    assert auth.authorize("administrator","supplier-pay",sensitive=True,approved=True).allowed
