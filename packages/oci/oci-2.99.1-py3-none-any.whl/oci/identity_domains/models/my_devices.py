# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyDevices(object):
    """
    The SCIM protocol defines a standard set of query parameters that can be used to filter, sort, and paginate to return zero or more resources in a query response. Queries MAY be made against a single resource or a resource type endpoint (e.g., /Users), or the service provider Base URI.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MyDevices object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param schemas:
            The value to assign to the schemas property of this MyDevices.
        :type schemas: list[str]

        :param total_results:
            The value to assign to the total_results property of this MyDevices.
        :type total_results: int

        :param resources:
            The value to assign to the resources property of this MyDevices.
        :type resources: list[oci.identity_domains.models.MyDevice]

        :param start_index:
            The value to assign to the start_index property of this MyDevices.
        :type start_index: int

        :param items_per_page:
            The value to assign to the items_per_page property of this MyDevices.
        :type items_per_page: int

        """
        self.swagger_types = {
            'schemas': 'list[str]',
            'total_results': 'int',
            'resources': 'list[MyDevice]',
            'start_index': 'int',
            'items_per_page': 'int'
        }

        self.attribute_map = {
            'schemas': 'schemas',
            'total_results': 'totalResults',
            'resources': 'Resources',
            'start_index': 'startIndex',
            'items_per_page': 'itemsPerPage'
        }

        self._schemas = None
        self._total_results = None
        self._resources = None
        self._start_index = None
        self._items_per_page = None

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this MyDevices.
        The schemas attribute is an array of Strings which allows introspection of the supported schema version for a SCIM representation as well any schema extensions supported by that representation. Each String value must be a unique URI. All representations of SCIM schema MUST include a non-zero value array with value(s) of the URIs supported by that representation. Duplicate values MUST NOT be included. Value order is not specified and MUST not impact behavior. REQUIRED.


        :return: The schemas of this MyDevices.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this MyDevices.
        The schemas attribute is an array of Strings which allows introspection of the supported schema version for a SCIM representation as well any schema extensions supported by that representation. Each String value must be a unique URI. All representations of SCIM schema MUST include a non-zero value array with value(s) of the URIs supported by that representation. Duplicate values MUST NOT be included. Value order is not specified and MUST not impact behavior. REQUIRED.


        :param schemas: The schemas of this MyDevices.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def total_results(self):
        """
        **[Required]** Gets the total_results of this MyDevices.
        The total number of results returned by the list or query operation.  The value may be larger than the number of resources returned such as when returning a single page of results where multiple pages are available. REQUIRED.


        :return: The total_results of this MyDevices.
        :rtype: int
        """
        return self._total_results

    @total_results.setter
    def total_results(self, total_results):
        """
        Sets the total_results of this MyDevices.
        The total number of results returned by the list or query operation.  The value may be larger than the number of resources returned such as when returning a single page of results where multiple pages are available. REQUIRED.


        :param total_results: The total_results of this MyDevices.
        :type: int
        """
        self._total_results = total_results

    @property
    def resources(self):
        """
        **[Required]** Gets the resources of this MyDevices.
        A multi-valued list of complex objects containing the requested resources. This MAY be a subset of the full set of resources if pagination is requested. REQUIRED if \"totalResults\" is non-zero.


        :return: The resources of this MyDevices.
        :rtype: list[oci.identity_domains.models.MyDevice]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """
        Sets the resources of this MyDevices.
        A multi-valued list of complex objects containing the requested resources. This MAY be a subset of the full set of resources if pagination is requested. REQUIRED if \"totalResults\" is non-zero.


        :param resources: The resources of this MyDevices.
        :type: list[oci.identity_domains.models.MyDevice]
        """
        self._resources = resources

    @property
    def start_index(self):
        """
        **[Required]** Gets the start_index of this MyDevices.
        The 1-based index of the first result in the current set of list results.  REQUIRED when partial results returned due to pagination.


        :return: The start_index of this MyDevices.
        :rtype: int
        """
        return self._start_index

    @start_index.setter
    def start_index(self, start_index):
        """
        Sets the start_index of this MyDevices.
        The 1-based index of the first result in the current set of list results.  REQUIRED when partial results returned due to pagination.


        :param start_index: The start_index of this MyDevices.
        :type: int
        """
        self._start_index = start_index

    @property
    def items_per_page(self):
        """
        **[Required]** Gets the items_per_page of this MyDevices.
        The number of resources returned in a list response page. REQUIRED when partial results returned due to pagination.


        :return: The items_per_page of this MyDevices.
        :rtype: int
        """
        return self._items_per_page

    @items_per_page.setter
    def items_per_page(self, items_per_page):
        """
        Sets the items_per_page of this MyDevices.
        The number of resources returned in a list response page. REQUIRED when partial results returned due to pagination.


        :param items_per_page: The items_per_page of this MyDevices.
        :type: int
        """
        self._items_per_page = items_per_page

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
