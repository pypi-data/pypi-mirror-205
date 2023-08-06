# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExportOpensearchClusterBackupDetails(object):
    """
    Information about the cluster backup to export.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExportOpensearchClusterBackupDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this ExportOpensearchClusterBackupDetails.
        :type compartment_id: str

        :param object_storage_namespace:
            The value to assign to the object_storage_namespace property of this ExportOpensearchClusterBackupDetails.
        :type object_storage_namespace: str

        :param object_storage_bucket_name:
            The value to assign to the object_storage_bucket_name property of this ExportOpensearchClusterBackupDetails.
        :type object_storage_bucket_name: str

        :param object_storage_prefix:
            The value to assign to the object_storage_prefix property of this ExportOpensearchClusterBackupDetails.
        :type object_storage_prefix: str

        :param snapshot_name:
            The value to assign to the snapshot_name property of this ExportOpensearchClusterBackupDetails.
        :type snapshot_name: str

        :param repository_name:
            The value to assign to the repository_name property of this ExportOpensearchClusterBackupDetails.
        :type repository_name: str

        :param prefix:
            The value to assign to the prefix property of this ExportOpensearchClusterBackupDetails.
        :type prefix: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ExportOpensearchClusterBackupDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this ExportOpensearchClusterBackupDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'object_storage_namespace': 'str',
            'object_storage_bucket_name': 'str',
            'object_storage_prefix': 'str',
            'snapshot_name': 'str',
            'repository_name': 'str',
            'prefix': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'object_storage_namespace': 'objectStorageNamespace',
            'object_storage_bucket_name': 'objectStorageBucketName',
            'object_storage_prefix': 'objectStoragePrefix',
            'snapshot_name': 'snapshotName',
            'repository_name': 'repositoryName',
            'prefix': 'prefix',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._compartment_id = None
        self._object_storage_namespace = None
        self._object_storage_bucket_name = None
        self._object_storage_prefix = None
        self._snapshot_name = None
        self._repository_name = None
        self._prefix = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this ExportOpensearchClusterBackupDetails.
        The OCID of the compartment where the Object Storage resources for the cluster backup are located.


        :return: The compartment_id of this ExportOpensearchClusterBackupDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExportOpensearchClusterBackupDetails.
        The OCID of the compartment where the Object Storage resources for the cluster backup are located.


        :param compartment_id: The compartment_id of this ExportOpensearchClusterBackupDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def object_storage_namespace(self):
        """
        **[Required]** Gets the object_storage_namespace of this ExportOpensearchClusterBackupDetails.
        The Object Storage namespace for the cluster backup export operation.


        :return: The object_storage_namespace of this ExportOpensearchClusterBackupDetails.
        :rtype: str
        """
        return self._object_storage_namespace

    @object_storage_namespace.setter
    def object_storage_namespace(self, object_storage_namespace):
        """
        Sets the object_storage_namespace of this ExportOpensearchClusterBackupDetails.
        The Object Storage namespace for the cluster backup export operation.


        :param object_storage_namespace: The object_storage_namespace of this ExportOpensearchClusterBackupDetails.
        :type: str
        """
        self._object_storage_namespace = object_storage_namespace

    @property
    def object_storage_bucket_name(self):
        """
        **[Required]** Gets the object_storage_bucket_name of this ExportOpensearchClusterBackupDetails.
        The name of the Object Storage bucket for the cluster backup export operation.


        :return: The object_storage_bucket_name of this ExportOpensearchClusterBackupDetails.
        :rtype: str
        """
        return self._object_storage_bucket_name

    @object_storage_bucket_name.setter
    def object_storage_bucket_name(self, object_storage_bucket_name):
        """
        Sets the object_storage_bucket_name of this ExportOpensearchClusterBackupDetails.
        The name of the Object Storage bucket for the cluster backup export operation.


        :param object_storage_bucket_name: The object_storage_bucket_name of this ExportOpensearchClusterBackupDetails.
        :type: str
        """
        self._object_storage_bucket_name = object_storage_bucket_name

    @property
    def object_storage_prefix(self):
        """
        Gets the object_storage_prefix of this ExportOpensearchClusterBackupDetails.
        The prefix within the Object Storage bucket for the cluster backup export operation.


        :return: The object_storage_prefix of this ExportOpensearchClusterBackupDetails.
        :rtype: str
        """
        return self._object_storage_prefix

    @object_storage_prefix.setter
    def object_storage_prefix(self, object_storage_prefix):
        """
        Sets the object_storage_prefix of this ExportOpensearchClusterBackupDetails.
        The prefix within the Object Storage bucket for the cluster backup export operation.


        :param object_storage_prefix: The object_storage_prefix of this ExportOpensearchClusterBackupDetails.
        :type: str
        """
        self._object_storage_prefix = object_storage_prefix

    @property
    def snapshot_name(self):
        """
        **[Required]** Gets the snapshot_name of this ExportOpensearchClusterBackupDetails.
        The name of the snapshot for the cluster backup export operation.


        :return: The snapshot_name of this ExportOpensearchClusterBackupDetails.
        :rtype: str
        """
        return self._snapshot_name

    @snapshot_name.setter
    def snapshot_name(self, snapshot_name):
        """
        Sets the snapshot_name of this ExportOpensearchClusterBackupDetails.
        The name of the snapshot for the cluster backup export operation.


        :param snapshot_name: The snapshot_name of this ExportOpensearchClusterBackupDetails.
        :type: str
        """
        self._snapshot_name = snapshot_name

    @property
    def repository_name(self):
        """
        **[Required]** Gets the repository_name of this ExportOpensearchClusterBackupDetails.
        The name of the repository containing the snapshots for the cluster backup export operation.


        :return: The repository_name of this ExportOpensearchClusterBackupDetails.
        :rtype: str
        """
        return self._repository_name

    @repository_name.setter
    def repository_name(self, repository_name):
        """
        Sets the repository_name of this ExportOpensearchClusterBackupDetails.
        The name of the repository containing the snapshots for the cluster backup export operation.


        :param repository_name: The repository_name of this ExportOpensearchClusterBackupDetails.
        :type: str
        """
        self._repository_name = repository_name

    @property
    def prefix(self):
        """
        **[Required]** Gets the prefix of this ExportOpensearchClusterBackupDetails.
        The prefix within object storage bucket for the cluster backup export operation.


        :return: The prefix of this ExportOpensearchClusterBackupDetails.
        :rtype: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """
        Sets the prefix of this ExportOpensearchClusterBackupDetails.
        The prefix within object storage bucket for the cluster backup export operation.


        :param prefix: The prefix of this ExportOpensearchClusterBackupDetails.
        :type: str
        """
        self._prefix = prefix

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this ExportOpensearchClusterBackupDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this ExportOpensearchClusterBackupDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this ExportOpensearchClusterBackupDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this ExportOpensearchClusterBackupDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this ExportOpensearchClusterBackupDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this ExportOpensearchClusterBackupDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this ExportOpensearchClusterBackupDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this ExportOpensearchClusterBackupDetails.
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
