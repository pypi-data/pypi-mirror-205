import unittest
import uuid

from drb.core.factory import FactoryLoader
from drb.nodes.logical_node import DrbLogicalNode
from drb.topics.dao import ManagerDao
from drb.topics.topic import TopicCategory

from drb.drivers.wmts import WmtsFactory


class TestOdataSignature(unittest.TestCase):
    svc_url = 'http+wmts://my.domain.com/wmts'
    svc_url_false = 'https://my.domain.com/wmts'
    fc_loader = None
    topic_loader = None
    wmts_id = uuid.UUID('1293b94a-7e62-4e17-bc39-effcf7945cd7')

    @classmethod
    def setUpClass(cls) -> None:
        cls.fc_loader = FactoryLoader()
        cls.topic_loader = ManagerDao()

    def test_impl_loading(self):
        factory_name = 'wmts'

        factory = self.fc_loader.get_factory(factory_name)
        self.assertIsNotNone(factory)
        self.assertIsInstance(factory, WmtsFactory)

        topic = self.topic_loader.get_drb_topic(self.wmts_id)
        self.assertIsNotNone(factory)
        self.assertEqual(self.wmts_id, topic.id)
        self.assertEqual('Web Map Tile Service (WMTS)', topic.label)
        self.assertIsNone(topic.description)
        self.assertEqual(TopicCategory.PROTOCOL, topic.category)
        self.assertEqual(factory_name, topic.factory)

    def test_impl_signatures(self):
        topic = self.topic_loader.get_drb_topic(self.wmts_id)
        node = DrbLogicalNode(self.svc_url)
        self.assertTrue(topic.matches(node))

        node = DrbLogicalNode(f'{self.svc_url_false}')
        self.assertFalse(topic.matches(node))

        node = DrbLogicalNode(f'http://not.odata.svc')
        self.assertFalse(topic.matches(node))
