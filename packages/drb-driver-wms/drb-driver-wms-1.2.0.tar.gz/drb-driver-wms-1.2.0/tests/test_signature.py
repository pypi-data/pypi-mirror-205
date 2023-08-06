import os
import sys
import unittest
import uuid

from drb.core.factory import FactoryLoader
from drb.nodes.logical_node import DrbLogicalNode
from drb.topics.dao import ManagerDao
from drb.topics.topic import TopicCategory

from drb.drivers.wms.factory import WmsFactory


class TestOdataSignature(unittest.TestCase):
    svc_url = 'http+wms://my.domain.com/wms'
    svc_url_false = 'https://my.domain.com/wms'
    mock_pkg = None
    fc_loader = None
    topic_loader = None
    wms_id = uuid.UUID('75410c6f-5926-4077-9409-38e2d2613572')

    @classmethod
    def setUpClass(cls) -> None:

        cls.fc_loader = FactoryLoader()
        cls.topic_loader = ManagerDao()

    def test_impl_loading(self):
        factory_name = 'wms'

        factory = self.fc_loader.get_factory(factory_name)
        self.assertIsNotNone(factory)
        self.assertIsInstance(factory, WmsFactory)

        topic = self.topic_loader.get_drb_topic(self.wms_id)
        self.assertIsNotNone(factory)
        self.assertEqual(self.wms_id, topic.id)
        self.assertEqual('Web Map Service (WMS)', topic.label)
        self.assertIsNone(topic.description)
        self.assertEqual(TopicCategory.PROTOCOL, topic.category)
        self.assertEqual(factory_name, topic.factory)

    def test_impl_signatures(self):
        topic = self.topic_loader.get_drb_topic(self.wms_id)
        node = DrbLogicalNode(self.svc_url)
        self.assertTrue(topic.matches(node))

        node = DrbLogicalNode(f'{self.svc_url_false}')
        self.assertFalse(topic.matches(node))

        node = DrbLogicalNode(f'http://not.odata.svc')
        self.assertFalse(topic.matches(node))
