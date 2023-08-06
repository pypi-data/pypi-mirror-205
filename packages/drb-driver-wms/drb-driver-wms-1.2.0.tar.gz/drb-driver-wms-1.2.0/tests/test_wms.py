import io
import unittest
from unittest import mock
from drb.drivers.http import DrbHttpNode
from drb.drivers.xml import XmlNode
from drb.drivers.json import JsonNode, JsonBaseNode

from drb.drivers.wxs import WXSNodeOperation
from drb.exceptions.core import DrbNotImplementationException
from drb.topics.resolver import _DrbFactoryResolver

from drb.drivers.wms import WmsServiceNode
from drb.drivers.wms.wms_nodes import WmsGetMapPredicate, \
    WmsGetFeatureInfoPredicate

stream_wms = b'<?xml version="1.0" encoding="UTF-8"?><WMS_Capabilities xmlns:inspire_vs="http://inspire.ec.europa.eu/schemas/inspire_vs/1.0" xmlns:inspire_common="http://inspire.ec.europa.eu/schemas/common/1.0" version="1.3.0" updateSequence="37" xmlns="http://www.opengis.net/wms" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wms http://geoserver.swarm.ops.internal.gael.fr/geoserver/schemas/wms/1.3.0/capabilities_1_3_0.xsd http://inspire.ec.europa.eu/schemas/inspire_vs/1.0 https://inspire.ec.europa.eu/schemas/inspire_vs/1.0/inspire_vs.xsd">\n  <Service>\n    <Name>WMS</Name>\n    <Title/>\n    <Abstract/>\n    <KeywordList/>\n    <OnlineResource xlink:type="simple" xlink:href="http://geoserver.swarm.ops.internal.gael.fr/geoserver/"/>\n    <ContactInformation>\n      <ContactPersonPrimary>\n        <ContactPerson/>\n        <ContactOrganization/>\n      </ContactPersonPrimary>\n      <ContactPosition/>\n      <ContactAddress>\n        <AddressType/>\n        <Address/>\n        <City/>\n        <StateOrProvince/>\n        <PostCode/>\n        <Country/>\n      </ContactAddress>\n      <ContactVoiceTelephone/>\n      <ContactFacsimileTelephone/>\n      <ContactElectronicMailAddress/>\n    </ContactInformation>\n    <Fees>none</Fees>\n    <AccessConstraints>none</AccessConstraints>\n  </Service>\n  <Capability>\n    <Request>\n      <GetCapabilities>\n        <Format>text/xml</Format>\n        <DCPType>\n          <HTTP>\n            <Get>\n              <OnlineResource xlink:type="simple" xlink:href="http://geoserver.swarm.ops.internal.gael.fr/geoserver/demo/ows?SERVICE=WMS&amp;"/>\n            </Get>\n            <Post>\n              <OnlineResource xlink:type="simple" xlink:href="http://geoserver.swarm.ops.internal.gael.fr/geoserver/demo/ows?SERVICE=WMS&amp;"/>\n            </Post>\n          </HTTP>\n        </DCPType>\n      </GetCapabilities>\n      <GetMap>\n        <Format>image/png</Format>\n        <Format>application/atom+xml</Format>\n        <Format>application/json;type=geojson</Format>\n        <Format>application/json;type=topojson</Format>\n        <Format>application/json;type=utfgrid</Format>\n        <Format>application/pdf</Format>\n        <Format>application/rss+xml</Format>\n        <Format>application/vnd.google-earth.kml+xml</Format>\n        <Format>application/vnd.google-earth.kml+xml;mode=networklink</Format>\n        <Format>application/vnd.google-earth.kmz</Format>\n        <Format>application/vnd.mapbox-vector-tile</Format>\n        <Format>image/geotiff</Format>\n        <Format>image/geotiff8</Format>\n        <Format>image/gif</Format>\n        <Format>image/jpeg</Format>\n        <Format>image/png; mode=8bit</Format>\n        <Format>image/svg+xml</Format>\n        <Format>image/tiff</Format>\n        <Format>image/tiff8</Format>\n        <Format>image/vnd.jpeg-png</Format>\n        <Format>image/vnd.jpeg-png8</Format>\n        <Format>text/html; subtype=openlayers</Format>\n        <Format>text/html; subtype=openlayers2</Format>\n        <Format>text/html; subtype=openlayers3</Format>\n        <DCPType>\n          <HTTP>\n            <Get>\n              <OnlineResource xlink:type="simple" xlink:href="http://geoserver.swarm.ops.internal.gael.fr/geoserver/demo/ows?SERVICE=WMS&amp;"/>\n            </Get>\n          </HTTP>\n        </DCPType>\n      </GetMap>\n      <GetFeatureInfo>\n        <Format>text/plain</Format>\n        <Format>application/vnd.ogc.gml</Format>\n        <Format>text/xml</Format>\n        <Format>application/vnd.ogc.gml/3.1.1</Format>\n        <Format>text/xml; subtype=gml/3.1.1</Format>\n        <Format>text/html</Format>\n        <Format>text/javascript</Format>\n        <Format>application/json</Format>\n        <DCPType>\n          <HTTP>\n            <Get>\n              <OnlineResource xlink:type="simple" xlink:href="http://geoserver.swarm.ops.internal.gael.fr/geoserver/demo/ows?SERVICE=WMS&amp;"/>\n            </Get>\n          </HTTP>\n        </DCPType>\n      </GetFeatureInfo>\n    </Request>\n    <Exception>\n      <Format>XML</Format>\n      <Format>INIMAGE</Format>\n      <Format>BLANK</Format>\n      <Format>JSON</Format>\n      <Format>JSONP</Format>\n    </Exception>\n    <Layer>\n      </Layer>\n  </Capability>\n</WMS_Capabilities>\n'  # noqa
stream_features = b'{"type":"FeatureCollection","features":[{"type":"Feature","id":"mgrs_region.20501","geometry":{"type":"MultiPolygon","coordinates":[[[[2186283.741,6231700.7722],[2186012.7894,6246896.7124],[2185740.5019,6262119.7873],[2185466.9899,6277369.9624],[2185191.9195,6292647.3726],[2184915.6245,6307952.324],[2184637.8824,6323284.9543],[2184358.8044,6338645.231],[2184078.2793,6354033.2925],[2183796.4183,6369449.4499],[2183512.9989,6384893.8443],[2198928.6333,6385164.4408],[2214345.4922,6385406.6784],[2229763.4644,6385620.211],[2245182.4383,6385805.552],[2260602.3029,6385962.1838],[2276022.8354,6386090.4488],[2291443.9244,6386190.1735],[2306865.4587,6386261.3571],[2322287.327,6386304.1707],[2337709.3067,6386318.442],[2337709.3067,6370866.9603],[2337709.3067,6355443.7452],[2337709.3067,6340048.6553],[2337709.3067,6324681.3793],[2337709.3067,6309341.9489],[2337709.3067,6294030.0554],[2337709.3067,6278745.7317],[2337709.3067,6263488.6713],[2337709.3067,6248258.9082],[2337709.3067,6233056.3073],[2322564.5126,6233042.7998],[2307419.9411,6233002.1087],[2292275.481,6232934.2344],[2277131.5775,6232839.3463],[2261988.1192,6232717.4454],[2246845.4402,6232568.1952],[2231703.4291,6232392.1035],[2216562.4199,6232188.6656],[2201422.4126,6231958.2211],[2186283.741,6231700.7722]]]]},"geometry_name":"the_geom","properties":{"GRID1MIL":"34U","GRID100K":"DV","LONGITUDE":20.307416,"LATITUDE":49.198764},"bbox":[2183512.9989,6231700.7722,2337709.3067,6386318.442]}],"totalFeatures":"unknown","numberReturned":1,"timeStamp":"2022-06-01T13:19:28.257Z","crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::3857"}},"bbox":[2183512.9989,6231700.7722,2337709.3067,6386318.442]}'  # noqa


def get_attribute_mock(self, name: str, namespace_uri: str = None):
    return 'text/xml'


def get_attribute_mock_feature(self, name: str, namespace_uri: str = None):
    return 'application/json'


def get_impl_mock(self, impl: type, **kwargs):
    return io.BytesIO(stream_wms)


def get_impl_mock_feature(self, impl: type, **kwargs):
    return io.BytesIO(stream_features)


def get_json_node(self, node):
    if isinstance(node, JsonNode):
        return node
    return JsonBaseNode(node, node.get_impl(io.BufferedIOBase))


class TestWMS(unittest.TestCase):

    def test_namespace(self):
        service_w_sample = WmsServiceNode('https+wms://w_sample_x')

        self.assertEqual(service_w_sample.namespace_uri, 'WMS')

    def test_type_service(self):
        service_w_sample = WmsServiceNode('https+wms://w_sample_x')

        self.assertEqual(service_w_sample.type_service, 'WMS')

    def test_name(self):
        service_w_sample = WmsServiceNode('https+wms://w_sample_x')

        self.assertEqual(service_w_sample.name, 'https://w_sample_x')

    def test_impl(self):
        with mock.patch.object(
                WXSNodeOperation,
                '_get_content_type',
                new=get_attribute_mock), \
                mock.patch.object(DrbHttpNode,
                                  'get_impl',
                                  new=get_impl_mock):

            service_w_sample = WmsServiceNode('https+wms://w_sample_x')

            self.assertTrue(service_w_sample.has_child('GetMap'))

            self.assertIsInstance(service_w_sample['GetMap'], WXSNodeOperation)

            self.assertTrue(service_w_sample.has_child('Layer'))

            self.assertIsInstance(service_w_sample['Layer'], XmlNode)

            service_w_sample.close()

    def test_operation(self):
        with mock.patch.object(WXSNodeOperation, '_get_content_type',
                               new=get_attribute_mock), mock.patch.object(
                DrbHttpNode, 'get_impl', new=get_impl_mock):
            service_w_sample = WmsServiceNode('https+wms://w_sample_x')

            operation = service_w_sample['GetFeatureInfo']

            self.assertFalse(operation.has_impl(io.BytesIO))
            self.assertIsNone(operation.value)

            with self.assertRaises(DrbNotImplementationException):
                self.assertIsNone(operation.get_impl(io.BytesIO))

            with mock.patch.object(
                    WXSNodeOperation,
                    '_get_content_type',
                    new=get_attribute_mock_feature), \
                    mock.patch.object(DrbHttpNode, 'get_impl',
                                      new=get_impl_mock_feature),  \
                    mock.patch.object(_DrbFactoryResolver, 'create',
                                      new=get_json_node):
                dict_request = {'param1': 'charlie'}

                feature = operation[dict_request]

                self.assertIsInstance(feature, JsonBaseNode)
                self.assertIsInstance(feature[0]['type'], JsonNode)

                self.assertEqual(feature[0]['type'].value, 'FeatureCollection')

    def test_url_service(self):
        with mock.patch.object(WXSNodeOperation,
                               '_get_content_type',
                               new=get_attribute_mock), \
                mock.patch.object(DrbHttpNode,
                                  'get_impl',
                                  new=get_impl_mock):
            service_w_sample = WmsServiceNode('https+wms://w_sample_x',
                                              service_number='v1')

            self.assertEqual(service_w_sample.url_service('GetMap'),
                             'https://w_sample_x?'
                             'request=GetMap&service=WMS&'
                             'service_number=v1')

    def test_get_map(self):
        with mock.patch.object(
                WXSNodeOperation,
                '_get_content_type',
                new=get_attribute_mock), \
                mock.patch.object(DrbHttpNode, 'get_impl', new=get_impl_mock):
            service_w_sample = WmsServiceNode('https+wms://w_sample_x')

            operation = service_w_sample['GetMap']

            self.assertFalse(operation.has_impl(io.BytesIO))
            self.assertIsNone(operation.value)

            with self.assertRaises(DrbNotImplementationException):
                self.assertIsNone(operation.get_impl(io.BytesIO))

            with mock.patch.object(
                    WXSNodeOperation,
                    '_get_content_type',
                    new=get_attribute_mock_feature), \
                    mock.patch.object(DrbHttpNode, 'get_impl',
                                      new=get_impl_mock_feature), \
                    mock.patch.object(_DrbFactoryResolver, 'create',
                                      new=get_json_node):

                predicate = WmsGetMapPredicate('mgrs_region',
                                               bbox='7514065.628545968,'
                                                    '7514065.628545967,'
                                                    '10018754.171394622,'
                                                    '10018754.171394628',
                                               width=256,
                                               height=128)

                feature = operation[predicate]

                self.assertIsInstance(feature, JsonBaseNode)
                self.assertIsInstance(feature[0]['type'], JsonNode)

                self.assertEqual(feature[0]['type'].value,
                                 'FeatureCollection')

    def test_get_feature_info(self):
        with mock.patch.object(WXSNodeOperation, '_get_content_type',
                               new=get_attribute_mock), \
                mock.patch.object(DrbHttpNode, 'get_impl', new=get_impl_mock):
            service_w_sample = WmsServiceNode('https+wms://w_sample_x')

            operation = service_w_sample['GetFeatureInfo']

            self.assertFalse(operation.has_impl(io.BytesIO))
            self.assertIsNone(operation.value)

            with self.assertRaises(DrbNotImplementationException):
                self.assertIsNone(operation.get_impl(io.BytesIO))

            with mock.patch.object(
                    WXSNodeOperation,
                    '_get_content_type',
                    new=get_attribute_mock_feature), \
                    mock.patch.object(DrbHttpNode, 'get_impl',
                                      new=get_impl_mock_feature), \
                    mock.patch.object(_DrbFactoryResolver, 'create',
                                      new=get_json_node):
                predicate = WmsGetFeatureInfoPredicate(
                    query_layers='mgrs_region',
                    bbox='7514065.628545968,'
                         '7514065.628545967,'
                         '10018754.171394622,'
                         '10018754.171394628',
                    width=256,
                    height=128,
                    i=5,
                    j=21)

                feature = operation[predicate]

                self.assertIsInstance(feature, JsonBaseNode)
                self.assertIsInstance(feature[0]['type'], JsonNode)

                self.assertEqual(feature[0]['type'].value,
                                 'FeatureCollection')
