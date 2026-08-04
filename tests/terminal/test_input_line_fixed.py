from dashboard.input_line_controller import InputLineController

def test_input_line_has_fixed_width_and_no_newlines():
    line=InputLineController(max_length=8); line.insert("abc\ndefghijkl")
    rendered=line.render(12)
    assert len(rendered)==12 and "\n" not in rendered and line.submit()=="abcdefgh"
