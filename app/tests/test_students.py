def test_create_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Hamza",
            "reg_no": "2212251",
            "department": "BSCS"
        }
    )

    assert response.status_code == 200


def test_get_students(client):
    response = client.get("/students")

    assert response.status_code == 200


def test_get_single_student(client):
    response = client.get("/students/2212251")

    assert response.status_code == 200
