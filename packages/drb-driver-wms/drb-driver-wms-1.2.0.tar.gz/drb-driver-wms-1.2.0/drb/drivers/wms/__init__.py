from . import _version
from .wms_nodes import WmsServiceNode, WmsNodeOperationGetMap, \
    WmsNodeOperationGetFeatureInfo, WmsGetMapPredicate, \
    WmsGetFeatureInfoPredicate
from .factory import WmsFactory

__version__ = _version.get_versions()['version']
__all__ = [
    'WmsServiceNode',
    'WmsNodeOperationGetMap',
    'WmsNodeOperationGetFeatureInfo',
    'WmsGetMapPredicate',
    'WmsGetFeatureInfoPredicate',
    'WmsFactory']
