import http.client
import unittest
from unittest import mock, TestCase

from src.Messenger import Messenger


class MessengerServiceTests(TestCase):
    def setUp(self):
        self.connect = mock.Mock(return_value=0)
        self.service = mock.Mock()

    def test_establish_service_assert_connection_called_once_with_service(self):
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.connect.assert_called_once_with(self.service)

    def test_mock_connect_returns_0_or_1(self):
        self.assertTrue(0 <= self.connect(mock.ANY) <= 1)

    def test_connect_is_instance_of_mock(self):
        self.assertIsInstance(self.connect, mock.Mock)

    def test_service_is_instance_of_mock(self):
        self.assertIsInstance(self.service, mock.Mock)

    def test_establish_service_fail(self):
        self.connect.return_value = 1
        messenger = Messenger(self.service, self.connect)
        self.assertEqual(1, messenger.establish_service())

    def test_establish_service_success(self):
        messenger = Messenger(self.service, self.connect)
        self.assertEqual(0, messenger.establish_service())

    def test_establish_service_connection_exception(self):
        self.connect.side_effect = Exception("Could not connect")
        messenger = Messenger(self.service, self.connect)
        self.assertEqual(1, messenger.establish_service())


class MessengerValidateAndSaveDataTests(TestCase):
    def setUp(self):
        message_data = mock.PropertyMock(return_value={'message': 'Hi Jacob', 'server': '250.11.184.255:5000'})
        self.connect = mock.Mock(return_value=0)
        self.service = mock.Mock()
        type(self.service).message_data = message_data

    def test_send_data_non_established_service(self):
        messenger = Messenger(self.service, self.connect)
        self.assertEqual(1, messenger.send_data(**self.service.message_data))

    def test_send_data_established_service(self):
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(0, messenger.send_data(**self.service.message_data))

    def test_send_data_message_type_list(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': [], 'server': '242.16.184.252:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_message_type_dict(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': {}, 'server': '242.16.184.252:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_message_type_number(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 3, 'server': '242.16.184.252:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_message_type_boolean(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': True, 'server': '242.16.184.252:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_message_type_string(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Paweł', 'server': '242.16.184.252:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertGreaterEqual(1, messenger.send_data(**self.service.message_data))

    def test_send_data_server_type_list(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': []})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_type_dict(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': {}})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_type_boolean(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': True})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_type_string(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '222.19.124.211:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertGreater(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv4(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '212.29.124.211:4520'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(0, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv4_out_of_bounds(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '268.19.124.211:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv4_contains_letters(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '2a8.1W.124.2f1:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv4_contains_special_characters(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '2*8.1%6.12).221:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv4_port_out_of_bounds(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '212.19.124.211:70525'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv4_port_contains_letters(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '212.19.124.211:7ffa5'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv4_port_contains_special_characters(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '212.19.124.211:7^*5'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv6(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': '42a3:5e8a:d8d3:6a87:c05b:ab38:7e88:ebf0:4520'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(0, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv6_uppercase(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Jarek', 'server': 'FE80:0000:0000:0000:0202:B3FF:FE1E:8329:4260'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(0, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv6_out_of_bounds(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': 'dc8f:527c:z00a:a1l1:fb72:bbc2:3767:017a:8525'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv6_contains_special_characters(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': 'dc8f:52!c:z00[:a1l1:f&72:bbc2:3767:017a:8525'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_server_ipv6_port_out_of_bounds(self):
        type(self.service).message_data = mock.PropertyMock(
            return_value={'message': 'Cześć Janek', 'server': 'FE80:0000:0000:0000:0202:B3FF:FE1E:8329:4260:70525'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))


class MessengerSocketSendDataTest(TestCase):
    def setUp(self):
        message_data = mock.PropertyMock(return_value={'message': 'Hi Jacob', 'server': '250.11.184.255:5000'})
        self.connect = mock.Mock(return_value=0)
        self.service = mock.Mock()
        self.http = mock.create_autospec(http.client, spec_set=True, instance=True)
        type(self.service).message_data = message_data
        self.messenger = Messenger(self.service, self.connect)
        self.messenger.establish_service()
        self.messenger.send_data(**self.service.message_data)

    def test_message_data_mock(self):
        self.assertTrue('message' in self.service.message_data and 'server' in self.service.message_data)

    def test_connector_called_request_with_message(self):
        connector = mock.MagicMock()
        connector.getresponse.return_value = mock.ANY
        self.http.HTTPSConnection.return_value = connector
        self.messenger.establish_http_and_send(self.http)
        connector.request.assert_called_once_with('POST', '/messages', 'Hi Jacob')

    def test_connector_closed(self):
        connector = mock.MagicMock()
        connector.getresponse.return_value = mock.ANY
        self.http.HTTPSConnection.return_value = connector
        self.messenger.establish_http_and_send(self.http)
        connector.close.assert_called()

    def test_connector_got_response(self):
        connector = mock.MagicMock()
        connector.getresponse.return_value = mock.ANY
        self.http.HTTPSConnection.return_value = connector
        self.messenger.establish_http_and_send(self.http)
        connector.getresponse.assert_called_once()

    def test_establish_http_and_send_status_200(self):
        connector = mock.MagicMock()
        connector.getresponse.return_value = 200
        self.http.HTTPSConnection.return_value = connector
        self.assertEqual(0, self.messenger.establish_http_and_send(self.http))

    def test_establish_http_and_send_status_404(self):
        connector = mock.MagicMock()
        connector.getresponse.return_value = 404
        self.http.HTTPSConnection.return_value = connector
        self.assertEqual(1, self.messenger.establish_http_and_send(self.http))

    def test_establish_http_and_send_status_400(self):
        connector = mock.MagicMock()
        connector.getresponse.return_value = 400
        self.http.HTTPSConnection.return_value = connector
        self.assertEqual(1, self.messenger.establish_http_and_send(self.http))

    def test_establish_http_and_send_status_403(self):
        connector = mock.MagicMock()
        connector.getresponse.return_value = 403
        self.http.HTTPSConnection.return_value = connector
        self.assertEqual(1, self.messenger.establish_http_and_send(self.http))

    def test_establish_http_and_send_status_408(self):
        connector = mock.MagicMock()
        connector.getresponse.return_value = 408
        self.http.HTTPSConnection.return_value = connector
        self.assertEqual(1, self.messenger.establish_http_and_send(self.http))

    def test_establish_http_and_send_to_fake_server(self):
        server = fake_server()
        connector = mock.create_autospec(server, spec_set=True, )
        connector.request = mock.Mock(side_effect=server.request)
        connector.getresponse = mock.Mock(side_effect=server.getresponse)
        connector.close = mock.Mock(side_effect=server.close)
        self.http.HTTPSConnection.return_value = connector
        self.assertEqual(0, self.messenger.establish_http_and_send(self.http))

    def test_spy_called_request_fake_server(self):
        server = fake_server()
        connector = mock.create_autospec(server, spec_set=True, )
        connector.request = mock.Mock(side_effect=server.request)
        connector.getresponse = mock.Mock(side_effect=server.getresponse)
        connector.close = mock.Mock(side_effect=server.close)
        self.http.HTTPSConnection.return_value = connector
        self.messenger.establish_http_and_send(self.http)
        connector.request.assert_called_once()

    def test_spy_called_getresponse_fake_server(self):
        server = fake_server()
        connector = mock.create_autospec(server, spec_set=True, )
        connector.request = mock.Mock(side_effect=server.request)
        connector.getresponse = mock.Mock(side_effect=server.getresponse)
        connector.close = mock.Mock(side_effect=server.close)
        self.http.HTTPSConnection.return_value = connector
        self.messenger.establish_http_and_send(self.http)
        connector.getresponse.assert_called_once()

    def test_spy_called_close_fake_server(self):
        server = fake_server()
        connector = mock.create_autospec(server, spec_set=True, )
        connector.request = mock.Mock(side_effect=server.request)
        connector.getresponse = mock.Mock(side_effect=server.getresponse)
        connector.close = mock.Mock(side_effect=server.close)
        self.http.HTTPSConnection.return_value = connector
        self.messenger.establish_http_and_send(self.http)
        connector.close.assert_called_once()


class fake_server:
    def request(self, method, route, message):
        if method == "POST" and route == "/messages":
            self.response = server_message_process_stub(message)
        else:
            self.response = 405

    def getresponse(self):
        return self.response

    def close(self):
        self.is_closed = True


def server_message_process_stub(message):
    return 200


if __name__ == "__main__":
    unittest.main()
