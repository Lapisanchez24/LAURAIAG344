from proccessor import clean_id, merge_name
def test_clean_id():
    assert clean_id("cc-111.530.476") == "111530476"


def test_merge_name():
    assert merge_name("Laura", "Sánchez") == "Laura Sánchez"
 