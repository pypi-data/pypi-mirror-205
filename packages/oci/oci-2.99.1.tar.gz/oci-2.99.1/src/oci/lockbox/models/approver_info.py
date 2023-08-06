# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ApproverInfo(object):
    """
    The approver data for this approver level.
    """

    #: A constant which can be used with the approver_type property of a ApproverInfo.
    #: This constant has a value of "GROUP"
    APPROVER_TYPE_GROUP = "GROUP"

    #: A constant which can be used with the approver_type property of a ApproverInfo.
    #: This constant has a value of "USER"
    APPROVER_TYPE_USER = "USER"

    def __init__(self, **kwargs):
        """
        Initializes a new ApproverInfo object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param approver_type:
            The value to assign to the approver_type property of this ApproverInfo.
            Allowed values for this property are: "GROUP", "USER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type approver_type: str

        :param approver_id:
            The value to assign to the approver_id property of this ApproverInfo.
        :type approver_id: str

        """
        self.swagger_types = {
            'approver_type': 'str',
            'approver_id': 'str'
        }

        self.attribute_map = {
            'approver_type': 'approverType',
            'approver_id': 'approverId'
        }

        self._approver_type = None
        self._approver_id = None

    @property
    def approver_type(self):
        """
        **[Required]** Gets the approver_type of this ApproverInfo.
        The approver type of this approver level.

        Allowed values for this property are: "GROUP", "USER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The approver_type of this ApproverInfo.
        :rtype: str
        """
        return self._approver_type

    @approver_type.setter
    def approver_type(self, approver_type):
        """
        Sets the approver_type of this ApproverInfo.
        The approver type of this approver level.


        :param approver_type: The approver_type of this ApproverInfo.
        :type: str
        """
        allowed_values = ["GROUP", "USER"]
        if not value_allowed_none_or_none_sentinel(approver_type, allowed_values):
            approver_type = 'UNKNOWN_ENUM_VALUE'
        self._approver_type = approver_type

    @property
    def approver_id(self):
        """
        **[Required]** Gets the approver_id of this ApproverInfo.
        The group or user ocid of the approver for this approver level.


        :return: The approver_id of this ApproverInfo.
        :rtype: str
        """
        return self._approver_id

    @approver_id.setter
    def approver_id(self, approver_id):
        """
        Sets the approver_id of this ApproverInfo.
        The group or user ocid of the approver for this approver level.


        :param approver_id: The approver_id of this ApproverInfo.
        :type: str
        """
        self._approver_id = approver_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
