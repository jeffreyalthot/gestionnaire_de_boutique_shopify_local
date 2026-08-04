from observability.logger import redact
def test_redaction(): assert redact({"access_token":"abc"})["access_token"]=="***"
