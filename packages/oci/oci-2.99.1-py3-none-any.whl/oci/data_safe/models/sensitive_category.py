# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .sensitive_type import SensitiveType
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SensitiveCategory(SensitiveType):
    """
    Details of the sensitive category.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SensitiveCategory object with values from keyword arguments. The default value of the :py:attr:`~oci.data_safe.models.SensitiveCategory.entity_type` attribute
        of this class is ``SENSITIVE_CATEGORY`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this SensitiveCategory.
        :type id: str

        :param entity_type:
            The value to assign to the entity_type property of this SensitiveCategory.
            Allowed values for this property are: "SENSITIVE_TYPE", "SENSITIVE_CATEGORY"
        :type entity_type: str

        :param display_name:
            The value to assign to the display_name property of this SensitiveCategory.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this SensitiveCategory.
        :type compartment_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this SensitiveCategory.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"
        :type lifecycle_state: str

        :param short_name:
            The value to assign to the short_name property of this SensitiveCategory.
        :type short_name: str

        :param source:
            The value to assign to the source property of this SensitiveCategory.
            Allowed values for this property are: "ORACLE", "USER"
        :type source: str

        :param time_created:
            The value to assign to the time_created property of this SensitiveCategory.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this SensitiveCategory.
        :type time_updated: datetime

        :param description:
            The value to assign to the description property of this SensitiveCategory.
        :type description: str

        :param parent_category_id:
            The value to assign to the parent_category_id property of this SensitiveCategory.
        :type parent_category_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this SensitiveCategory.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this SensitiveCategory.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this SensitiveCategory.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'entity_type': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'lifecycle_state': 'str',
            'short_name': 'str',
            'source': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'description': 'str',
            'parent_category_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'entity_type': 'entityType',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'lifecycle_state': 'lifecycleState',
            'short_name': 'shortName',
            'source': 'source',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'description': 'description',
            'parent_category_id': 'parentCategoryId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._entity_type = None
        self._display_name = None
        self._compartment_id = None
        self._lifecycle_state = None
        self._short_name = None
        self._source = None
        self._time_created = None
        self._time_updated = None
        self._description = None
        self._parent_category_id = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._entity_type = 'SENSITIVE_CATEGORY'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
