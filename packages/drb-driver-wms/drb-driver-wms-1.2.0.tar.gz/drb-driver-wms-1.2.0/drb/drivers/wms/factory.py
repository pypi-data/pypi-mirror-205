from drb.core import DrbNode
from drb.core.factory import DrbFactory
from drb.drivers.http import DrbHttpNode
from drb.exceptions.core import DrbFactoryException

from .wms_nodes import WmsServiceNode


class WmsFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, WmsServiceNode):
            return node
        if isinstance(node, DrbHttpNode):
            node_wms_service = WmsServiceNode(
                url=node.path.original_path, auth=node.auth
            )
        else:
            node_wms_service = WmsServiceNode(node.path.name)
        try:
            node_wms_service.children
        except Exception as e:
            final_url = node.path.name.replace("+wms", "")
            raise DrbFactoryException(f"Unsupported Wms service: {final_url}")
        return node_wms_service
