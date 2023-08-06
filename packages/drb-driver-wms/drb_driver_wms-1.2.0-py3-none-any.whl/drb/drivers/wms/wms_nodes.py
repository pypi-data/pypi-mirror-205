from __future__ import annotations
from drb.core.predicate import Predicate

from requests.auth import AuthBase

from drb.drivers.wxs import WXSServiceNode, WXSNodeOperation


class WmsServiceNode(WXSServiceNode):
    def __init__(self, url: str, auth: AuthBase = None, **kwargs):
        if kwargs is not None and len(kwargs) > 0:
            super(WmsServiceNode, self).__init__(url, auth=auth, **kwargs)
        else:
            super(WmsServiceNode, self).__init__(url, auth)
        self._service_url = url.replace("+wms", "") if "+wms" in url else url
        self.namespace_uri = "WMS"
        self.name = self._service_url

    @property
    def type_service(self):
        return "WMS"

    def manage_predefined_operations_metadata(self):
        return None

    def read_capabilities(self, xmlnode_tree):
        super().read_capabilities(xmlnode_tree)
        xmlnode = xmlnode_tree["Capability"]

        for child in xmlnode:
            if child.name == "Request":
                for request_cap in child:
                    format_attr = []
                    DCPType = None

                    for child in request_cap.children:
                        if child.name == "Format":
                            format_attr.append(child.value)
                        if child.name == "DCPType":
                            DCPType = request_cap["DCPType"]

                    attr = {
                        ("Format", None): format_attr,
                        ("DCPType", None): DCPType,
                    }

                    if request_cap.name.lower() == "getfeatureinfo":
                        operation = WmsNodeOperationGetFeatureInfo(
                            self,
                            name=request_cap.name,
                            namespace=request_cap.namespace_uri,
                            attributes=attr,
                            version=self._version,
                        )
                    elif request_cap.name.lower() == "getmap":
                        operation = WmsNodeOperationGetMap(
                            self,
                            name=request_cap.name,
                            namespace=request_cap.namespace_uri,
                            attributes=attr,
                            version=self._version,
                        )
                    else:
                        operation = WXSNodeOperation(
                            self,
                            name=request_cap.name,
                            namespace=request_cap.namespace_uri,
                            attributes=attr,
                            version=self._version,
                        )

                    self._children.append(operation)
            else:
                self._children.append(child)


class WmsGetMapPredicate(Predicate):
    def __init__(
        self,
        layers,
        bbox,
        width,
        height,
        styles="",
        format="image/png",
        crs="EPSG:3857",
        **kwargs,
    ):

        self._layers = layers
        self._bbox = bbox
        self._width = width
        self._height = height
        self._styles = styles
        self._format = format
        self._csr = crs

        self.others = dict(kwargs)

    def to_dict(self):
        arg_dict = {
            "layers": self._layers,
            "styles": self._styles,
            "crs": self._csr,
            "bbox": self._bbox,
            "width": self._width,
            "height": self._height,
            "format": self._format,
        }
        arg_dict.update(self.others)

        return arg_dict

    def matches(self, key) -> bool:
        return False


class WmsGetFeatureInfoPredicate(WmsGetMapPredicate):
    def __init__(
        self,
        query_layers,
        i,
        j,
        bbox,
        width,
        height,
        layers=None,
        styles="",
        info_format="application/json",
        crs="EPSG:3857",
        **kwargs,
    ):

        super().__init__(
            layers, bbox, width, height, styles, format=None, crs=crs, **kwargs
        )
        self._query_layers = query_layers

        if self._layers is None:
            self._layers = query_layers
        self._info_format = info_format
        self._i = i
        self._j = j

    def to_dict(self):
        arg_dict = {
            "query_layers": self._query_layers,
            "i": self._i,
            "j": self._j,
        }
        arg_dict.update(super().to_dict())

        return arg_dict

    def matches(self, key) -> bool:
        return False


class WmsNodeOperationGetMap(WXSNodeOperation):
    def __getitem__(self, item):

        if isinstance(item, WmsGetMapPredicate):
            return self._get_child(item.to_dict())

        return self._get_child(item)


class WmsNodeOperationGetFeatureInfo(WXSNodeOperation):
    def __getitem__(self, item):

        if isinstance(item, WmsGetFeatureInfoPredicate):
            return self._get_child(item.to_dict())

        return self._get_child(item)
