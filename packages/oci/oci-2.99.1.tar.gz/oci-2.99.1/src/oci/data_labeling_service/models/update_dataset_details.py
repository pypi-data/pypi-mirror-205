# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateDatasetDetails(object):
    """
    Once the Dataset is defined, it's largely immutable from a metadata perspective.  The records found in the data source itself, may change over time.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateDatasetDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateDatasetDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdateDatasetDetails.
        :type description: str

        :param labeling_instructions:
            The value to assign to the labeling_instructions property of this UpdateDatasetDetails.
        :type labeling_instructions: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateDatasetDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateDatasetDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'description': 'str',
            'labeling_instructions': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'description': 'description',
            'labeling_instructions': 'labelingInstructions',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._description = None
        self._labeling_instructions = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateDatasetDetails.
        A user-friendly display name for the resource.


        :return: The display_name of this UpdateDatasetDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateDatasetDetails.
        A user-friendly display name for the resource.


        :param display_name: The display_name of this UpdateDatasetDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this UpdateDatasetDetails.
        A user provided description of the dataset


        :return: The description of this UpdateDatasetDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateDatasetDetails.
        A user provided description of the dataset


        :param description: The description of this UpdateDatasetDetails.
        :type: str
        """
        self._description = description

    @property
    def labeling_instructions(self):
        """
        Gets the labeling_instructions of this UpdateDatasetDetails.
        The labeling instructions for human labelers in rich text format


        :return: The labeling_instructions of this UpdateDatasetDetails.
        :rtype: str
        """
        return self._labeling_instructions

    @labeling_instructions.setter
    def labeling_instructions(self, labeling_instructions):
        """
        Sets the labeling_instructions of this UpdateDatasetDetails.
        The labeling instructions for human labelers in rich text format


        :param labeling_instructions: The labeling_instructions of this UpdateDatasetDetails.
        :type: str
        """
        self._labeling_instructions = labeling_instructions

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateDatasetDetails.
        A simple key-value pair that is applied without any predefined name, type, or scope. It exists for cross-compatibility only.
        For example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateDatasetDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateDatasetDetails.
        A simple key-value pair that is applied without any predefined name, type, or scope. It exists for cross-compatibility only.
        For example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateDatasetDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateDatasetDetails.
        The defined tags for this resource. Each key is predefined and scoped to a namespace.
        For example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateDatasetDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateDatasetDetails.
        The defined tags for this resource. Each key is predefined and scoped to a namespace.
        For example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateDatasetDetails.
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
