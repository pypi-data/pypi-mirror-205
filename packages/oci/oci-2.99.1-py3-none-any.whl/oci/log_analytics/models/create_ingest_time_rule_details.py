# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateIngestTimeRuleDetails(object):
    """
    The information required to create an ingest time rule.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateIngestTimeRuleDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateIngestTimeRuleDetails.
        :type compartment_id: str

        :param description:
            The value to assign to the description property of this CreateIngestTimeRuleDetails.
        :type description: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateIngestTimeRuleDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateIngestTimeRuleDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param display_name:
            The value to assign to the display_name property of this CreateIngestTimeRuleDetails.
        :type display_name: str

        :param conditions:
            The value to assign to the conditions property of this CreateIngestTimeRuleDetails.
        :type conditions: oci.log_analytics.models.IngestTimeRuleCondition

        :param actions:
            The value to assign to the actions property of this CreateIngestTimeRuleDetails.
        :type actions: list[oci.log_analytics.models.IngestTimeRuleAction]

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'description': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'display_name': 'str',
            'conditions': 'IngestTimeRuleCondition',
            'actions': 'list[IngestTimeRuleAction]'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'description': 'description',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'display_name': 'displayName',
            'conditions': 'conditions',
            'actions': 'actions'
        }

        self._compartment_id = None
        self._description = None
        self._freeform_tags = None
        self._defined_tags = None
        self._display_name = None
        self._conditions = None
        self._actions = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateIngestTimeRuleDetails.
        Compartment Identifier `OCID]`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateIngestTimeRuleDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateIngestTimeRuleDetails.
        Compartment Identifier `OCID]`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateIngestTimeRuleDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def description(self):
        """
        Gets the description of this CreateIngestTimeRuleDetails.
        Description for this resource.


        :return: The description of this CreateIngestTimeRuleDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateIngestTimeRuleDetails.
        Description for this resource.


        :param description: The description of this CreateIngestTimeRuleDetails.
        :type: str
        """
        self._description = description

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateIngestTimeRuleDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateIngestTimeRuleDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateIngestTimeRuleDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateIngestTimeRuleDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateIngestTimeRuleDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateIngestTimeRuleDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateIngestTimeRuleDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateIngestTimeRuleDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this CreateIngestTimeRuleDetails.
        The ingest time rule display name.


        :return: The display_name of this CreateIngestTimeRuleDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateIngestTimeRuleDetails.
        The ingest time rule display name.


        :param display_name: The display_name of this CreateIngestTimeRuleDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def conditions(self):
        """
        **[Required]** Gets the conditions of this CreateIngestTimeRuleDetails.

        :return: The conditions of this CreateIngestTimeRuleDetails.
        :rtype: oci.log_analytics.models.IngestTimeRuleCondition
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """
        Sets the conditions of this CreateIngestTimeRuleDetails.

        :param conditions: The conditions of this CreateIngestTimeRuleDetails.
        :type: oci.log_analytics.models.IngestTimeRuleCondition
        """
        self._conditions = conditions

    @property
    def actions(self):
        """
        **[Required]** Gets the actions of this CreateIngestTimeRuleDetails.
        The action(s) to be performed if the ingest time rule condition(s) are satisfied.


        :return: The actions of this CreateIngestTimeRuleDetails.
        :rtype: list[oci.log_analytics.models.IngestTimeRuleAction]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """
        Sets the actions of this CreateIngestTimeRuleDetails.
        The action(s) to be performed if the ingest time rule condition(s) are satisfied.


        :param actions: The actions of this CreateIngestTimeRuleDetails.
        :type: list[oci.log_analytics.models.IngestTimeRuleAction]
        """
        self._actions = actions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
