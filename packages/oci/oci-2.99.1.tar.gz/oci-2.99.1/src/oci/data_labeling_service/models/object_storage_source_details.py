# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .dataset_source_details import DatasetSourceDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ObjectStorageSourceDetails(DatasetSourceDetails):
    """
    Specifies the dataset location in object storage. This requires that all records are in this bucket, and under this prefix. We do not support a dataset with objects in arbitrary locations across buckets or prefixes.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ObjectStorageSourceDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.data_labeling_service.models.ObjectStorageSourceDetails.source_type` attribute
        of this class is ``OBJECT_STORAGE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source_type:
            The value to assign to the source_type property of this ObjectStorageSourceDetails.
            Allowed values for this property are: "OBJECT_STORAGE"
        :type source_type: str

        :param namespace:
            The value to assign to the namespace property of this ObjectStorageSourceDetails.
        :type namespace: str

        :param bucket:
            The value to assign to the bucket property of this ObjectStorageSourceDetails.
        :type bucket: str

        :param prefix:
            The value to assign to the prefix property of this ObjectStorageSourceDetails.
        :type prefix: str

        """
        self.swagger_types = {
            'source_type': 'str',
            'namespace': 'str',
            'bucket': 'str',
            'prefix': 'str'
        }

        self.attribute_map = {
            'source_type': 'sourceType',
            'namespace': 'namespace',
            'bucket': 'bucket',
            'prefix': 'prefix'
        }

        self._source_type = None
        self._namespace = None
        self._bucket = None
        self._prefix = None
        self._source_type = 'OBJECT_STORAGE'

    @property
    def namespace(self):
        """
        **[Required]** Gets the namespace of this ObjectStorageSourceDetails.
        The namespace of the bucket that contains the dataset data source.


        :return: The namespace of this ObjectStorageSourceDetails.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """
        Sets the namespace of this ObjectStorageSourceDetails.
        The namespace of the bucket that contains the dataset data source.


        :param namespace: The namespace of this ObjectStorageSourceDetails.
        :type: str
        """
        self._namespace = namespace

    @property
    def bucket(self):
        """
        **[Required]** Gets the bucket of this ObjectStorageSourceDetails.
        The object storage bucket that contains the dataset data source.


        :return: The bucket of this ObjectStorageSourceDetails.
        :rtype: str
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """
        Sets the bucket of this ObjectStorageSourceDetails.
        The object storage bucket that contains the dataset data source.


        :param bucket: The bucket of this ObjectStorageSourceDetails.
        :type: str
        """
        self._bucket = bucket

    @property
    def prefix(self):
        """
        Gets the prefix of this ObjectStorageSourceDetails.
        A common path prefix shared by the objects that make up the dataset. Except for the CSV file type, records are not generated for the objects whose names exactly match with the prefix.


        :return: The prefix of this ObjectStorageSourceDetails.
        :rtype: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """
        Sets the prefix of this ObjectStorageSourceDetails.
        A common path prefix shared by the objects that make up the dataset. Except for the CSV file type, records are not generated for the objects whose names exactly match with the prefix.


        :param prefix: The prefix of this ObjectStorageSourceDetails.
        :type: str
        """
        self._prefix = prefix

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
