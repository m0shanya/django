from django.test import Client


class TestHomework:
    def test_homework_index_view(self):
        client = Client()

        response = client.get("/homework/")
        assert response.status_code == 200

        response = client.get("/homework/?get-key-1=test-key-1")
        assert response.status_code == 200

        response = client.get("/homework/?get-key-1=test-key-1&get-key-2=test-key-2&get-key-3=test-key-3")
        assert response.status_code == 200

        response = client.post("/homework/?get-key-1=test-key-1", data={"post-key-2": "test-key-2"})
        assert response.status_code == 200

        response = client.post("/homework/", data={"post-key-1": "test-key-1", "post-key-3": "test-key-2"})
        assert response.status_code == 200
