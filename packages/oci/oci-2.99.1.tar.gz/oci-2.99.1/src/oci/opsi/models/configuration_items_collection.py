# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConfigurationItemsCollection(object):
    """
    Collection of configuration item summary objects.
    """

    #: A constant which can be used with the opsi_config_type property of a ConfigurationItemsCollection.
    #: This constant has a value of "UX_CONFIGURATION"
    OPSI_CONFIG_TYPE_UX_CONFIGURATION = "UX_CONFIGURATION"

    def __init__(self, **kwargs):
        """
        Initializes a new ConfigurationItemsCollection object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.opsi.models.UxConfigurationItemsCollection`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param opsi_config_type:
            The value to assign to the opsi_config_type property of this ConfigurationItemsCollection.
            Allowed values for this property are: "UX_CONFIGURATION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type opsi_config_type: str

        :param config_items:
            The value to assign to the config_items property of this ConfigurationItemsCollection.
        :type config_items: list[oci.opsi.models.ConfigurationItemSummary]

        """
        self.swagger_types = {
            'opsi_config_type': 'str',
            'config_items': 'list[ConfigurationItemSummary]'
        }

        self.attribute_map = {
            'opsi_config_type': 'opsiConfigType',
            'config_items': 'configItems'
        }

        self._opsi_config_type = None
        self._config_items = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['opsiConfigType']

        if type == 'UX_CONFIGURATION':
            return 'UxConfigurationItemsCollection'
        else:
            return 'ConfigurationItemsCollection'

    @property
    def opsi_config_type(self):
        """
        **[Required]** Gets the opsi_config_type of this ConfigurationItemsCollection.
        OPSI configuration type.

        Allowed values for this property are: "UX_CONFIGURATION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The opsi_config_type of this ConfigurationItemsCollection.
        :rtype: str
        """
        return self._opsi_config_type

    @opsi_config_type.setter
    def opsi_config_type(self, opsi_config_type):
        """
        Sets the opsi_config_type of this ConfigurationItemsCollection.
        OPSI configuration type.


        :param opsi_config_type: The opsi_config_type of this ConfigurationItemsCollection.
        :type: str
        """
        allowed_values = ["UX_CONFIGURATION"]
        if not value_allowed_none_or_none_sentinel(opsi_config_type, allowed_values):
            opsi_config_type = 'UNKNOWN_ENUM_VALUE'
        self._opsi_config_type = opsi_config_type

    @property
    def config_items(self):
        """
        Gets the config_items of this ConfigurationItemsCollection.
        Array of configuration item summary objects.


        :return: The config_items of this ConfigurationItemsCollection.
        :rtype: list[oci.opsi.models.ConfigurationItemSummary]
        """
        return self._config_items

    @config_items.setter
    def config_items(self, config_items):
        """
        Sets the config_items of this ConfigurationItemsCollection.
        Array of configuration item summary objects.


        :param config_items: The config_items of this ConfigurationItemsCollection.
        :type: list[oci.opsi.models.ConfigurationItemSummary]
        """
        self._config_items = config_items

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
