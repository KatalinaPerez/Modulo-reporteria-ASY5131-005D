import unittest
from unittest.mock import patch
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import api_clients


class TestApiClients(unittest.TestCase):

    @patch('api_clients.requests.get')
    def test_obtener_ventas(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"producto": "Camiseta", "cantidad": 10, "total": 100}
        ]
        ventas = api_clients.obtener_ventas()
        self.assertEqual(len(ventas), 1)
        self.assertEqual(ventas[0]["producto"], "Camiseta")

    @patch('api_clients.requests.get')
    def test_obtener_seguridad(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"evento": "Acceso no autorizado", "hora": "12:00"}
        ]
        seguridad = api_clients.obtener_seguridad()
        self.assertEqual(len(seguridad), 1)
        self.assertIn("evento", seguridad[0])

    @patch('api_clients.requests.get')
    def test_obtener_despachos(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"producto": "Zapatos", "destino": "Bodega", "cantidad": 5}
        ]
        despachos = api_clients.obtener_despachos()
        self.assertEqual(despachos[0]["producto"], "Zapatos")

#::::::::::::::::::::::::: ERROR 404 ::::::::::::::::::::::
    @patch('api_clients.requests.get')
    def test_obtener_ventas_error_404(self, mock_get):
        # Simulamos que la URL no existe (Error 404)
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        ventas = api_clients.obtener_ventas()

        # Comprobamos que la función devuelve una lista vacía en caso de error
        self.assertEqual(ventas, [])

    @patch('api_clients.requests.get')
    def test_obtener_seguridad_error_404(self, mock_get):
        # Simulamos que la URL no existe (Error 404)
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        seguridad = api_clients.obtener_seguridad()

        # Comprobamos que la función devuelve una lista vacía en caso de error
        self.assertEqual(seguridad, [])

    @patch('api_clients.requests.get')
    def test_obtener_despachos_error_404(self, mock_get):
        # Simulamos que la URL no existe (Error 404)
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        despachos = api_clients.obtener_despachos()

        # Comprobamos que la función devuelve una lista vacía en caso de error
        self.assertEqual(despachos, [])

if __name__ == '__main__':
    unittest.main()


