# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MonitoredResourceAliasSourceCredential(object):
    """
    Monitored Resource Alias Reference Source Credential
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MonitoredResourceAliasSourceCredential object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source:
            The value to assign to the source property of this MonitoredResourceAliasSourceCredential.
        :type source: str

        :param name:
            The value to assign to the name property of this MonitoredResourceAliasSourceCredential.
        :type name: str

        :param service:
            The value to assign to the service property of this MonitoredResourceAliasSourceCredential.
        :type service: str

        """
        self.swagger_types = {
            'source': 'str',
            'name': 'str',
            'service': 'str'
        }

        self.attribute_map = {
            'source': 'source',
            'name': 'name',
            'service': 'service'
        }

        self._source = None
        self._name = None
        self._service = None

    @property
    def source(self):
        """
        **[Required]** Gets the source of this MonitoredResourceAliasSourceCredential.
        The source type and source name combination,delimited with (.) separator. This refers to the pre-existing source which alias cred should point to. Ex. {source type}.{source name} and source type max char limit is 63.


        :return: The source of this MonitoredResourceAliasSourceCredential.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Sets the source of this MonitoredResourceAliasSourceCredential.
        The source type and source name combination,delimited with (.) separator. This refers to the pre-existing source which alias cred should point to. Ex. {source type}.{source name} and source type max char limit is 63.


        :param source: The source of this MonitoredResourceAliasSourceCredential.
        :type: str
        """
        self._source = source

    @property
    def name(self):
        """
        **[Required]** Gets the name of this MonitoredResourceAliasSourceCredential.
        The name of the pre-existing source credential which alias cred should point to. This should refer to the pre-existing source attribute binded credential name.


        :return: The name of this MonitoredResourceAliasSourceCredential.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this MonitoredResourceAliasSourceCredential.
        The name of the pre-existing source credential which alias cred should point to. This should refer to the pre-existing source attribute binded credential name.


        :param name: The name of this MonitoredResourceAliasSourceCredential.
        :type: str
        """
        self._name = name

    @property
    def service(self):
        """
        **[Required]** Gets the service of this MonitoredResourceAliasSourceCredential.
        The name of the service owning the credential. Ex stack-monitoring or dbmgmt


        :return: The service of this MonitoredResourceAliasSourceCredential.
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service):
        """
        Sets the service of this MonitoredResourceAliasSourceCredential.
        The name of the service owning the credential. Ex stack-monitoring or dbmgmt


        :param service: The service of this MonitoredResourceAliasSourceCredential.
        :type: str
        """
        self._service = service

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
