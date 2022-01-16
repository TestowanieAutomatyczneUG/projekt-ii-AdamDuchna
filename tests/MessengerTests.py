from unittest import mock,TestCase
from src.Messenger import Messenger

class MessengerTests(TestCase):
    def test_establish_service_fail(self):
        connect = mock.Mock(return_value=1)
        service = mock.Mock()
        messenger = Messenger(service,connect)
        self.assertEqual(1,messenger.establishService())
    def test_establish_service_sucess(self):
        connect = mock.Mock(return_value=0)
        service = mock.Mock()
        messenger = Messenger(service,connect)
        self.assertEqual(0,messenger.establishService())
