# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Template(object):
    """
    The properties that define a template. A template is a pre-built Terraform configuration that provisions a set of resources used in a common scenario.
    """

    #: A constant which can be used with the lifecycle_state property of a Template.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    def __init__(self, **kwargs):
        """
        Initializes a new Template object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this Template.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this Template.
        :type compartment_id: str

        :param category_id:
            The value to assign to the category_id property of this Template.
        :type category_id: str

        :param display_name:
            The value to assign to the display_name property of this Template.
        :type display_name: str

        :param description:
            The value to assign to the description property of this Template.
        :type description: str

        :param long_description:
            The value to assign to the long_description property of this Template.
        :type long_description: str

        :param is_free_tier:
            The value to assign to the is_free_tier property of this Template.
        :type is_free_tier: bool

        :param time_created:
            The value to assign to the time_created property of this Template.
        :type time_created: datetime

        :param template_config_source:
            The value to assign to the template_config_source property of this Template.
        :type template_config_source: oci.resource_manager.models.TemplateConfigSource

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this Template.
            Allowed values for this property are: "ACTIVE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this Template.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this Template.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'category_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'long_description': 'str',
            'is_free_tier': 'bool',
            'time_created': 'datetime',
            'template_config_source': 'TemplateConfigSource',
            'lifecycle_state': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'category_id': 'categoryId',
            'display_name': 'displayName',
            'description': 'description',
            'long_description': 'longDescription',
            'is_free_tier': 'isFreeTier',
            'time_created': 'timeCreated',
            'template_config_source': 'templateConfigSource',
            'lifecycle_state': 'lifecycleState',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._compartment_id = None
        self._category_id = None
        self._display_name = None
        self._description = None
        self._long_description = None
        self._is_free_tier = None
        self._time_created = None
        self._template_config_source = None
        self._lifecycle_state = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this Template.
        Unique identifier (`OCID`__) for the template.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this Template.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Template.
        Unique identifier (`OCID`__) for the template.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this Template.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this Template.
        The `OCID`__ of the compartment containing this template.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this Template.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this Template.
        The `OCID`__ of the compartment containing this template.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this Template.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def category_id(self):
        """
        Gets the category_id of this Template.
        Unique identifier for the category where the template is located.
        Possible values are `0` (Quick Starts), `1` (Service), `2` (Architecture), and `3` (Private).


        :return: The category_id of this Template.
        :rtype: str
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """
        Sets the category_id of this Template.
        Unique identifier for the category where the template is located.
        Possible values are `0` (Quick Starts), `1` (Service), `2` (Architecture), and `3` (Private).


        :param category_id: The category_id of this Template.
        :type: str
        """
        self._category_id = category_id

    @property
    def display_name(self):
        """
        Gets the display_name of this Template.
        Human-readable name of the template.


        :return: The display_name of this Template.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this Template.
        Human-readable name of the template.


        :param display_name: The display_name of this Template.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this Template.
        Brief description of the template.


        :return: The description of this Template.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Template.
        Brief description of the template.


        :param description: The description of this Template.
        :type: str
        """
        self._description = description

    @property
    def long_description(self):
        """
        Gets the long_description of this Template.
        Detailed description of the template. This description is displayed in the Console page listing templates when the template is expanded. Avoid entering confidential information.


        :return: The long_description of this Template.
        :rtype: str
        """
        return self._long_description

    @long_description.setter
    def long_description(self, long_description):
        """
        Sets the long_description of this Template.
        Detailed description of the template. This description is displayed in the Console page listing templates when the template is expanded. Avoid entering confidential information.


        :param long_description: The long_description of this Template.
        :type: str
        """
        self._long_description = long_description

    @property
    def is_free_tier(self):
        """
        Gets the is_free_tier of this Template.
        whether the template will work for free tier tenancy.


        :return: The is_free_tier of this Template.
        :rtype: bool
        """
        return self._is_free_tier

    @is_free_tier.setter
    def is_free_tier(self, is_free_tier):
        """
        Sets the is_free_tier of this Template.
        whether the template will work for free tier tenancy.


        :param is_free_tier: The is_free_tier of this Template.
        :type: bool
        """
        self._is_free_tier = is_free_tier

    @property
    def time_created(self):
        """
        Gets the time_created of this Template.
        The date and time at which the template was created.
        Format is defined by RFC3339.
        Example: `2020-11-25T21:10:29.600Z`


        :return: The time_created of this Template.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this Template.
        The date and time at which the template was created.
        Format is defined by RFC3339.
        Example: `2020-11-25T21:10:29.600Z`


        :param time_created: The time_created of this Template.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def template_config_source(self):
        """
        Gets the template_config_source of this Template.

        :return: The template_config_source of this Template.
        :rtype: oci.resource_manager.models.TemplateConfigSource
        """
        return self._template_config_source

    @template_config_source.setter
    def template_config_source(self, template_config_source):
        """
        Sets the template_config_source of this Template.

        :param template_config_source: The template_config_source of this Template.
        :type: oci.resource_manager.models.TemplateConfigSource
        """
        self._template_config_source = template_config_source

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this Template.
        The current lifecycle state of the template.

        Allowed values for this property are: "ACTIVE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this Template.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this Template.
        The current lifecycle state of the template.


        :param lifecycle_state: The lifecycle_state of this Template.
        :type: str
        """
        allowed_values = ["ACTIVE"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this Template.
        Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this Template.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this Template.
        Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this Template.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this Template.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this Template.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this Template.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this Template.
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
