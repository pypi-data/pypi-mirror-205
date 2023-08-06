# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateTemplateDetails(object):
    """
    Update details for a template.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateTemplateDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateTemplateDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdateTemplateDetails.
        :type description: str

        :param long_description:
            The value to assign to the long_description property of this UpdateTemplateDetails.
        :type long_description: str

        :param logo_file_base64_encoded:
            The value to assign to the logo_file_base64_encoded property of this UpdateTemplateDetails.
        :type logo_file_base64_encoded: str

        :param template_config_source:
            The value to assign to the template_config_source property of this UpdateTemplateDetails.
        :type template_config_source: oci.resource_manager.models.UpdateTemplateConfigSourceDetails

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateTemplateDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateTemplateDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'description': 'str',
            'long_description': 'str',
            'logo_file_base64_encoded': 'str',
            'template_config_source': 'UpdateTemplateConfigSourceDetails',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'description': 'description',
            'long_description': 'longDescription',
            'logo_file_base64_encoded': 'logoFileBase64Encoded',
            'template_config_source': 'templateConfigSource',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._description = None
        self._long_description = None
        self._logo_file_base64_encoded = None
        self._template_config_source = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateTemplateDetails.
        The template's display name. Avoid entering confidential information.


        :return: The display_name of this UpdateTemplateDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateTemplateDetails.
        The template's display name. Avoid entering confidential information.


        :param display_name: The display_name of this UpdateTemplateDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this UpdateTemplateDetails.
        Description of the template. Avoid entering confidential information.


        :return: The description of this UpdateTemplateDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateTemplateDetails.
        Description of the template. Avoid entering confidential information.


        :param description: The description of this UpdateTemplateDetails.
        :type: str
        """
        self._description = description

    @property
    def long_description(self):
        """
        Gets the long_description of this UpdateTemplateDetails.
        Detailed description of the template. This description is displayed in the Console page listing templates when the template is expanded. Avoid entering confidential information.


        :return: The long_description of this UpdateTemplateDetails.
        :rtype: str
        """
        return self._long_description

    @long_description.setter
    def long_description(self, long_description):
        """
        Sets the long_description of this UpdateTemplateDetails.
        Detailed description of the template. This description is displayed in the Console page listing templates when the template is expanded. Avoid entering confidential information.


        :param long_description: The long_description of this UpdateTemplateDetails.
        :type: str
        """
        self._long_description = long_description

    @property
    def logo_file_base64_encoded(self):
        """
        Gets the logo_file_base64_encoded of this UpdateTemplateDetails.
        Base64-encoded logo for the template.


        :return: The logo_file_base64_encoded of this UpdateTemplateDetails.
        :rtype: str
        """
        return self._logo_file_base64_encoded

    @logo_file_base64_encoded.setter
    def logo_file_base64_encoded(self, logo_file_base64_encoded):
        """
        Sets the logo_file_base64_encoded of this UpdateTemplateDetails.
        Base64-encoded logo for the template.


        :param logo_file_base64_encoded: The logo_file_base64_encoded of this UpdateTemplateDetails.
        :type: str
        """
        self._logo_file_base64_encoded = logo_file_base64_encoded

    @property
    def template_config_source(self):
        """
        Gets the template_config_source of this UpdateTemplateDetails.

        :return: The template_config_source of this UpdateTemplateDetails.
        :rtype: oci.resource_manager.models.UpdateTemplateConfigSourceDetails
        """
        return self._template_config_source

    @template_config_source.setter
    def template_config_source(self, template_config_source):
        """
        Sets the template_config_source of this UpdateTemplateDetails.

        :param template_config_source: The template_config_source of this UpdateTemplateDetails.
        :type: oci.resource_manager.models.UpdateTemplateConfigSourceDetails
        """
        self._template_config_source = template_config_source

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateTemplateDetails.
        Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateTemplateDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateTemplateDetails.
        Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateTemplateDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateTemplateDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateTemplateDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateTemplateDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateTemplateDetails.
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
