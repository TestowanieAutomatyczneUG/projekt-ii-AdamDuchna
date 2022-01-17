from unittest import mock, TestCase

from src.Messenger import Messenger


class MessengerServiceTests(TestCase):
    def setUp(self):
        self.connect = mock.Mock(return_value=0)
        self.service = mock.Mock()

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

    def test_establish_service_assert_connection_called_once_with_service(self):
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.connect.assert_called_once_with(self.service)


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

    def test_send_data_message_wrong_type_list(self):
        type(self.service).message_data = mock.PropertyMock(return_value={'message': [], 'server': '242.16.184.252:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))

    def test_send_data_message_wrong_type_dict(self):
        type(self.service).message_data = mock.PropertyMock(return_value={'message': {}, 'server': '242.16.184.252:5000'})
        messenger = Messenger(self.service, self.connect)
        messenger.establish_service()
        self.assertEqual(2, messenger.send_data(**self.service.message_data))