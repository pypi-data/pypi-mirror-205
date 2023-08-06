# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DownloadMaskingLogDetails(object):
    """
    Details to download masking log.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DownloadMaskingLogDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param target_id:
            The value to assign to the target_id property of this DownloadMaskingLogDetails.
        :type target_id: str

        :param masking_work_request_id:
            The value to assign to the masking_work_request_id property of this DownloadMaskingLogDetails.
        :type masking_work_request_id: str

        """
        self.swagger_types = {
            'target_id': 'str',
            'masking_work_request_id': 'str'
        }

        self.attribute_map = {
            'target_id': 'targetId',
            'masking_work_request_id': 'maskingWorkRequestId'
        }

        self._target_id = None
        self._masking_work_request_id = None

    @property
    def target_id(self):
        """
        Gets the target_id of this DownloadMaskingLogDetails.
        The OCID of the target database for which the masking log is to be downloaded.


        :return: The target_id of this DownloadMaskingLogDetails.
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """
        Sets the target_id of this DownloadMaskingLogDetails.
        The OCID of the target database for which the masking log is to be downloaded.


        :param target_id: The target_id of this DownloadMaskingLogDetails.
        :type: str
        """
        self._target_id = target_id

    @property
    def masking_work_request_id(self):
        """
        Gets the masking_work_request_id of this DownloadMaskingLogDetails.
        The OCID of the masking work request that resulted in this masking log.


        :return: The masking_work_request_id of this DownloadMaskingLogDetails.
        :rtype: str
        """
        return self._masking_work_request_id

    @masking_work_request_id.setter
    def masking_work_request_id(self, masking_work_request_id):
        """
        Sets the masking_work_request_id of this DownloadMaskingLogDetails.
        The OCID of the masking work request that resulted in this masking log.


        :param masking_work_request_id: The masking_work_request_id of this DownloadMaskingLogDetails.
        :type: str
        """
        self._masking_work_request_id = masking_work_request_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
