# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .association import Association
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TenancyAssociation(Association):
    """
    Tenancy association represents the tenancy id to which the governance rule will be applied.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new TenancyAssociation object with values from keyword arguments. The default value of the :py:attr:`~oci.governance_rules_control_plane.models.TenancyAssociation.type` attribute
        of this class is ``TENANCY`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this TenancyAssociation.
        :type type: str

        :param tenancy_id:
            The value to assign to the tenancy_id property of this TenancyAssociation.
        :type tenancy_id: str

        """
        self.swagger_types = {
            'type': 'str',
            'tenancy_id': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'tenancy_id': 'tenancyId'
        }

        self._type = None
        self._tenancy_id = None
        self._type = 'TENANCY'

    @property
    def tenancy_id(self):
        """
        **[Required]** Gets the tenancy_id of this TenancyAssociation.
        The Oracle ID (`OCID`__) of the tenancy to which the governance rule will be applied as part of this tenancy inclusion criterion.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The tenancy_id of this TenancyAssociation.
        :rtype: str
        """
        return self._tenancy_id

    @tenancy_id.setter
    def tenancy_id(self, tenancy_id):
        """
        Sets the tenancy_id of this TenancyAssociation.
        The Oracle ID (`OCID`__) of the tenancy to which the governance rule will be applied as part of this tenancy inclusion criterion.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param tenancy_id: The tenancy_id of this TenancyAssociation.
        :type: str
        """
        self._tenancy_id = tenancy_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
