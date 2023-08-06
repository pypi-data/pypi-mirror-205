# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SoftwarePackageFile(object):
    """
    A file associated with a package
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SoftwarePackageFile object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param path:
            The value to assign to the path property of this SoftwarePackageFile.
        :type path: str

        :param type:
            The value to assign to the type property of this SoftwarePackageFile.
        :type type: str

        :param time_modified:
            The value to assign to the time_modified property of this SoftwarePackageFile.
        :type time_modified: datetime

        :param checksum:
            The value to assign to the checksum property of this SoftwarePackageFile.
        :type checksum: str

        :param checksum_type:
            The value to assign to the checksum_type property of this SoftwarePackageFile.
        :type checksum_type: str

        :param size_in_bytes:
            The value to assign to the size_in_bytes property of this SoftwarePackageFile.
        :type size_in_bytes: int

        """
        self.swagger_types = {
            'path': 'str',
            'type': 'str',
            'time_modified': 'datetime',
            'checksum': 'str',
            'checksum_type': 'str',
            'size_in_bytes': 'int'
        }

        self.attribute_map = {
            'path': 'path',
            'type': 'type',
            'time_modified': 'timeModified',
            'checksum': 'checksum',
            'checksum_type': 'checksumType',
            'size_in_bytes': 'sizeInBytes'
        }

        self._path = None
        self._type = None
        self._time_modified = None
        self._checksum = None
        self._checksum_type = None
        self._size_in_bytes = None

    @property
    def path(self):
        """
        Gets the path of this SoftwarePackageFile.
        file path


        :return: The path of this SoftwarePackageFile.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path of this SoftwarePackageFile.
        file path


        :param path: The path of this SoftwarePackageFile.
        :type: str
        """
        self._path = path

    @property
    def type(self):
        """
        Gets the type of this SoftwarePackageFile.
        type of the file


        :return: The type of this SoftwarePackageFile.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this SoftwarePackageFile.
        type of the file


        :param type: The type of this SoftwarePackageFile.
        :type: str
        """
        self._type = type

    @property
    def time_modified(self):
        """
        Gets the time_modified of this SoftwarePackageFile.
        The date and time of the last modification to this file, as described
        in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_modified of this SoftwarePackageFile.
        :rtype: datetime
        """
        return self._time_modified

    @time_modified.setter
    def time_modified(self, time_modified):
        """
        Sets the time_modified of this SoftwarePackageFile.
        The date and time of the last modification to this file, as described
        in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_modified: The time_modified of this SoftwarePackageFile.
        :type: datetime
        """
        self._time_modified = time_modified

    @property
    def checksum(self):
        """
        Gets the checksum of this SoftwarePackageFile.
        checksum of the file


        :return: The checksum of this SoftwarePackageFile.
        :rtype: str
        """
        return self._checksum

    @checksum.setter
    def checksum(self, checksum):
        """
        Sets the checksum of this SoftwarePackageFile.
        checksum of the file


        :param checksum: The checksum of this SoftwarePackageFile.
        :type: str
        """
        self._checksum = checksum

    @property
    def checksum_type(self):
        """
        Gets the checksum_type of this SoftwarePackageFile.
        type of the checksum


        :return: The checksum_type of this SoftwarePackageFile.
        :rtype: str
        """
        return self._checksum_type

    @checksum_type.setter
    def checksum_type(self, checksum_type):
        """
        Sets the checksum_type of this SoftwarePackageFile.
        type of the checksum


        :param checksum_type: The checksum_type of this SoftwarePackageFile.
        :type: str
        """
        self._checksum_type = checksum_type

    @property
    def size_in_bytes(self):
        """
        Gets the size_in_bytes of this SoftwarePackageFile.
        size of the file in bytes


        :return: The size_in_bytes of this SoftwarePackageFile.
        :rtype: int
        """
        return self._size_in_bytes

    @size_in_bytes.setter
    def size_in_bytes(self, size_in_bytes):
        """
        Sets the size_in_bytes of this SoftwarePackageFile.
        size of the file in bytes


        :param size_in_bytes: The size_in_bytes of this SoftwarePackageFile.
        :type: int
        """
        self._size_in_bytes = size_in_bytes

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
