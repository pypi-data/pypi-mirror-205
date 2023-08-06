# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ObjectDetails(object):
    """
    Details of the Objectstorage object
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ObjectDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param object_namespace:
            The value to assign to the object_namespace property of this ObjectDetails.
        :type object_namespace: str

        :param object_bucket:
            The value to assign to the object_bucket property of this ObjectDetails.
        :type object_bucket: str

        :param object_name:
            The value to assign to the object_name property of this ObjectDetails.
        :type object_name: str

        :param object_url:
            The value to assign to the object_url property of this ObjectDetails.
        :type object_url: str

        :param checksum:
            The value to assign to the checksum property of this ObjectDetails.
        :type checksum: str

        """
        self.swagger_types = {
            'object_namespace': 'str',
            'object_bucket': 'str',
            'object_name': 'str',
            'object_url': 'str',
            'checksum': 'str'
        }

        self.attribute_map = {
            'object_namespace': 'objectNamespace',
            'object_bucket': 'objectBucket',
            'object_name': 'objectName',
            'object_url': 'objectUrl',
            'checksum': 'checksum'
        }

        self._object_namespace = None
        self._object_bucket = None
        self._object_name = None
        self._object_url = None
        self._checksum = None

    @property
    def object_namespace(self):
        """
        **[Required]** Gets the object_namespace of this ObjectDetails.
        Objectstorage namespace reference providing the original location of this object


        :return: The object_namespace of this ObjectDetails.
        :rtype: str
        """
        return self._object_namespace

    @object_namespace.setter
    def object_namespace(self, object_namespace):
        """
        Sets the object_namespace of this ObjectDetails.
        Objectstorage namespace reference providing the original location of this object


        :param object_namespace: The object_namespace of this ObjectDetails.
        :type: str
        """
        self._object_namespace = object_namespace

    @property
    def object_bucket(self):
        """
        **[Required]** Gets the object_bucket of this ObjectDetails.
        Objectstorage bucket reference providing the original location of this object


        :return: The object_bucket of this ObjectDetails.
        :rtype: str
        """
        return self._object_bucket

    @object_bucket.setter
    def object_bucket(self, object_bucket):
        """
        Sets the object_bucket of this ObjectDetails.
        Objectstorage bucket reference providing the original location of this object


        :param object_bucket: The object_bucket of this ObjectDetails.
        :type: str
        """
        self._object_bucket = object_bucket

    @property
    def object_name(self):
        """
        **[Required]** Gets the object_name of this ObjectDetails.
        Objectstorage object name reference providing the original location of this object


        :return: The object_name of this ObjectDetails.
        :rtype: str
        """
        return self._object_name

    @object_name.setter
    def object_name(self, object_name):
        """
        Sets the object_name of this ObjectDetails.
        Objectstorage object name reference providing the original location of this object


        :param object_name: The object_name of this ObjectDetails.
        :type: str
        """
        self._object_name = object_name

    @property
    def object_url(self):
        """
        Gets the object_url of this ObjectDetails.
        Object storage URL for download


        :return: The object_url of this ObjectDetails.
        :rtype: str
        """
        return self._object_url

    @object_url.setter
    def object_url(self, object_url):
        """
        Sets the object_url of this ObjectDetails.
        Object storage URL for download


        :param object_url: The object_url of this ObjectDetails.
        :type: str
        """
        self._object_url = object_url

    @property
    def checksum(self):
        """
        Gets the checksum of this ObjectDetails.
        Object content SHA256 Hash


        :return: The checksum of this ObjectDetails.
        :rtype: str
        """
        return self._checksum

    @checksum.setter
    def checksum(self, checksum):
        """
        Sets the checksum of this ObjectDetails.
        Object content SHA256 Hash


        :param checksum: The checksum of this ObjectDetails.
        :type: str
        """
        self._checksum = checksum

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
