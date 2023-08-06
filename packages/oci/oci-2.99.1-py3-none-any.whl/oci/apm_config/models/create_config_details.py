# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateConfigDetails(object):
    """
    The request body used to create new configuration items. It must specify the configuration type of the item,
    as well as the actual data to populate the item with.
    """

    #: A constant which can be used with the config_type property of a CreateConfigDetails.
    #: This constant has a value of "SPAN_FILTER"
    CONFIG_TYPE_SPAN_FILTER = "SPAN_FILTER"

    #: A constant which can be used with the config_type property of a CreateConfigDetails.
    #: This constant has a value of "METRIC_GROUP"
    CONFIG_TYPE_METRIC_GROUP = "METRIC_GROUP"

    #: A constant which can be used with the config_type property of a CreateConfigDetails.
    #: This constant has a value of "APDEX"
    CONFIG_TYPE_APDEX = "APDEX"

    #: A constant which can be used with the config_type property of a CreateConfigDetails.
    #: This constant has a value of "OPTIONS"
    CONFIG_TYPE_OPTIONS = "OPTIONS"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateConfigDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.apm_config.models.CreateSpanFilterDetails`
        * :class:`~oci.apm_config.models.CreateMetricGroupDetails`
        * :class:`~oci.apm_config.models.CreateOptionsDetails`
        * :class:`~oci.apm_config.models.CreateApdexRulesDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param config_type:
            The value to assign to the config_type property of this CreateConfigDetails.
            Allowed values for this property are: "SPAN_FILTER", "METRIC_GROUP", "APDEX", "OPTIONS"
        :type config_type: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateConfigDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateConfigDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'config_type': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'config_type': 'configType',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._config_type = None
        self._freeform_tags = None
        self._defined_tags = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['configType']

        if type == 'SPAN_FILTER':
            return 'CreateSpanFilterDetails'

        if type == 'METRIC_GROUP':
            return 'CreateMetricGroupDetails'

        if type == 'OPTIONS':
            return 'CreateOptionsDetails'

        if type == 'APDEX':
            return 'CreateApdexRulesDetails'
        else:
            return 'CreateConfigDetails'

    @property
    def config_type(self):
        """
        **[Required]** Gets the config_type of this CreateConfigDetails.
        The type of configuration item.

        Allowed values for this property are: "SPAN_FILTER", "METRIC_GROUP", "APDEX", "OPTIONS"


        :return: The config_type of this CreateConfigDetails.
        :rtype: str
        """
        return self._config_type

    @config_type.setter
    def config_type(self, config_type):
        """
        Sets the config_type of this CreateConfigDetails.
        The type of configuration item.


        :param config_type: The config_type of this CreateConfigDetails.
        :type: str
        """
        allowed_values = ["SPAN_FILTER", "METRIC_GROUP", "APDEX", "OPTIONS"]
        if not value_allowed_none_or_none_sentinel(config_type, allowed_values):
            raise ValueError(
                "Invalid value for `config_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._config_type = config_type

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateConfigDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateConfigDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateConfigDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateConfigDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateConfigDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateConfigDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateConfigDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateConfigDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
