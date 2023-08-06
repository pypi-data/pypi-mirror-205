import io
import unittest
from unittest import mock

from drb.drivers.http import DrbHttpNode
from drb.drivers.wxs import WXSNodeOperation
from drb.nodes.logical_node import DrbLogicalNode

from drb.drivers.wcs import WcsFactory, WcsServiceNode

stream_wcs = b'<?xml version="1.0" encoding="UTF-8"?>\n<wcs:Capabilities xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xsi:schemaLocation="http://www.opengis.net/wcs/2.0 http://schemas.opengis.net/wcs/2.0/wcsAll.xsd " version="2.0.1">\n  <ows:ServiceIdentification>\n    <ows:Title>SoilGrids250m 2.0 - Nitrogen</ows:Title>\n    <ows:Abstract>Nitrogen in cg/kg at 6 standard depths predicted using the global compilation of soil ground observations. To visualize these layers please use www.soilgrids.org.</ows:Abstract>\n    <ows:Keywords>\n      <ows:Keyword>nitrogen</ows:Keyword>\n      <ows:Keyword>digital soil mapping</ows:Keyword>\n      <ows:Keyword>nutrients</ows:Keyword>\n      <ows:Keyword>Soil science</ows:Keyword>\n      <ows:Keyword>Global</ows:Keyword>\n      <ows:Keyword>geoscientificInformation</ows:Keyword>\n    </ows:Keywords>\n    <ows:ServiceType codeSpace="OGC">OGC WCS</ows:ServiceType>\n    <ows:ServiceTypeVersion>2.0.1</ows:ServiceTypeVersion>\n    <ows:ServiceTypeVersion>1.1.1</ows:ServiceTypeVersion>\n    <ows:ServiceTypeVersion>1.0.0</ows:ServiceTypeVersion>\n    <ows:Profile>http://www.opengis.net/spec/WCS/2.0/conf/core</ows:Profile>\n       <ows:AccessConstraints>None</ows:AccessConstraints>\n  </ows:ServiceIdentification>\n  <ows:ServiceProvider>\n    <ows:ProviderName>ISRIC - World Soil Reference</ows:ProviderName>\n    <ows:ProviderSite xlink:type="simple" xlink:href="https://maps.isric.org/"/>\n    </ows:ServiceProvider>\n  <ows:OperationsMetadata>\n    <ows:Operation name="GetCapabilities">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;"/>\n          <ows:Post xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;">\n            <ows:Constraint name="PostEncoding">\n              <ows:AllowedValues>\n                <ows:Value>XML</ows:Value>\n              </ows:AllowedValues>\n            </ows:Constraint>\n          </ows:Post>\n        </ows:HTTP>\n      </ows:DCP>\n    </ows:Operation>\n    <ows:Operation name="DescribeCoverage">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;"/>\n          <ows:Post xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;">\n            <ows:Constraint name="PostEncoding">\n              <ows:AllowedValues>\n                <ows:Value>XML</ows:Value>\n              </ows:AllowedValues>\n            </ows:Constraint>\n          </ows:Post>\n        </ows:HTTP>\n      </ows:DCP>\n    </ows:Operation>\n    <ows:Operation name="GetCoverage">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;"/>\n          <ows:Post xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;">\n            <ows:Constraint name="PostEncoding">\n              <ows:AllowedValues>\n                <ows:Value>XML</ows:Value>\n              </ows:AllowedValues>\n            </ows:Constraint>\n          </ows:Post>\n        </ows:HTTP>\n      </ows:DCP>\n    </ows:Operation>\n  </ows:OperationsMetadata>\n  <wcs:ServiceMetadata>\n    <wcs:formatSupported>image/tiff</wcs:formatSupported>\n    <wcs:formatSupported>image/png</wcs:formatSupported>\n    <wcs:formatSupported>image/jpeg</wcs:formatSupported>\n    <wcs:formatSupported>image/png; mode=8bit</wcs:formatSupported>\n    <wcs:formatSupported>image/vnd.jpeg-png</wcs:formatSupported>\n    <wcs:formatSupported>image/vnd.jpeg-png8</wcs:formatSupported>\n    <wcs:Extension>\n      <int:InterpolationMetadata>\n        <int:InterpolationSupported>NEAREST</int:InterpolationSupported>\n        <int:InterpolationSupported>AVERAGE</int:InterpolationSupported>\n        <int:InterpolationSupported>BILINEAR</int:InterpolationSupported>\n      </int:InterpolationMetadata>\n          </wcs:Extension>\n  </wcs:ServiceMetadata>\n  <wcs:Contents>\n    <wcs:CoverageSummary>\n      <wcs:CoverageId>nitrogen_0-5cm_Q0.05</wcs:CoverageId>\n      <wcs:CoverageSubtype>RectifiedGridCoverage</wcs:CoverageSubtype>\n    </wcs:CoverageSummary>\n  </wcs:Contents>\n</wcs:Capabilities>\n'  # noqa


def get_attribute_mock(self, name: str, namespace_uri: str = None):
    return 'text/xml'


def get_impl_mock(self, impl: type, **kwargs):
    return io.BytesIO(stream_wcs)


class TestWcsFactory(unittest.TestCase):
    svc_url = 'https://wcs.test.com'

    def test_create(self):
        with mock.patch.object(
                WXSNodeOperation,
                '_get_content_type',
                new=get_attribute_mock), \
                mock.patch.object(
                    DrbHttpNode,
                    'get_impl',
                    new=get_impl_mock):
            factory = WcsFactory()

            node = factory.create(self.svc_url)
            self.assertIsNotNone(node)
            self.assertIsInstance(node, WcsServiceNode)

    def test_create_logical_node(self):
        with mock.patch.object(
                WXSNodeOperation,
                '_get_content_type',
                new=get_attribute_mock), \
                mock.patch.object(
                    DrbHttpNode,
                    'get_impl',
                    new=get_impl_mock):
            factory = WcsFactory()

            node = factory.create(DrbLogicalNode(self.svc_url))
            self.assertIsNotNone(node)
            self.assertIsInstance(node, WcsServiceNode)
