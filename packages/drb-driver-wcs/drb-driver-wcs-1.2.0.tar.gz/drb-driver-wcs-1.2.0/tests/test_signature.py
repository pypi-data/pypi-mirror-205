import unittest
import uuid

from drb.core.factory import FactoryLoader
from drb.nodes.logical_node import DrbLogicalNode
from drb.topics.dao import ManagerDao
from drb.topics.topic import TopicCategory

from drb.drivers.wcs import WcsFactory


class TestWcsSignature(unittest.TestCase):
    svc_url = 'http+wcs://my.domain.com/wcs'
    svc_url_false = 'https://my.domain.com/wcs'
    fc_loader = None
    topic_loader = None
    wcs_id = uuid.UUID('dc71a76b-35dd-485b-ba5d-6c4464145364')

    @classmethod
    def setUpClass(cls) -> None:
        cls.fc_loader = FactoryLoader()
        cls.topic_loader = ManagerDao()

    def test_impl_loading(self):
        factory_name = 'wcs'

        factory = self.fc_loader.get_factory(factory_name)
        self.assertIsNotNone(factory)
        self.assertIsInstance(factory, WcsFactory)

        topic = self.topic_loader.get_drb_topic(self.wcs_id)
        self.assertIsNotNone(factory)
        self.assertEqual(self.wcs_id, topic.id)
        self.assertEqual('Web Coverage Service (WCS)', topic.label)
        self.assertIsNone(topic.description)
        self.assertEqual(TopicCategory.PROTOCOL, topic.category)
        self.assertEqual(factory_name, topic.factory)

    def test_impl_signatures(self):
        topic = self.topic_loader.get_drb_topic(self.wcs_id)
        node = DrbLogicalNode(self.svc_url)
        self.assertTrue(topic.matches(node))

        node = DrbLogicalNode(f'{self.svc_url_false}')
        self.assertFalse(topic.matches(node))

        node = DrbLogicalNode(f'http://not.odata.svc')
        self.assertFalse(topic.matches(node))
