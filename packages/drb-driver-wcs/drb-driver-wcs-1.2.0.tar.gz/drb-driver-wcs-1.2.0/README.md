# WCS driver
The web coverage service driver extends abstracts WxS driver with the GetCoverage feature.


# Nodes
### WcsServiceNode
Represents the WCS service. This node has no attribute and
has as children WcsOperationNode like GetCoverage.
Others children give information about the service like for example 
ServiceMetadata, that could give information about Supported Format inside a XmlNode.
Those children are filled in by the information returned from 
the service's GetCapabilities request.



### WcsOperationNode

Represents an operation than can mde on the service.
For WCS service, the mandatory operation are GetCoverage, GetCapabilities, and 
GetFeatureInfo.
Optional operations may be provided by the service 
and indicated in the possibilities thereof. 
Those optional operations are also represented as WcsOperationNode.

For perform an operation (mandatory or optional), you can use the operator '[]' with a dict that contains 
the parameters of the request.

Example:
```
dict_request = {'COVERAGEID': 'nitrogen_5-15cm_Q0.5'}

describe_coverage = service_wcs['DescribeCoverage'][dict_request]
```

For mandatory operations GetCoverage and DescribeCoverage you can
alternatively use Predicate WcsGetCoveragePredicate and WcsDescribeCoveragePredicate.

Specific class define WcsNodeOperationGetCoverage and WcsNodeOperationDescribeCoverage 
for accept respectively WcsGetCoveragePredicate WcsDescribeCoveragePredicate.

Example:
```
predicate = WcsGetCoveragePredicate(coverage_id='nitrogen_5-15cm_Q0.5', format=}


get_coverage = service_wcs['GetCoverage'][predicate]
```

# Installation
```
pip install drb-driver-wcs
```
# Examples

```python
from drb.drivers.wcs import WcsServiceNode

url_wcs='https+wcs://myserver_wcs/wcs'


service_wcs = WcsServiceNode(url_wcs)

list_cap = service_wcs[:]

print('----------------------------------------')
print('list_cap')

print(list_cap)

for child in service_wcs:
    print(child)
    print(child.name)

# => <drb_driver_wxs.wXs_node.WXSNodeOperation object at 0x7fea3b54ac70>
# => GetCapabilities
# => <drb_driver_wcs.wcs_nodes.WcsNodeOperationDescribeCoverage object at 0x7fea3b5652e0>
# => DescribeCoverage
# => <drb_driver_wcs.wcs_nodes.WcsNodeOperationGetCoverage object at 0x7fea3b5765b0>
# => GetCoverage
# => <drb_driver_xml.xml_node.XmlNode object at 0x7fea3b54aca0>
# => Contents
#     
    
dict_request = {'COVERAGE': 'greenland_accumulation', 'VERSION' : '1.1.1'}

describe = service_wcs['DescribeCoverage'][dict_request]

print('-----------------------------------------------------------------')
print('DescribeCoverage: nitrogen_5...')
print(describe)
print(describe[0].name)
# => <drb_driver_xml.xml_node.XmlNode object at 0x7f7aa91f0be0>
# => CoverageDescription

```


