from app.contacts import load_contacts_from_csv
import tempfile, os

def test_load_contacts_from_csv():
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        f.write("phone\n+966500000001\n0500000002\nnot_a_phone\n")
    contacts, errors = load_contacts_from_csv(path)
    assert len(contacts) == 2
    # third row should be ignored and reported as error
    assert errors
