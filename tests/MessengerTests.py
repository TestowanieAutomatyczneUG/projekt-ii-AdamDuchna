from unittest import mock, TestCase

from src.Messenger import Messenger


class MessengerTests(TestCase):
    def test_establish_service_fail(self):
        connect = mock.Mock(return_value=1)
        service = mock.Mock()
        messenger = Messenger(service, connect)
        self.assertEqual(1, messenger.establish_service())

    def test_establish_service_sucess(self):
        connect = mock.Mock(return_value=0)
        service = mock.Mock()
        messenger = Messenger(service, connect)
        self.assertEqual(0, messenger.establish_service())

    def test_establish_service_connection_called_with_service(self):
        connect = mock.Mock(return_value=0)
        service = mock.Mock()
        messenger = Messenger(service, connect)
        messenger.establish_service()
        connect.assert_called_once_with(service)

    def test_establish_service_connection_exception(self):
        connect = mock.Mock(return_value=Exception("Could not connect"))
        service = mock.Mock()
        messenger = Messenger(service, connect)
        messenger.establish_service()
        self.assertGreaterEqual(1,messenger.establish_service())


