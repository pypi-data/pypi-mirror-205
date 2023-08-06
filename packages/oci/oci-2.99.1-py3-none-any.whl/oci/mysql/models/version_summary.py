# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VersionSummary(object):
    """
    A summary of the supported MySQL Versions families, and a list of their supported minor versions.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VersionSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param version_family:
            The value to assign to the version_family property of this VersionSummary.
        :type version_family: str

        :param versions:
            The value to assign to the versions property of this VersionSummary.
        :type versions: list[oci.mysql.models.Version]

        """
        self.swagger_types = {
            'version_family': 'str',
            'versions': 'list[Version]'
        }

        self.attribute_map = {
            'version_family': 'versionFamily',
            'versions': 'versions'
        }

        self._version_family = None
        self._versions = None

    @property
    def version_family(self):
        """
        Gets the version_family of this VersionSummary.
        A descriptive summary of a group of versions.


        :return: The version_family of this VersionSummary.
        :rtype: str
        """
        return self._version_family

    @version_family.setter
    def version_family(self, version_family):
        """
        Sets the version_family of this VersionSummary.
        A descriptive summary of a group of versions.


        :param version_family: The version_family of this VersionSummary.
        :type: str
        """
        self._version_family = version_family

    @property
    def versions(self):
        """
        **[Required]** Gets the versions of this VersionSummary.
        The list of supported MySQL Versions.


        :return: The versions of this VersionSummary.
        :rtype: list[oci.mysql.models.Version]
        """
        return self._versions

    @versions.setter
    def versions(self, versions):
        """
        Sets the versions of this VersionSummary.
        The list of supported MySQL Versions.


        :param versions: The versions of this VersionSummary.
        :type: list[oci.mysql.models.Version]
        """
        self._versions = versions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
