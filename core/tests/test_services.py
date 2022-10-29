import logging
from django.test import TestCase
from core.services import Serializing, AddArticlePageService
from core.forms import AddArticleForm


logger = logging.getLogger("debug")


class SerializingTest(TestCase):
    def test_serialize(self):
        result = Serializing.serialize([{"key": "value"}])
        self.assertEqual(type(result), str)
        logger.debug("serialize() method is ---OK")

    def test_deserialize(self):
        json = Serializing.serialize({"key": "value"})
        result = Serializing.deserialize(json)
        self.assertEqual(type(result), dict)
        logger.debug("deserialize() method is ---OK")


class UserMarkServiceTest(TestCase):
    pass
