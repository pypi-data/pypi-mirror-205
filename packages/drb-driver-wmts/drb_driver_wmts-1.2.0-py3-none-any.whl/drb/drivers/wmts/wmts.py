from __future__ import annotations

from drb.core import Predicate, DrbFactory, DrbNode
from drb.drivers.http import DrbHttpNode
from drb.drivers.wxs import WXSServiceNode, WXSNodeOperation
from drb.exceptions.core import DrbFactoryException
from requests.auth import AuthBase


class WmtsServiceNode(WXSServiceNode):
    def __init__(self, url: str, auth: AuthBase = None, **kwargs):
        if kwargs is not None and len(kwargs) > 0:
            super(WmtsServiceNode, self).__init__(url, auth=auth, **kwargs)
        else:
            super(WmtsServiceNode, self).__init__(url, auth)
        self._service_url = url.replace('+wmts', '') \
            if '+wmts' in url else url
        self.namespace_uri = 'WMTS'
        self.name = self._service_url

    @property
    def type_service(self):
        return 'WMTS'

    def manage_predefined_operations_metadata(self, name, request_cap, attr):
        operation = None
        if name == 'GetTile':
            operation = WmtsNodeOperationGetTile(
                self,
                name=name,
                namespace=request_cap.namespace_uri,
                attributes=attr,
                version=self._version)
        elif name == 'GetFeatureInfo':
            operation = WmtsNodeOperationGetFeatureInfo(
                self,
                name=name,
                namespace=request_cap.namespace_uri,
                attributes=attr,
                version=self._version)
        return operation


class WmtsGetTilePredicate(Predicate):

    def __init__(self,
                 layer,
                 tile_matrix_set,
                 tile_matrix,
                 tile_row,
                 tile_col,
                 style='',
                 format='image/jpeg',
                 **kwargs):
        self._layer = layer
        self._tile_matrix = tile_matrix
        self._tile_row = tile_row
        self._tile_col = tile_col

        self._style = style
        self._format = format
        self._tile_matrix_set = tile_matrix_set

        self.others = dict(kwargs)

    def to_dict(self):
        arg_dict = {'layer': self._layer,
                    'style': self._style,
                    'tilematrixset': self._tile_matrix_set,
                    'tilematrix': self._tile_matrix,
                    'tilerow': self._tile_row,
                    'tilecol': self._tile_col,
                    'format': self._format,
                    }
        arg_dict.update(self.others)

        return arg_dict

    def matches(self, key) -> bool:
        return False


class WmtsGetFeatureInfoPredicate(WmtsGetTilePredicate):

    def __init__(self, i, j,
                 info_format,
                 layer,
                 tile_matrix_set,
                 tile_matrix,
                 tile_row,
                 tile_col,
                 style='',
                 format='image/jpeg',
                 **kwargs):
        super().__init__(layer, tile_matrix_set,
                         tile_matrix, tile_row, tile_col,
                         style, format, **kwargs)

        self._info_format = info_format
        self._i = i
        self._j = j

    @classmethod
    def from_WmtsGetTilePredicate(cls,
                                  get_tile_predicate: WmtsGetTilePredicate,
                                  i,
                                  j,
                                  info_format
                                  ):
        return cls(i, j, info_format,
                   layer=get_tile_predicate._layer,
                   tile_matrix_set=get_tile_predicate._tile_matrix_set,
                   tile_matrix=get_tile_predicate._tile_matrix,
                   tile_row=get_tile_predicate._tile_row,
                   tile_col=get_tile_predicate._tile_col,
                   style=get_tile_predicate._style,
                   format=get_tile_predicate._format,
                   **get_tile_predicate.others
                   )

    def to_dict(self):
        arg_dict = {'infoformat': self._info_format,
                    'i': self._i,
                    'j': self._j
                    }
        arg_dict.update(super().to_dict())

        return arg_dict

    def matches(self, key) -> bool:
        return False


class WmtsNodeOperationGetTile(WXSNodeOperation):

    def __getitem__(self, item):
        if isinstance(item, WmtsGetTilePredicate):
            return self._get_child(item.to_dict())

        return self._get_child(item)


class WmtsNodeOperationGetFeatureInfo(WXSNodeOperation):

    def __getitem__(self, item):
        if isinstance(item, WmtsGetFeatureInfoPredicate):
            return self._get_child(item.to_dict())

        return self._get_child(item)


class WmtsFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, WmtsServiceNode):
            return node
        if isinstance(node, DrbHttpNode):
            node_wmts_service = WmtsServiceNode(
                url=node.path.original_path,
                auth=node.auth)
        else:
            node_wmts_service = WmtsServiceNode(node.path.name)
        try:
            node_wmts_service.children
        except Exception as e:
            final_url = node.path.name.replace('+wmts', '')
            raise DrbFactoryException(f'Unsupported Wmts service: {final_url}')
        return node_wmts_service
