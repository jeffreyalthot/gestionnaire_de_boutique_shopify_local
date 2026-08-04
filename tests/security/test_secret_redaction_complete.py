from security.token_redactor import redact_text

def test_all_common_token_forms_are_redacted():
    value=redact_text("access_token=abc refresh_token=def Authorization=ghi Bearer xyz.123")
    assert "abc" not in value and "def" not in value and "ghi" not in value and "xyz.123" not in value
    assert value.count("***")>=4
