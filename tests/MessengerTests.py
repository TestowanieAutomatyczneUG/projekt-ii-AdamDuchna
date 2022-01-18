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

    def test_establish_service_sucess(self):
        messenger = Messenger(self.service, self.connect)
        self.assertEqual(0, messenger.establish_service())

    def test_establish_service_connection_exception(self):
        self.connect.side_effect = Exception("Could not connect")
        messenger = Messenger(self.service, self.connect)
        self.assertEqual(1, messenger.establish_service())


class MessengerSendDataTests(TestCase):
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
        self.assertEqual(0, messenger.send_data(**self.service.message_data))

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
        self.assertEqual(0, messenger.send_data(**self.service.message_data))

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


if __name__ == "__main__":
    unittest.main()
