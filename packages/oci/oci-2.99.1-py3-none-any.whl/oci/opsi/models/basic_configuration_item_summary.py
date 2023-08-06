# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .configuration_item_summary import ConfigurationItemSummary
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class BasicConfigurationItemSummary(ConfigurationItemSummary):
    """
    Basic configuration item summary.
    Value field contain the most preferred value for the specified scope (compartmentId), which could be from any of the ConfigurationItemValueSourceConfigurationType.
    Default value field contains the default value from Operations Insights.
    """

    #: A constant which can be used with the value_source_config property of a BasicConfigurationItemSummary.
    #: This constant has a value of "DEFAULT"
    VALUE_SOURCE_CONFIG_DEFAULT = "DEFAULT"

    #: A constant which can be used with the value_source_config property of a BasicConfigurationItemSummary.
    #: This constant has a value of "TENANT"
    VALUE_SOURCE_CONFIG_TENANT = "TENANT"

    #: A constant which can be used with the value_source_config property of a BasicConfigurationItemSummary.
    #: This constant has a value of "COMPARTMENT"
    VALUE_SOURCE_CONFIG_COMPARTMENT = "COMPARTMENT"

    def __init__(self, **kwargs):
        """
        Initializes a new BasicConfigurationItemSummary object with values from keyword arguments. The default value of the :py:attr:`~oci.opsi.models.BasicConfigurationItemSummary.config_item_type` attribute
        of this class is ``BASIC`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param config_item_type:
            The value to assign to the config_item_type property of this BasicConfigurationItemSummary.
            Allowed values for this property are: "BASIC", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type config_item_type: str

        :param name:
            The value to assign to the name property of this BasicConfigurationItemSummary.
        :type name: str

        :param value:
            The value to assign to the value property of this BasicConfigurationItemSummary.
        :type value: str

        :param value_source_config:
            The value to assign to the value_source_config property of this BasicConfigurationItemSummary.
            Allowed values for this property are: "DEFAULT", "TENANT", "COMPARTMENT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type value_source_config: str

        :param default_value:
            The value to assign to the default_value property of this BasicConfigurationItemSummary.
        :type default_value: str

        :param applicable_contexts:
            The value to assign to the applicable_contexts property of this BasicConfigurationItemSummary.
        :type applicable_contexts: list[str]

        :param metadata:
            The value to assign to the metadata property of this BasicConfigurationItemSummary.
        :type metadata: oci.opsi.models.ConfigurationItemMetadata

        """
        self.swagger_types = {
            'config_item_type': 'str',
            'name': 'str',
            'value': 'str',
            'value_source_config': 'str',
            'default_value': 'str',
            'applicable_contexts': 'list[str]',
            'metadata': 'ConfigurationItemMetadata'
        }

        self.attribute_map = {
            'config_item_type': 'configItemType',
            'name': 'name',
            'value': 'value',
            'value_source_config': 'valueSourceConfig',
            'default_value': 'defaultValue',
            'applicable_contexts': 'applicableContexts',
            'metadata': 'metadata'
        }

        self._config_item_type = None
        self._name = None
        self._value = None
        self._value_source_config = None
        self._default_value = None
        self._applicable_contexts = None
        self._metadata = None
        self._config_item_type = 'BASIC'

    @property
    def name(self):
        """
        Gets the name of this BasicConfigurationItemSummary.
        Name of configuration item.


        :return: The name of this BasicConfigurationItemSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this BasicConfigurationItemSummary.
        Name of configuration item.


        :param name: The name of this BasicConfigurationItemSummary.
        :type: str
        """
        self._name = name

    @property
    def value(self):
        """
        Gets the value of this BasicConfigurationItemSummary.
        Value of configuration item.


        :return: The value of this BasicConfigurationItemSummary.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this BasicConfigurationItemSummary.
        Value of configuration item.


        :param value: The value of this BasicConfigurationItemSummary.
        :type: str
        """
        self._value = value

    @property
    def value_source_config(self):
        """
        Gets the value_source_config of this BasicConfigurationItemSummary.
        Source configuration from where the value is taken for a configuration item.

        Allowed values for this property are: "DEFAULT", "TENANT", "COMPARTMENT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The value_source_config of this BasicConfigurationItemSummary.
        :rtype: str
        """
        return self._value_source_config

    @value_source_config.setter
    def value_source_config(self, value_source_config):
        """
        Sets the value_source_config of this BasicConfigurationItemSummary.
        Source configuration from where the value is taken for a configuration item.


        :param value_source_config: The value_source_config of this BasicConfigurationItemSummary.
        :type: str
        """
        allowed_values = ["DEFAULT", "TENANT", "COMPARTMENT"]
        if not value_allowed_none_or_none_sentinel(value_source_config, allowed_values):
            value_source_config = 'UNKNOWN_ENUM_VALUE'
        self._value_source_config = value_source_config

    @property
    def default_value(self):
        """
        Gets the default_value of this BasicConfigurationItemSummary.
        Value of configuration item.


        :return: The default_value of this BasicConfigurationItemSummary.
        :rtype: str
        """
        return self._default_value

    @default_value.setter
    def default_value(self, default_value):
        """
        Sets the default_value of this BasicConfigurationItemSummary.
        Value of configuration item.


        :param default_value: The default_value of this BasicConfigurationItemSummary.
        :type: str
        """
        self._default_value = default_value

    @property
    def applicable_contexts(self):
        """
        Gets the applicable_contexts of this BasicConfigurationItemSummary.
        List of contexts in Operations Insights where this configuration item is applicable.


        :return: The applicable_contexts of this BasicConfigurationItemSummary.
        :rtype: list[str]
        """
        return self._applicable_contexts

    @applicable_contexts.setter
    def applicable_contexts(self, applicable_contexts):
        """
        Sets the applicable_contexts of this BasicConfigurationItemSummary.
        List of contexts in Operations Insights where this configuration item is applicable.


        :param applicable_contexts: The applicable_contexts of this BasicConfigurationItemSummary.
        :type: list[str]
        """
        self._applicable_contexts = applicable_contexts

    @property
    def metadata(self):
        """
        Gets the metadata of this BasicConfigurationItemSummary.

        :return: The metadata of this BasicConfigurationItemSummary.
        :rtype: oci.opsi.models.ConfigurationItemMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this BasicConfigurationItemSummary.

        :param metadata: The metadata of this BasicConfigurationItemSummary.
        :type: oci.opsi.models.ConfigurationItemMetadata
        """
        self._metadata = metadata

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
