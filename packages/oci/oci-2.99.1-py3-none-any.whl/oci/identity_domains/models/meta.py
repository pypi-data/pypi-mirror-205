# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Meta(object):
    """
    A complex attribute that contains resource metadata. All sub-attributes are OPTIONAL.

    **SCIM++ Properties:**
    - caseExact: false
    - idcsSearchable: true
    - multiValued: false
    - mutability: readOnly
    - required: false
    - returned: default
    - idcsCsvAttributeNameMappings: [[columnHeaderName:Created Date, mapsTo:meta.created]]
    - type: complex
    """

    def __init__(self, **kwargs):
        """
        Initializes a new Meta object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param resource_type:
            The value to assign to the resource_type property of this Meta.
        :type resource_type: str

        :param created:
            The value to assign to the created property of this Meta.
        :type created: str

        :param last_modified:
            The value to assign to the last_modified property of this Meta.
        :type last_modified: str

        :param location:
            The value to assign to the location property of this Meta.
        :type location: str

        :param version:
            The value to assign to the version property of this Meta.
        :type version: str

        """
        self.swagger_types = {
            'resource_type': 'str',
            'created': 'str',
            'last_modified': 'str',
            'location': 'str',
            'version': 'str'
        }

        self.attribute_map = {
            'resource_type': 'resourceType',
            'created': 'created',
            'last_modified': 'lastModified',
            'location': 'location',
            'version': 'version'
        }

        self._resource_type = None
        self._created = None
        self._last_modified = None
        self._location = None
        self._version = None

    @property
    def resource_type(self):
        """
        Gets the resource_type of this Meta.
        Name of the resource type of the resource--for example, Users or Groups

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The resource_type of this Meta.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """
        Sets the resource_type of this Meta.
        Name of the resource type of the resource--for example, Users or Groups

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param resource_type: The resource_type of this Meta.
        :type: str
        """
        self._resource_type = resource_type

    @property
    def created(self):
        """
        Gets the created of this Meta.
        The DateTime the Resource was added to the Service Provider

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :return: The created of this Meta.
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created):
        """
        Sets the created of this Meta.
        The DateTime the Resource was added to the Service Provider

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :param created: The created of this Meta.
        :type: str
        """
        self._created = created

    @property
    def last_modified(self):
        """
        Gets the last_modified of this Meta.
        The most recent DateTime that the details of this Resource were updated at the Service Provider. If this Resource has never been modified since its initial creation, the value MUST be the same as the value of created. The attribute MUST be a DateTime.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :return: The last_modified of this Meta.
        :rtype: str
        """
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified):
        """
        Sets the last_modified of this Meta.
        The most recent DateTime that the details of this Resource were updated at the Service Provider. If this Resource has never been modified since its initial creation, the value MUST be the same as the value of created. The attribute MUST be a DateTime.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :param last_modified: The last_modified of this Meta.
        :type: str
        """
        self._last_modified = last_modified

    @property
    def location(self):
        """
        Gets the location of this Meta.
        The URI of the Resource being returned. This value MUST be the same as the Location HTTP response header.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The location of this Meta.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Sets the location of this Meta.
        The URI of the Resource being returned. This value MUST be the same as the Location HTTP response header.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param location: The location of this Meta.
        :type: str
        """
        self._location = location

    @property
    def version(self):
        """
        Gets the version of this Meta.
        The version of the Resource being returned. This value must be the same as the ETag HTTP response header.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The version of this Meta.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this Meta.
        The version of the Resource being returned. This value must be the same as the ETag HTTP response header.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param version: The version of this Meta.
        :type: str
        """
        self._version = version

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
