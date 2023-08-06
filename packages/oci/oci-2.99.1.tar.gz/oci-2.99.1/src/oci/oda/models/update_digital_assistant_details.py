# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateDigitalAssistantDetails(object):
    """
    Properties to update a Digital Assistant.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateDigitalAssistantDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param category:
            The value to assign to the category property of this UpdateDigitalAssistantDetails.
        :type category: str

        :param description:
            The value to assign to the description property of this UpdateDigitalAssistantDetails.
        :type description: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateDigitalAssistantDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateDigitalAssistantDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'category': 'str',
            'description': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'category': 'category',
            'description': 'description',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._category = None
        self._description = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def category(self):
        """
        Gets the category of this UpdateDigitalAssistantDetails.
        The resource's category.  This is used to group resource's together.


        :return: The category of this UpdateDigitalAssistantDetails.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this UpdateDigitalAssistantDetails.
        The resource's category.  This is used to group resource's together.


        :param category: The category of this UpdateDigitalAssistantDetails.
        :type: str
        """
        self._category = category

    @property
    def description(self):
        """
        Gets the description of this UpdateDigitalAssistantDetails.
        A short description of the resource.


        :return: The description of this UpdateDigitalAssistantDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateDigitalAssistantDetails.
        A short description of the resource.


        :param description: The description of this UpdateDigitalAssistantDetails.
        :type: str
        """
        self._description = description

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateDigitalAssistantDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateDigitalAssistantDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateDigitalAssistantDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateDigitalAssistantDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateDigitalAssistantDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateDigitalAssistantDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateDigitalAssistantDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateDigitalAssistantDetails.
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
