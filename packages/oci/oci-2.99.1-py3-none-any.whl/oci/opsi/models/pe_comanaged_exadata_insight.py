# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .exadata_insight import ExadataInsight
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PeComanagedExadataInsight(ExadataInsight):
    """
    Private endpoint managed Exadata insight resource (ExaCS).
    """

    #: A constant which can be used with the exadata_infra_resource_type property of a PeComanagedExadataInsight.
    #: This constant has a value of "cloudExadataInfrastructure"
    EXADATA_INFRA_RESOURCE_TYPE_CLOUD_EXADATA_INFRASTRUCTURE = "cloudExadataInfrastructure"

    def __init__(self, **kwargs):
        """
        Initializes a new PeComanagedExadataInsight object with values from keyword arguments. The default value of the :py:attr:`~oci.opsi.models.PeComanagedExadataInsight.entity_source` attribute
        of this class is ``PE_COMANAGED_EXADATA`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param entity_source:
            The value to assign to the entity_source property of this PeComanagedExadataInsight.
            Allowed values for this property are: "EM_MANAGED_EXTERNAL_EXADATA", "PE_COMANAGED_EXADATA", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type entity_source: str

        :param id:
            The value to assign to the id property of this PeComanagedExadataInsight.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this PeComanagedExadataInsight.
        :type compartment_id: str

        :param exadata_name:
            The value to assign to the exadata_name property of this PeComanagedExadataInsight.
        :type exadata_name: str

        :param exadata_display_name:
            The value to assign to the exadata_display_name property of this PeComanagedExadataInsight.
        :type exadata_display_name: str

        :param exadata_type:
            The value to assign to the exadata_type property of this PeComanagedExadataInsight.
            Allowed values for this property are: "DBMACHINE", "EXACS", "EXACC", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type exadata_type: str

        :param exadata_rack_type:
            The value to assign to the exadata_rack_type property of this PeComanagedExadataInsight.
            Allowed values for this property are: "FULL", "HALF", "QUARTER", "EIGHTH", "FLEX", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type exadata_rack_type: str

        :param is_virtualized_exadata:
            The value to assign to the is_virtualized_exadata property of this PeComanagedExadataInsight.
        :type is_virtualized_exadata: bool

        :param status:
            The value to assign to the status property of this PeComanagedExadataInsight.
            Allowed values for this property are: "DISABLED", "ENABLED", "TERMINATED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this PeComanagedExadataInsight.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this PeComanagedExadataInsight.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this PeComanagedExadataInsight.
        :type system_tags: dict(str, dict(str, object))

        :param time_created:
            The value to assign to the time_created property of this PeComanagedExadataInsight.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this PeComanagedExadataInsight.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this PeComanagedExadataInsight.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this PeComanagedExadataInsight.
        :type lifecycle_details: str

        :param exadata_infra_id:
            The value to assign to the exadata_infra_id property of this PeComanagedExadataInsight.
        :type exadata_infra_id: str

        :param exadata_infra_resource_type:
            The value to assign to the exadata_infra_resource_type property of this PeComanagedExadataInsight.
            Allowed values for this property are: "cloudExadataInfrastructure", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type exadata_infra_resource_type: str

        :param exadata_shape:
            The value to assign to the exadata_shape property of this PeComanagedExadataInsight.
        :type exadata_shape: str

        """
        self.swagger_types = {
            'entity_source': 'str',
            'id': 'str',
            'compartment_id': 'str',
            'exadata_name': 'str',
            'exadata_display_name': 'str',
            'exadata_type': 'str',
            'exadata_rack_type': 'str',
            'is_virtualized_exadata': 'bool',
            'status': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'exadata_infra_id': 'str',
            'exadata_infra_resource_type': 'str',
            'exadata_shape': 'str'
        }

        self.attribute_map = {
            'entity_source': 'entitySource',
            'id': 'id',
            'compartment_id': 'compartmentId',
            'exadata_name': 'exadataName',
            'exadata_display_name': 'exadataDisplayName',
            'exadata_type': 'exadataType',
            'exadata_rack_type': 'exadataRackType',
            'is_virtualized_exadata': 'isVirtualizedExadata',
            'status': 'status',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'exadata_infra_id': 'exadataInfraId',
            'exadata_infra_resource_type': 'exadataInfraResourceType',
            'exadata_shape': 'exadataShape'
        }

        self._entity_source = None
        self._id = None
        self._compartment_id = None
        self._exadata_name = None
        self._exadata_display_name = None
        self._exadata_type = None
        self._exadata_rack_type = None
        self._is_virtualized_exadata = None
        self._status = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._exadata_infra_id = None
        self._exadata_infra_resource_type = None
        self._exadata_shape = None
        self._entity_source = 'PE_COMANAGED_EXADATA'

    @property
    def exadata_infra_id(self):
        """
        **[Required]** Gets the exadata_infra_id of this PeComanagedExadataInsight.
        The `OCID`__ of the Exadata Infrastructure.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The exadata_infra_id of this PeComanagedExadataInsight.
        :rtype: str
        """
        return self._exadata_infra_id

    @exadata_infra_id.setter
    def exadata_infra_id(self, exadata_infra_id):
        """
        Sets the exadata_infra_id of this PeComanagedExadataInsight.
        The `OCID`__ of the Exadata Infrastructure.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param exadata_infra_id: The exadata_infra_id of this PeComanagedExadataInsight.
        :type: str
        """
        self._exadata_infra_id = exadata_infra_id

    @property
    def exadata_infra_resource_type(self):
        """
        **[Required]** Gets the exadata_infra_resource_type of this PeComanagedExadataInsight.
        OCI exadata infrastructure resource type

        Allowed values for this property are: "cloudExadataInfrastructure", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The exadata_infra_resource_type of this PeComanagedExadataInsight.
        :rtype: str
        """
        return self._exadata_infra_resource_type

    @exadata_infra_resource_type.setter
    def exadata_infra_resource_type(self, exadata_infra_resource_type):
        """
        Sets the exadata_infra_resource_type of this PeComanagedExadataInsight.
        OCI exadata infrastructure resource type


        :param exadata_infra_resource_type: The exadata_infra_resource_type of this PeComanagedExadataInsight.
        :type: str
        """
        allowed_values = ["cloudExadataInfrastructure"]
        if not value_allowed_none_or_none_sentinel(exadata_infra_resource_type, allowed_values):
            exadata_infra_resource_type = 'UNKNOWN_ENUM_VALUE'
        self._exadata_infra_resource_type = exadata_infra_resource_type

    @property
    def exadata_shape(self):
        """
        **[Required]** Gets the exadata_shape of this PeComanagedExadataInsight.
        The shape of the Exadata Infrastructure.


        :return: The exadata_shape of this PeComanagedExadataInsight.
        :rtype: str
        """
        return self._exadata_shape

    @exadata_shape.setter
    def exadata_shape(self, exadata_shape):
        """
        Sets the exadata_shape of this PeComanagedExadataInsight.
        The shape of the Exadata Infrastructure.


        :param exadata_shape: The exadata_shape of this PeComanagedExadataInsight.
        :type: str
        """
        self._exadata_shape = exadata_shape

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
