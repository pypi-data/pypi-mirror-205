# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateOpaInstanceDetails(object):
    """
    The information about new OpaInstance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateOpaInstanceDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this CreateOpaInstanceDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this CreateOpaInstanceDetails.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateOpaInstanceDetails.
        :type compartment_id: str

        :param consumption_model:
            The value to assign to the consumption_model property of this CreateOpaInstanceDetails.
        :type consumption_model: str

        :param shape_name:
            The value to assign to the shape_name property of this CreateOpaInstanceDetails.
        :type shape_name: str

        :param metering_type:
            The value to assign to the metering_type property of this CreateOpaInstanceDetails.
        :type metering_type: str

        :param idcs_at:
            The value to assign to the idcs_at property of this CreateOpaInstanceDetails.
        :type idcs_at: str

        :param is_breakglass_enabled:
            The value to assign to the is_breakglass_enabled property of this CreateOpaInstanceDetails.
        :type is_breakglass_enabled: bool

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateOpaInstanceDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateOpaInstanceDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'consumption_model': 'str',
            'shape_name': 'str',
            'metering_type': 'str',
            'idcs_at': 'str',
            'is_breakglass_enabled': 'bool',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'consumption_model': 'consumptionModel',
            'shape_name': 'shapeName',
            'metering_type': 'meteringType',
            'idcs_at': 'idcsAt',
            'is_breakglass_enabled': 'isBreakglassEnabled',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._description = None
        self._compartment_id = None
        self._consumption_model = None
        self._shape_name = None
        self._metering_type = None
        self._idcs_at = None
        self._is_breakglass_enabled = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this CreateOpaInstanceDetails.
        OpaInstance Identifier. User-friendly name for the instance. Avoid entering confidential information. You can change this value anytime.


        :return: The display_name of this CreateOpaInstanceDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateOpaInstanceDetails.
        OpaInstance Identifier. User-friendly name for the instance. Avoid entering confidential information. You can change this value anytime.


        :param display_name: The display_name of this CreateOpaInstanceDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this CreateOpaInstanceDetails.
        Description of the Oracle Process Automation instance.


        :return: The description of this CreateOpaInstanceDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateOpaInstanceDetails.
        Description of the Oracle Process Automation instance.


        :param description: The description of this CreateOpaInstanceDetails.
        :type: str
        """
        self._description = description

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateOpaInstanceDetails.
        Compartment Identifier


        :return: The compartment_id of this CreateOpaInstanceDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateOpaInstanceDetails.
        Compartment Identifier


        :param compartment_id: The compartment_id of this CreateOpaInstanceDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def consumption_model(self):
        """
        Gets the consumption_model of this CreateOpaInstanceDetails.
        Parameter specifying which entitlement to use for billing purposes


        :return: The consumption_model of this CreateOpaInstanceDetails.
        :rtype: str
        """
        return self._consumption_model

    @consumption_model.setter
    def consumption_model(self, consumption_model):
        """
        Sets the consumption_model of this CreateOpaInstanceDetails.
        Parameter specifying which entitlement to use for billing purposes


        :param consumption_model: The consumption_model of this CreateOpaInstanceDetails.
        :type: str
        """
        self._consumption_model = consumption_model

    @property
    def shape_name(self):
        """
        **[Required]** Gets the shape_name of this CreateOpaInstanceDetails.
        Shape of the instance.


        :return: The shape_name of this CreateOpaInstanceDetails.
        :rtype: str
        """
        return self._shape_name

    @shape_name.setter
    def shape_name(self, shape_name):
        """
        Sets the shape_name of this CreateOpaInstanceDetails.
        Shape of the instance.


        :param shape_name: The shape_name of this CreateOpaInstanceDetails.
        :type: str
        """
        self._shape_name = shape_name

    @property
    def metering_type(self):
        """
        Gets the metering_type of this CreateOpaInstanceDetails.
        MeteringType Identifier


        :return: The metering_type of this CreateOpaInstanceDetails.
        :rtype: str
        """
        return self._metering_type

    @metering_type.setter
    def metering_type(self, metering_type):
        """
        Sets the metering_type of this CreateOpaInstanceDetails.
        MeteringType Identifier


        :param metering_type: The metering_type of this CreateOpaInstanceDetails.
        :type: str
        """
        self._metering_type = metering_type

    @property
    def idcs_at(self):
        """
        Gets the idcs_at of this CreateOpaInstanceDetails.
        IDCS Authentication token. This is required for all realms with IDCS. This property is optional, as it is not required for non-IDCS realms.


        :return: The idcs_at of this CreateOpaInstanceDetails.
        :rtype: str
        """
        return self._idcs_at

    @idcs_at.setter
    def idcs_at(self, idcs_at):
        """
        Sets the idcs_at of this CreateOpaInstanceDetails.
        IDCS Authentication token. This is required for all realms with IDCS. This property is optional, as it is not required for non-IDCS realms.


        :param idcs_at: The idcs_at of this CreateOpaInstanceDetails.
        :type: str
        """
        self._idcs_at = idcs_at

    @property
    def is_breakglass_enabled(self):
        """
        Gets the is_breakglass_enabled of this CreateOpaInstanceDetails.
        indicates if breakGlass is enabled for the opa instance.


        :return: The is_breakglass_enabled of this CreateOpaInstanceDetails.
        :rtype: bool
        """
        return self._is_breakglass_enabled

    @is_breakglass_enabled.setter
    def is_breakglass_enabled(self, is_breakglass_enabled):
        """
        Sets the is_breakglass_enabled of this CreateOpaInstanceDetails.
        indicates if breakGlass is enabled for the opa instance.


        :param is_breakglass_enabled: The is_breakglass_enabled of this CreateOpaInstanceDetails.
        :type: bool
        """
        self._is_breakglass_enabled = is_breakglass_enabled

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateOpaInstanceDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateOpaInstanceDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateOpaInstanceDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateOpaInstanceDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateOpaInstanceDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateOpaInstanceDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateOpaInstanceDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateOpaInstanceDetails.
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
