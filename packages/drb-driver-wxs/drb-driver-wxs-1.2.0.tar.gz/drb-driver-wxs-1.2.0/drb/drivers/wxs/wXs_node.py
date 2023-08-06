import abc
import io

import keyring
from deprecated.classic import deprecated
from drb.exceptions.core import DrbException, DrbNotImplementationException, \
    DrbFactoryException

from defusedxml import ElementTree

from drb.core import DrbNode
from drb.nodes.abstract_node import AbstractNode
from drb.core.path import ParsedPath
from requests.auth import AuthBase, HTTPBasicAuth
from typing import Any, List, Optional

from drb.topics.resolver import create
from drb.drivers.http import DrbHttpNode
from drb.drivers.xml import XmlNode


class WXSServiceNode(AbstractNode, abc.ABC):
    """
    Common WXsNode interface
    """

    def __init__(self, service_url, auth: AuthBase = None, **kwargs):
        super(AbstractNode, self).__init__()
        self._original_service_url = service_url
        self._service_url = service_url
        self.__auth = auth
        self._children = None
        self.__path = None
        self.__other_key = kwargs
        self._version = None
        self._available_impl.clear()

    def read_capabilities(self, xml_node: DrbNode):
        for key_attr in xml_node.attribute_names():
            if key_attr[0].lower() == 'version':
                self._version = xml_node @ key_attr[0]
        self.read_version_service(xml_node)
        if 'OperationsMetadata' in xml_node:
            self.read_capabilities_operations_metadata(xml_node)

    def read_version_service(self, xmlnode_tree):
        if 'ServiceIdentification' in xmlnode_tree:
            xmlnode = xmlnode_tree['ServiceIdentification']
            if 'ServiceTypeVersion' in xmlnode:
                versions = xmlnode['ServiceTypeVersion', None, :]
                version_max = versions[0].value
                for version_item in versions[1:]:
                    version = version_item.value
                    if version[0] > version_max[0]:
                        version_max = version
                    elif version[0] == version_max[0]:
                        if version[2] > version_max[2]:
                            version_max = version
                        elif version[2] == version_max[2]:
                            if version[4] > version_max[4]:
                                version_max = version
                self._version = version_max

    @abc.abstractmethod
    def manage_predefined_operations_metadata(self, name, request_cap, attr):
        return None

    def read_capabilities_operations_metadata(self, xmlnode_tree):
        for xmlnode in xmlnode_tree.children:

            if xmlnode.name == 'OperationsMetadata':
                for request_cap in xmlnode.children:
                    for child in request_cap.children:
                        if child.name == 'DCP':
                            DCPType = request_cap['DCP']

                    attr = {('DCP', None): DCPType}

                    name = request_cap @ 'name'
                    operation = self.manage_predefined_operations_metadata(
                        name,
                        request_cap,
                        attr)
                    if operation is None:
                        operation = WXSNodeOperation(
                            self,
                            name=name,
                            namespace=request_cap.namespace_uri,
                            attributes=attr,
                            version=self._version)

                    self._children.append(operation)
            else:
                self._children.append(xmlnode)

    def get_auth(self) -> Optional[AuthBase]:
        """
        Returns the associated authentication required to access to the Wxs
        service.
        :returns: an authentication compatible with requests library.
        :rtype: AuthBase
        """
        if self.__auth is None:
            credential = keyring.get_credential(
                service_name=self.path.path,
                username=None
            )
            if credential is not None:
                self.__auth = HTTPBasicAuth(
                    credential.username,
                    credential.password
                )
        return self.__auth

    @property
    @abc.abstractmethod
    def type_service(self):
        raise NotImplementedError

    @property
    def path(self) -> ParsedPath:
        if self.__path is None:
            self.__path = ParsedPath(self._service_url)
        return self.__path

    @staticmethod
    def compute_key_url(url, arguments: dict):
        if arguments is not None:
            for (key, value) in arguments.items():
                if isinstance(value, (list, tuple)):
                    for value_item in value:
                        url += f'&{key}={value_item}'
                else:
                    url += f'&{key}={value}'
        return url

    def url_service(self, request: str):
        url = f'{self._service_url}?request={request}' \
               f'&service={self.type_service}'
        return WXSServiceNode.compute_key_url(url, self.__other_key)

    def get_capabilities(self):
        get_caps = WXSNodeOperationGetCapabilities(self)
        return get_caps.children()[0]

    @property
    @deprecated(version='1.2.0',
                reason='Only bracket browse should be use')
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            try:
                self.read_capabilities(self.get_capabilities())
            except DrbException as ex:
                raise DrbFactoryException(
                    f'Unsupported Wxs service: {self.name}')

        return self._children

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(f"Wxs Not doesn't support {impl} implementation")

    def __eq__(self, other):
        return isinstance(other, WXSServiceNode) and \
            self._service_url == other._service_url

    def __hash__(self):
        return hash(self._service_url)


class WXSNodeOperation(AbstractNode):

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def __compute_url(self, arguments: dict):
        url = self._parent.url_service(self.name)
        if self._version is not None and len(self._version) > 0 \
                and 'version' not in arguments.keys():
            url = WXSServiceNode.compute_key_url(url,
                                                 {'version': self._version})
        return WXSServiceNode.compute_key_url(url, arguments)

    def __init__(self,
                 source: WXSServiceNode,
                 name: str,
                 namespace: str,
                 attributes: dict = {},
                 version: str = None):
        super(AbstractNode, self).__init__()

        self.name = name
        self.namespace_uri = namespace
        self.parent = source
        self._version = version
        self.__init_attributes(attributes)
        self._available_impl.clear()

    def __init_attributes(self, attr: dict):
        for key in attr.keys():
            self @= (key[0], key[1], attr[key])

    @property
    @deprecated(version='1.2.0',
                reason='Only bracket browse should be use')
    def children(self) -> List[DrbNode]:
        return []

    @staticmethod
    def _get_content_type(node):
        content_type = ''
        for attr_key in node.attribute_names():
            if attr_key[0].lower() == 'content-type':
                content_type = node @ attr_key[0]
        return content_type

    def _get_child(self, item):
        if isinstance(item, dict):
            url = self.__compute_url(item)
            node = DrbHttpNode(url, auth=self._parent.get_auth())
            impl = node.get_impl(io.BytesIO)

            content_type = self._get_content_type(node)
            if 'text/xml' in content_type:
                tree = ElementTree.parse(impl)
                node_child = XmlNode(tree.getroot())
            elif 'text/html' in content_type:
                tree = ElementTree.parse(impl)
                node_child = XmlNode(tree.getroot())
            else:
                node_child = create(node)
            return node_child
        else:
            raise KeyError(f'Invalid key: {type(item)}')

    def __getitem__(self, item):
        return self._get_child(item)


class WXSNodeOperationGetCapabilities(WXSNodeOperation):
    def __init__(self,
                 source: WXSServiceNode):
        super().__init__(source, 'GetCapabilities', None)

    def children(self) -> List[DrbNode]:
        return [self._get_child({})]
