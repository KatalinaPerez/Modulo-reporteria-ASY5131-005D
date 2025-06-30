import pytest
from django.urls import reverse 
from django.test import Client
import main_api.views as views

@pytest.mark.django_db
def test_editar_pdf_get():
    client = Client()
    response = client.get(reverse("editar_pdf"))

    assert response.status_code == 200
    assert b"Editar Datos del PDF" in response.content

@pytest.mark.django_db
def test_editar_pdf_post(monkeypatch):
    client = Client()

    fake_users = [
        {
            "id": 1,
            "name": "Tomas Vega",
            "username": "tomivega",
            "email": "tomas@example.com",
            "address": {
                "street": "Calle Falsa 123",
                "city": "Quilpué"
            }
        }
    ]

    # Mock requests.get
    class MockResponse:
        def json(self):
            return fake_users

    monkeypatch.setattr(views.requests, "get", lambda url: MockResponse())  

    # Mock boto3.client para evitar la subida real a S3
    class MockS3Client:
        def put_object(self, Bucket, Key, Body):
            print("✅ Simulando subida a S3")

    monkeypatch.setattr(views.boto3, "client", lambda *args, **kwargs: MockS3Client())  

    data = {
        "encargado": "Juan Pérez",
        "area": "Ventas",
        "descripcion": "Reporte generado en test",
        "nombre_1": "Tomas Vega",
        "usuario_1": "tomivega",
        "email_1": "tomas@example.com",
        "calle_1": "Calle Falsa 123",
        "ciudad_1": "Quilpué"
    }

    response = client.post(reverse("editar_pdf"), data)

    assert response.status_code == 200
    assert b"%PDF" in response.content 