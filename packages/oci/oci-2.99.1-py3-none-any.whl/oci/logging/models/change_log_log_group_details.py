# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ChangeLogLogGroupDetails(object):
    """
    Contains details indicating which log group the log should move to.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ChangeLogLogGroupDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param target_log_group_id:
            The value to assign to the target_log_group_id property of this ChangeLogLogGroupDetails.
        :type target_log_group_id: str

        """
        self.swagger_types = {
            'target_log_group_id': 'str'
        }

        self.attribute_map = {
            'target_log_group_id': 'targetLogGroupId'
        }

        self._target_log_group_id = None

    @property
    def target_log_group_id(self):
        """
        Gets the target_log_group_id of this ChangeLogLogGroupDetails.
        Log group OCID.


        :return: The target_log_group_id of this ChangeLogLogGroupDetails.
        :rtype: str
        """
        return self._target_log_group_id

    @target_log_group_id.setter
    def target_log_group_id(self, target_log_group_id):
        """
        Sets the target_log_group_id of this ChangeLogLogGroupDetails.
        Log group OCID.


        :param target_log_group_id: The target_log_group_id of this ChangeLogLogGroupDetails.
        :type: str
        """
        self._target_log_group_id = target_log_group_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
