from __future__ import annotations

from drb.core import Predicate, DrbFactory, DrbNode
from drb.drivers.http import DrbHttpNode
from drb.drivers.wxs import WXSServiceNode, WXSNodeOperation
from drb.exceptions.core import DrbFactoryException
from requests.auth import AuthBase


class WcsServiceNode(WXSServiceNode):
    def __init__(self, url: str, auth: AuthBase = None, **kwargs):
        if kwargs is not None and len(kwargs) > 0:
            super(WcsServiceNode, self).__init__(url, auth=auth, **kwargs)
        else:
            super(WcsServiceNode, self).__init__(url, auth)
        self._service_url = url.replace('+wcs', '') \
            if '+wcs' in url else url
        self.namespace_uri = 'WCS'
        self.name = self._service_url

    @property
    def type_service(self):
        return 'WCS'

    def manage_predefined_operations_metadata(self, name, request_cap, attr):
        operation = None
        if name == 'GetCoverage':
            operation = WcsNodeOperationGetCoverage(
                self,
                name=name,
                namespace=request_cap.namespace_uri,
                attributes=attr,
                version=self._version)
        elif name == 'DescribeCoverage':
            operation = WcsNodeOperationDescribeCoverage(
                self,
                name=name,
                namespace=request_cap.namespace_uri,
                attributes=attr,
                version=self._version)
        return operation

    def read_capabilities(self, xmlnode_tree):
        super().read_capabilities(xmlnode_tree)


class WcsDescribeCoveragePredicate(Predicate):

    def __init__(self, coverage_id, **kwargs):
        self._coverage_id = coverage_id
        self.others = dict(**kwargs)

    def to_dict(self, version):
        arg_dict = {}

        # If the predicate force a specific version
        if 'version' in self.others.keys():
            version = self.others['version']

        if version[0] >= '2':
            arg_dict['coverageId'] = self._coverage_id
        else:
            arg_dict['coverage'] = self._coverage_id

        arg_dict.update(self.others)

        return arg_dict

    def matches(self, key) -> bool:
        return False


class WcsGetCoveragePredicate(WcsDescribeCoveragePredicate):

    def __init__(self, coverage_id, **kwargs):
        super().__init__(coverage_id, **kwargs)


class WcsNodeOperationGetCoverage(WXSNodeOperation):

    def __getitem__(self, item):
        if isinstance(item, WcsGetCoveragePredicate):
            return self._get_child(item.to_dict(self._version))

        return self._get_child(item)


class WcsNodeOperationDescribeCoverage(WXSNodeOperation):

    def __getitem__(self, item):
        if isinstance(item, WcsDescribeCoveragePredicate):
            return self._get_child(item.to_dict(self._version))

        return self._get_child(item)


class WcsFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, WcsServiceNode):
            return node
        if isinstance(node, DrbHttpNode):
            node_wcs_service = WcsServiceNode(
                url=node.path.original_path,
                auth=node.auth)
        else:
            node_wcs_service = WcsServiceNode(
                url=node.path.original_path)
        try:
            node_wcs_service.children
        except Exception as err:
            final_url = node.path.name.replace('+wcs', '')
            raise DrbFactoryException(f'Unsupported Wcs service: {final_url}')
        return node_wcs_service
