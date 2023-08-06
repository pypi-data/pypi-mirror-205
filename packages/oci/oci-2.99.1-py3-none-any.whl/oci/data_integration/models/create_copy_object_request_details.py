# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateCopyObjectRequestDetails(object):
    """
    Details of copy object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateCopyObjectRequestDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source_workspace_id:
            The value to assign to the source_workspace_id property of this CreateCopyObjectRequestDetails.
        :type source_workspace_id: str

        :param object_keys:
            The value to assign to the object_keys property of this CreateCopyObjectRequestDetails.
        :type object_keys: list[str]

        :param copy_conflict_resolution:
            The value to assign to the copy_conflict_resolution property of this CreateCopyObjectRequestDetails.
        :type copy_conflict_resolution: oci.data_integration.models.CopyConflictResolution

        """
        self.swagger_types = {
            'source_workspace_id': 'str',
            'object_keys': 'list[str]',
            'copy_conflict_resolution': 'CopyConflictResolution'
        }

        self.attribute_map = {
            'source_workspace_id': 'sourceWorkspaceId',
            'object_keys': 'objectKeys',
            'copy_conflict_resolution': 'copyConflictResolution'
        }

        self._source_workspace_id = None
        self._object_keys = None
        self._copy_conflict_resolution = None

    @property
    def source_workspace_id(self):
        """
        **[Required]** Gets the source_workspace_id of this CreateCopyObjectRequestDetails.
        The workspace id of the source from where we need to copy object.


        :return: The source_workspace_id of this CreateCopyObjectRequestDetails.
        :rtype: str
        """
        return self._source_workspace_id

    @source_workspace_id.setter
    def source_workspace_id(self, source_workspace_id):
        """
        Sets the source_workspace_id of this CreateCopyObjectRequestDetails.
        The workspace id of the source from where we need to copy object.


        :param source_workspace_id: The source_workspace_id of this CreateCopyObjectRequestDetails.
        :type: str
        """
        self._source_workspace_id = source_workspace_id

    @property
    def object_keys(self):
        """
        **[Required]** Gets the object_keys of this CreateCopyObjectRequestDetails.
        The list of the objects to be copied.


        :return: The object_keys of this CreateCopyObjectRequestDetails.
        :rtype: list[str]
        """
        return self._object_keys

    @object_keys.setter
    def object_keys(self, object_keys):
        """
        Sets the object_keys of this CreateCopyObjectRequestDetails.
        The list of the objects to be copied.


        :param object_keys: The object_keys of this CreateCopyObjectRequestDetails.
        :type: list[str]
        """
        self._object_keys = object_keys

    @property
    def copy_conflict_resolution(self):
        """
        **[Required]** Gets the copy_conflict_resolution of this CreateCopyObjectRequestDetails.

        :return: The copy_conflict_resolution of this CreateCopyObjectRequestDetails.
        :rtype: oci.data_integration.models.CopyConflictResolution
        """
        return self._copy_conflict_resolution

    @copy_conflict_resolution.setter
    def copy_conflict_resolution(self, copy_conflict_resolution):
        """
        Sets the copy_conflict_resolution of this CreateCopyObjectRequestDetails.

        :param copy_conflict_resolution: The copy_conflict_resolution of this CreateCopyObjectRequestDetails.
        :type: oci.data_integration.models.CopyConflictResolution
        """
        self._copy_conflict_resolution = copy_conflict_resolution

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
