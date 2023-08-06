# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .connector_attribute import ConnectorAttribute
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalStorage(ConnectorAttribute):
    """
    BICC Connector Attribute.Object Storage as External storage where the BICC extracted files are written
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalStorage object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.ExternalStorage.model_type` attribute
        of this class is ``EXTERNAL_STORAGE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this ExternalStorage.
            Allowed values for this property are: "EXTERNAL_STORAGE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type model_type: str

        :param storage_id:
            The value to assign to the storage_id property of this ExternalStorage.
        :type storage_id: str

        :param storage_name:
            The value to assign to the storage_name property of this ExternalStorage.
        :type storage_name: str

        :param host:
            The value to assign to the host property of this ExternalStorage.
        :type host: str

        :param tenancy_id:
            The value to assign to the tenancy_id property of this ExternalStorage.
        :type tenancy_id: str

        :param namespace:
            The value to assign to the namespace property of this ExternalStorage.
        :type namespace: str

        :param bucket:
            The value to assign to the bucket property of this ExternalStorage.
        :type bucket: str

        """
        self.swagger_types = {
            'model_type': 'str',
            'storage_id': 'str',
            'storage_name': 'str',
            'host': 'str',
            'tenancy_id': 'str',
            'namespace': 'str',
            'bucket': 'str'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'storage_id': 'storageId',
            'storage_name': 'storageName',
            'host': 'host',
            'tenancy_id': 'tenancyId',
            'namespace': 'namespace',
            'bucket': 'bucket'
        }

        self._model_type = None
        self._storage_id = None
        self._storage_name = None
        self._host = None
        self._tenancy_id = None
        self._namespace = None
        self._bucket = None
        self._model_type = 'EXTERNAL_STORAGE'

    @property
    def storage_id(self):
        """
        Gets the storage_id of this ExternalStorage.
        Id of the external stoarge configured in BICC console. Usually its numeric.


        :return: The storage_id of this ExternalStorage.
        :rtype: str
        """
        return self._storage_id

    @storage_id.setter
    def storage_id(self, storage_id):
        """
        Sets the storage_id of this ExternalStorage.
        Id of the external stoarge configured in BICC console. Usually its numeric.


        :param storage_id: The storage_id of this ExternalStorage.
        :type: str
        """
        self._storage_id = storage_id

    @property
    def storage_name(self):
        """
        Gets the storage_name of this ExternalStorage.
        Name of the external storage configured in BICC console


        :return: The storage_name of this ExternalStorage.
        :rtype: str
        """
        return self._storage_name

    @storage_name.setter
    def storage_name(self, storage_name):
        """
        Sets the storage_name of this ExternalStorage.
        Name of the external storage configured in BICC console


        :param storage_name: The storage_name of this ExternalStorage.
        :type: str
        """
        self._storage_name = storage_name

    @property
    def host(self):
        """
        Gets the host of this ExternalStorage.
        Object Storage host Url. DO not give http/https.


        :return: The host of this ExternalStorage.
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """
        Sets the host of this ExternalStorage.
        Object Storage host Url. DO not give http/https.


        :param host: The host of this ExternalStorage.
        :type: str
        """
        self._host = host

    @property
    def tenancy_id(self):
        """
        Gets the tenancy_id of this ExternalStorage.
        Tenancy OCID for the OOS bucket


        :return: The tenancy_id of this ExternalStorage.
        :rtype: str
        """
        return self._tenancy_id

    @tenancy_id.setter
    def tenancy_id(self, tenancy_id):
        """
        Sets the tenancy_id of this ExternalStorage.
        Tenancy OCID for the OOS bucket


        :param tenancy_id: The tenancy_id of this ExternalStorage.
        :type: str
        """
        self._tenancy_id = tenancy_id

    @property
    def namespace(self):
        """
        Gets the namespace of this ExternalStorage.
        Namespace for the OOS bucket


        :return: The namespace of this ExternalStorage.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """
        Sets the namespace of this ExternalStorage.
        Namespace for the OOS bucket


        :param namespace: The namespace of this ExternalStorage.
        :type: str
        """
        self._namespace = namespace

    @property
    def bucket(self):
        """
        Gets the bucket of this ExternalStorage.
        Bucket Name where BICC extracts stores the files


        :return: The bucket of this ExternalStorage.
        :rtype: str
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """
        Sets the bucket of this ExternalStorage.
        Bucket Name where BICC extracts stores the files


        :param bucket: The bucket of this ExternalStorage.
        :type: str
        """
        self._bucket = bucket

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
