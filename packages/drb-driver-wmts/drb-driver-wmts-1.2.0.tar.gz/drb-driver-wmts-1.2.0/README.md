# WMTS driver
The web map tile service driver extends abstracts WxS driver with the getTile feature.

# Nodes
### WmtsServiceNode
Represents the WMTS service. This node has no attribute and
has as children WmtsOperationNode like GetTile.
Others children give information about the service like layers, and are XmlNode.
Those children are filled in by the information returned from 
the service's GetCapabilities request.

### WmtsOperationNode

Represents an operation than can mde on the service.
For WMTS service, the mandatory operation are GetTile, GetCapabilities, and 
GetFeatureInfo.
Optional operations may be provided by the service 
and indicated in the possibilities thereof. 
Those optional operations are also represented as WmtsOperationNode.

For perform an operation (mandatory or optional), you can use the operator '[]' with a dict that contains 
the parameters of the request.

Example:
```
dict_request = {'layers': 'mgrs_region', 'format': 'image/png', 'height': 256, 'width': 256, 'crs': 'EPSG:3857', 'bbox': '7514065.628545968,7514065.628545967,10018754.171394622,10018754.171394628'}


get_map = service_wmts['GetTile'][dict_request]
```

For mandatory operations GetTile and GetFeatureInfo you can
alternatively use Predicate WmtsGetTilePredicate and WmtsGetFeatureInfoPredicate.

Specific class define WXSNodeOperationGetTile and WXSNodeOperationGetFeatureInfo 
for accept respectively WmtsGetTilePredicate WmtsGetFeatureInfoPredicate.

Example:
```
predicate = WmtsGetTilePredicate(layer='ORTHOIMAGERY.ORTHOPHOTOS',
                                 tile_matrix_set='PM',
                                 tile_matrix=14, tile_col=8180, tile_row=5905,
                                 style='normal')

get_map = service_wmts['GetTile'][predicate]
```

# Installation
```
pip install drb-driver-wmts
```
# Examples

```python
from drb.drivers.wmts import WmtsServiceNode, WmtsGetTilePredicate

url_wmts='https+wmts://geoserver.swarm.ops.internal.gael.fr/geoserver/demo/wmts?'

service_wmts = WmtsServiceNode(url_wmts)

list_cap = service_wmts.children

print('----------------------------------------')
print('list_cap')

print(list_cap)

for child in service_wmts:
    print(child)
    print(child.name)

#=>  <drb_driver_wXs.wXs_node.WXSNodeOperation object at 0x7f5403865d90>
#=>  GetCapabilities
#=>  <drb_driver_wmts.wmts_nodes.WmtsNodeOperationGetTile object at 0x7f54047b4700>
#=>  GetTile
#=>  <drb_driver_wmts.wmts_nodes.WmtsNodeOperationGetFeatureInfo object at 0x7f54047b4460>
#=>  GetFeatureInfo
#=>  <drb_driver_xml.xml_node.XmlNode object at 0x7f5402914c70>
#=>  Contents

    
get_map = service_wmts['GetTile']


dict_request = {'layer': 'ORTHOIMAGERY.ORTHOPHOTOS', 'format': 'image/jpeg', 'TILEMATRIXSET': 'PM', 'TILEMATRIX': 14, 'TILECOL': 8180, 'TILEROW': '5905', 'style': 'normal'}


tile_res = service_wmts['GetTile'][dict_request]

print('----------------------------------------')
print('GetTile : with parameter return image')
print(tile_res)
#=>  <drb_driver_image.image_node_factory.DrbImageBaseNode object at 0x7fc2cb23efa0>


predicate = WmtsGetTilePredicate(layer='ORTHOIMAGERY.ORTHOPHOTOS',
                                 tile_matrix_set='PM',
                                 tile_matrix=14, tile_col=8180, tile_row=5905,
                                 style='normal')


print('----------------------------------------')
print('GetTile : with parameter return image')
print(tile_res)
#=>  <drb_driver_image.image_node_factory.DrbImageBaseNode object at 0x7f54047b4970>

```



