import io
import unittest
from unittest import mock

from drb.drivers.http import DrbHttpNode
from drb.drivers.wxs import WXSNodeOperation
from drb.drivers.xml import XmlBaseNode, XmlNode
from drb.exceptions.core import DrbNotImplementationException
from drb.topics.resolver import _DrbFactoryResolver

from drb.drivers.wcs import WcsServiceNode, WcsDescribeCoveragePredicate,\
    WcsGetCoveragePredicate

stream_wcs = b'<?xml version="1.0" encoding="UTF-8"?>\n<wcs:Capabilities xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:crs="http://www.opengis.net/wcs/crs/1.0" xmlns:int="http://www.opengis.net/wcs/interpolation/1.0" xsi:schemaLocation="http://www.opengis.net/wcs/2.0 http://schemas.opengis.net/wcs/2.0/wcsAll.xsd " version="2.0.1">\n  <ows:ServiceIdentification>\n    <ows:Title>SoilGrids250m 2.0 - Nitrogen</ows:Title>\n    <ows:Abstract>Nitrogen in cg/kg at 6 standard depths predicted using the global compilation of soil ground observations. To visualize these layers please use www.soilgrids.org.</ows:Abstract>\n    <ows:Keywords>\n      <ows:Keyword>nitrogen</ows:Keyword>\n      <ows:Keyword>digital soil mapping</ows:Keyword>\n      <ows:Keyword>nutrients</ows:Keyword>\n      <ows:Keyword>Soil science</ows:Keyword>\n      <ows:Keyword>Global</ows:Keyword>\n      <ows:Keyword>geoscientificInformation</ows:Keyword>\n    </ows:Keywords>\n    <ows:ServiceType codeSpace="OGC">OGC WCS</ows:ServiceType>\n   <ows:ServiceTypeVersion>1.0.0</ows:ServiceTypeVersion> <ows:ServiceTypeVersion>1.0.1</ows:ServiceTypeVersion> <ows:ServiceTypeVersion>1.1.1</ows:ServiceTypeVersion>  <ows:ServiceTypeVersion>2.0.1</ows:ServiceTypeVersion>\n    \n    \n    <ows:Profile>http://www.opengis.net/spec/WCS/2.0/conf/core</ows:Profile>\n       <ows:AccessConstraints>None</ows:AccessConstraints>\n  </ows:ServiceIdentification>\n  <ows:ServiceProvider>\n    <ows:ProviderName>ISRIC - World Soil Reference</ows:ProviderName>\n    <ows:ProviderSite xlink:type="simple" xlink:href="https://maps.isric.org/"/>\n    </ows:ServiceProvider>\n  <ows:OperationsMetadata>\n    <ows:Operation name="GetCapabilities">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;"/>\n          <ows:Post xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;">\n            <ows:Constraint name="PostEncoding">\n              <ows:AllowedValues>\n                <ows:Value>XML</ows:Value>\n              </ows:AllowedValues>\n            </ows:Constraint>\n          </ows:Post>\n        </ows:HTTP>\n      </ows:DCP>\n    </ows:Operation>\n    <ows:Operation name="DescribeCoverage">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;"/>\n          <ows:Post xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;">\n            <ows:Constraint name="PostEncoding">\n              <ows:AllowedValues>\n                <ows:Value>XML</ows:Value>\n              </ows:AllowedValues>\n            </ows:Constraint>\n          </ows:Post>\n        </ows:HTTP>\n      </ows:DCP>\n    </ows:Operation>\n    <ows:Operation name="GetCoverage">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;"/>\n          <ows:Post xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/nitrogen.map&amp;amp;">\n            <ows:Constraint name="PostEncoding">\n              <ows:AllowedValues>\n                <ows:Value>XML</ows:Value>\n              </ows:AllowedValues>\n            </ows:Constraint>\n          </ows:Post>\n        </ows:HTTP>\n      </ows:DCP>\n    </ows:Operation>\n  </ows:OperationsMetadata>\n  <wcs:ServiceMetadata>\n    <wcs:formatSupported>image/tiff</wcs:formatSupported>\n    <wcs:formatSupported>image/png</wcs:formatSupported>\n    <wcs:formatSupported>image/jpeg</wcs:formatSupported>\n    <wcs:formatSupported>image/png; mode=8bit</wcs:formatSupported>\n    <wcs:formatSupported>image/vnd.jpeg-png</wcs:formatSupported>\n    <wcs:formatSupported>image/vnd.jpeg-png8</wcs:formatSupported>\n    <wcs:Extension>\n      <int:InterpolationMetadata>\n        <int:InterpolationSupported>NEAREST</int:InterpolationSupported>\n        <int:InterpolationSupported>AVERAGE</int:InterpolationSupported>\n        <int:InterpolationSupported>BILINEAR</int:InterpolationSupported>\n      </int:InterpolationMetadata>\n          </wcs:Extension>\n  </wcs:ServiceMetadata>\n  <wcs:Contents>\n    <wcs:CoverageSummary>\n      <wcs:CoverageId>nitrogen_0-5cm_Q0.05</wcs:CoverageId>\n      <wcs:CoverageSubtype>RectifiedGridCoverage</wcs:CoverageSubtype>\n    </wcs:CoverageSummary>\n  </wcs:Contents>\n</wcs:Capabilities>\n'  # noqa
stream_wcs_v1 = b'<?xml version="1.0" encoding="ISO-8859-1"?>\n<Capabilities xmlns="http://www.opengis.net/wcs/1.1" xmlns:ows="http://www.opengis.net/ows" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" version="1.1.1">\n  <ows:ServiceIdentification>\n    <ows:Title>Atlas of the Cryosphere: Northern Hemisphere</ows:Title>\n      <ows:Keywords>\n      <ows:Keyword>Snow Water Equivalent</ows:Keyword>\n    </ows:Keywords>\n      <ows:ServiceTypeVersion>1.1.1</ows:ServiceTypeVersion>\n    <ows:Fees>none</ows:Fees>\n    <ows:AccessConstraints>none</ows:AccessConstraints>\n  </ows:ServiceIdentification>\n  <ows:ServiceProvider>\n    <ows:ProviderName>National Snow and Ice Data Center</ows:ProviderName>\n      </ows:ServiceProvider>\n  <ows:OperationsMetadata>\n    <ows:Operation name="GetCapabilities">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="http://nsidc.org/cgi-bin/atlas_north?"/>\n        </ows:HTTP>\n      </ows:DCP>\n      <ows:Parameter name="service">\n        <ows:Value>WCS</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="version">\n        <ows:Value>1.1.1</ows:Value>\n      </ows:Parameter>\n    </ows:Operation>\n    <ows:Operation name="DescribeCoverage">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="http://nsidc.org/cgi-bin/atlas_north?"/>\n        </ows:HTTP>\n      </ows:DCP>\n      <ows:Parameter name="service">\n        <ows:Value>WCS</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="version">\n        <ows:Value>1.1.1</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="identifiers">\n        <ows:Value>sea_ice_concentration_01</ows:Value>\n        <ows:Value>sea_ice_concentration_02</ows:Value>\n        <ows:Value>sea_ice_concentration_03</ows:Value>\n        <ows:Value>sea_ice_concentration_04</ows:Value>\n         <ows:Value>greenland_elevation</ows:Value>\n      </ows:Parameter>\n    </ows:Operation>\n    <ows:Operation name="GetCoverage">\n      <ows:DCP>\n        <ows:HTTP>\n          <ows:Get xlink:type="simple" xlink:href="http://nsidc.org/cgi-bin/atlas_north?"/>\n        </ows:HTTP>\n      </ows:DCP>\n      <ows:Parameter name="service">\n        <ows:Value>WCS</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="version">\n        <ows:Value>1.1.1</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="Identifier">\n        <ows:Value>sea_ice_concentration_01</ows:Value>\n        <ows:Value>sea_ice_concentration_02</ows:Value>\n        <ows:Value>sea_ice_concentration_03</ows:Value>\n          <ows:Value>greenland_ice_thickness</ows:Value>\n        <ows:Value>greenland_elevation</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="InterpolationType">\n        <ows:Value>NEAREST_NEIGHBOUR</ows:Value>\n        <ows:Value>BILINEAR</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="format">\n        <ows:Value>image/png</ows:Value>\n        <ows:Value>image/tiff</ows:Value>\n        <ows:Value>image/gif</ows:Value>\n        <ows:Value>image/png; mode=24bit</ows:Value>\n        <ows:Value>image/jpeg</ows:Value>\n        <ows:Value>image/vnd.wap.wbmp</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="store">\n        <ows:Value>false</ows:Value>\n      </ows:Parameter>\n      <ows:Parameter name="GridBaseCRS">\n        <ows:Value>urn:ogc:def:crs:epsg::4326</ows:Value>\n      </ows:Parameter>\n    </ows:Operation>\n  </ows:OperationsMetadata>\n  <Contents>\n    <CoverageSummary>\n      </CoverageSummary>\n  </Contents>\n</Capabilities>'  # noqa
stream_describes = b'<?xml version="1.0" encoding="UTF-8"?>\n<wcs:CoverageDescriptions xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:ows="http://www.opengis.net/ows/2.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:swe="http://www.opengis.net/swe/2.0" xsi:schemaLocation="http://www.opengis.net/wcs/2.0 http://schemas.opengis.net/wcs/2.0/wcsAll.xsd ">\n  <wcs:CoverageDescription gml:id="nitrogen_5-15cm_Q0.5">\n    <gml:boundedBy>\n      <gml:Envelope srsName="http://www.opengis.net/def/crs/EPSG/0/152160" axisLabels="x y" uomLabels="m m" srsDimension="2">\n        <gml:lowerCorner>-19949750 -6147500</gml:lowerCorner>\n        <gml:upperCorner>19861750 8361000</gml:upperCorner>\n      </gml:Envelope>\n    </gml:boundedBy>\n    <wcs:CoverageId>nitrogen_5-15cm_Q0.5</wcs:CoverageId>\n    <gml:domainSet>\n      <gml:RectifiedGrid dimension="2" gml:id="grid_nitrogen_5-15cm_Q0.5">\n        <gml:limits>\n          <gml:GridEnvelope>\n            <gml:low>0 0</gml:low>\n            <gml:high>159245 58033</gml:high>\n          </gml:GridEnvelope>\n        </gml:limits>\n        <gml:axisLabels>x y</gml:axisLabels>\n        <gml:origin>\n          <gml:Point gml:id="grid_origin_nitrogen_5-15cm_Q0.5" srsName="http://www.opengis.net/def/crs/EPSG/0/152160">\n            <gml:pos>-19949625.000000 8360875.000000</gml:pos>\n          </gml:Point>\n        </gml:origin>\n        <gml:offsetVector srsName="http://www.opengis.net/def/crs/EPSG/0/152160">250.000000 0</gml:offsetVector>\n        <gml:offsetVector srsName="http://www.opengis.net/def/crs/EPSG/0/152160">0 -250.000000</gml:offsetVector>\n      </gml:RectifiedGrid>\n    </gml:domainSet>\n    <gmlcov:rangeType>\n      <swe:DataRecord>\n        <swe:field name="band1">\n          <swe:Quantity>\n            <swe:nilValues/>\n            <swe:uom code="W.m-2.Sr-1"/>\n            <swe:constraint>\n              <swe:AllowedValues>\n                <swe:interval>0 65535</swe:interval>\n                <swe:significantFigures>5</swe:significantFigures>\n              </swe:AllowedValues>\n            </swe:constraint>\n          </swe:Quantity>\n        </swe:field>\n      </swe:DataRecord>\n    </gmlcov:rangeType>\n    <wcs:ServiceParameters>\n      <wcs:CoverageSubtype>RectifiedGridCoverage</wcs:CoverageSubtype>\n      <wcs:nativeFormat/>\n    </wcs:ServiceParameters>\n  </wcs:CoverageDescription>\n</wcs:CoverageDescriptions>\n'  # noqa
stream_describes_v1 = b'<?xml version="1.0" encoding="ISO-8859-1"?>\n<CoverageDescriptions xmlns="http://www.opengis.net/wcs/1.1" xmlns:ows="http://www.opengis.net/ows" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" version="1.1.1">\n  <CoverageDescription>\n     <Identifier>greenland_accumulation</Identifier>\n    <ows:Keywords>\n      <ows:Keyword>Cryosphere</ows:Keyword>\n      <ows:Keyword>Earth Science</ows:Keyword>\n       </ows:Keywords>\n    <Range>\n      <Field>\n        <ows:Title>snow water equivalent (SWE) (g cm^-2 yr^-1)</ows:Title>\n        <Identifier>pixels</Identifier>\n        <InterpolationMethods>\n          <DefaultMethod>nearest neighbor</DefaultMethod>\n          <OtherMethod>bilinear</OtherMethod>\n        </InterpolationMethods>\n        <Axis identifier="bands">\n          <AvailableKeys>\n            <Key>1</Key>\n          </AvailableKeys>\n        </Axis>\n      </Field>\n    </Range>\n    <SupportedCRS>urn:ogc:def:crs:EPSG::32661</SupportedCRS>\n    <SupportedCRS>urn:ogc:def:crs:EPSG::4326</SupportedCRS>\n   <SupportedFormat>image/tiff</SupportedFormat>\n  </CoverageDescription>\n</CoverageDescriptions>\n'  # noqa


def get_attribute_mock(self, name: str, namespace_uri: str = None):
    return 'text/xml'


def get_attribute_mock_feature(self, name: str, namespace_uri: str = None):
    return 'application/json'


def get_impl_mock(self, impl: type, **kwargs):
    return io.BytesIO(stream_wcs)


def get_impl_mock_v1(self, impl: type, **kwargs):
    return io.BytesIO(stream_wcs_v1)


def get_impl_mock_feature(self, impl: type, **kwargs):
    return io.BytesIO(stream_describes)


def get_impl_mock_feature_v1(self, impl: type, **kwargs):
    return io.BytesIO(stream_describes_v1)


def get_xml_node(self, node):
    if isinstance(node, XmlNode):
        return node
    return XmlBaseNode(node, node.get_impl(io.BytesIO))


class TestWCS(unittest.TestCase):

    def test_namespace(self):
        service_w_sample = WcsServiceNode('https+wcs://w_sample_x')

        self.assertEqual(service_w_sample.namespace_uri, 'WCS')

    def test_type_service(self):
        service_w_sample = WcsServiceNode('https+wcs://w_sample_x')

        self.assertEqual(service_w_sample.type_service, 'WCS')

    def test_name(self):
        service_w_sample = WcsServiceNode('https+wcs://w_sample_x')

        self.assertEqual(service_w_sample.name, 'https://w_sample_x')

    def test_impl(self):
        with mock.patch.object(
                WXSNodeOperation,
                '_get_content_type',
                new=get_attribute_mock), \
                mock.patch.object(DrbHttpNode,
                                  'get_impl',
                                  new=get_impl_mock):

            service_w_sample = WcsServiceNode('https+wcs://w_sample_x')

            self.assertTrue(service_w_sample.has_child('GetCoverage'))

            self.assertIsInstance(service_w_sample['GetCoverage'],
                                  WXSNodeOperation)

            self.assertTrue(service_w_sample.has_child('Contents'))

            self.assertIsInstance(service_w_sample['Contents'], XmlNode)

            service_w_sample.close()

    def test_operation(self):
        with mock.patch.object(WXSNodeOperation, '_get_content_type',
                               new=get_attribute_mock), mock.patch.object(
                DrbHttpNode, 'get_impl', new=get_impl_mock):
            service_w_sample = WcsServiceNode('https+wcs://w_sample_x')

            operation = service_w_sample['DescribeCoverage']

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
                                      new=get_xml_node):
                dict_request = {'param1': 'charlie'}

                feature = operation[dict_request]

                self.assertIsInstance(feature, XmlBaseNode)
                self.assertIsInstance(feature['CoverageDescriptions'], XmlNode)
                cover_child = \
                    feature['CoverageDescriptions']['CoverageDescription']
                self.assertEqual(cover_child['CoverageId'].value,
                                 'nitrogen_5-15cm_Q0.5')

                self.assertTrue(cover_child.has_child('domainSet'))

    def test_operation_v1(self):
        with mock.patch.object(WXSNodeOperation, '_get_content_type',
                               new=get_attribute_mock), mock.patch.object(
                DrbHttpNode, 'get_impl', new=get_impl_mock_v1):
            service_w_sample = WcsServiceNode('https+wcs://w_sample_x')

            operation = service_w_sample['DescribeCoverage']

            self.assertFalse(operation.has_impl(io.BytesIO))
            self.assertIsNone(operation.value)

            with self.assertRaises(DrbNotImplementationException):
                self.assertIsNone(operation.get_impl(io.BytesIO))

            with mock.patch.object(
                    WXSNodeOperation,
                    '_get_content_type',
                    new=get_attribute_mock_feature), \
                    mock.patch.object(DrbHttpNode, 'get_impl',
                                      new=get_impl_mock_feature_v1),  \
                    mock.patch.object(_DrbFactoryResolver, 'create',
                                      new=get_xml_node):
                predicate = WcsDescribeCoveragePredicate(
                    coverage_id='greenland_accumulation')
                feature = operation[predicate]

                self.assertIsInstance(feature, XmlBaseNode)
                self.assertIsInstance(feature['CoverageDescriptions'], XmlNode)
                cover_child = \
                    feature['CoverageDescriptions']['CoverageDescription']
                self.assertEqual(cover_child['Identifier'].value,
                                 'greenland_accumulation')

                self.assertTrue(cover_child.has_child('SupportedFormat'))

    def test_get_coverage(self):
        with mock.patch.object(
                WXSNodeOperation, '_get_content_type',
                new=get_attribute_mock), \
                mock.patch.object(DrbHttpNode, 'get_impl', new=get_impl_mock):
            service_w_sample = WcsServiceNode('https+wcs://w_sample_x')

            operation = service_w_sample['GetCoverage']

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
                                      new=get_xml_node):

                predicate = WcsGetCoveragePredicate(
                    coverage_id='nitrogen_5-15cm_Q0.5',
                    format='GEOTIFF_INT16')

                feature = operation[predicate]

                self.assertIsInstance(feature, XmlBaseNode)

    def test_describe_coverage_info(self):
        with mock.patch.object(WXSNodeOperation,
                               '_get_content_type',
                               new=get_attribute_mock), \
                mock.patch.object(DrbHttpNode, 'get_impl', new=get_impl_mock):
            service_w_sample = WcsServiceNode('https+wcs://w_sample_x')

            operation = service_w_sample['DescribeCoverage']

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
                                      new=get_xml_node):
                predicate = WcsDescribeCoveragePredicate(
                    coverage_id='nitrogen_5-15cm_Q0.5')

                feature = operation[predicate]

                self.assertIsInstance(feature, XmlBaseNode)
                self.assertIsInstance(feature['CoverageDescriptions'], XmlNode)
                cover_child = \
                    feature['CoverageDescriptions']['CoverageDescription']
                self.assertEqual(cover_child['CoverageId'].value,
                                 'nitrogen_5-15cm_Q0.5')

                self.assertTrue(cover_child.has_child('domainSet'))

    def test_url_service(self):
        with mock.patch.object(WXSNodeOperation,
                               '_get_content_type',
                               new=get_attribute_mock), \
                mock.patch.object(DrbHttpNode,
                                  'get_impl',
                                  new=get_impl_mock):
            service_w_sample = WcsServiceNode('https+wcs://w_sample_x',
                                              service_number='v1')

            self.assertEqual(service_w_sample.url_service('GetCoverage'),
                             'https://w_sample_x?'
                             'request=GetCoverage&service=WCS&'
                             'service_number=v1')
