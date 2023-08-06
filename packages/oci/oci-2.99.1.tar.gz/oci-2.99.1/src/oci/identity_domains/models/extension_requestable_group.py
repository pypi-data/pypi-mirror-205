# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionRequestableGroup(object):
    """
    Requestable Group
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionRequestableGroup object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param requestable:
            The value to assign to the requestable property of this ExtensionRequestableGroup.
        :type requestable: bool

        """
        self.swagger_types = {
            'requestable': 'bool'
        }

        self.attribute_map = {
            'requestable': 'requestable'
        }

        self._requestable = None

    @property
    def requestable(self):
        """
        Gets the requestable of this ExtensionRequestableGroup.
        Flag controlling whether group membership can be request by user through self service console.

        **Added In:** 17.3.4

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Requestable, mapsTo:requestable]]
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :return: The requestable of this ExtensionRequestableGroup.
        :rtype: bool
        """
        return self._requestable

    @requestable.setter
    def requestable(self, requestable):
        """
        Sets the requestable of this ExtensionRequestableGroup.
        Flag controlling whether group membership can be request by user through self service console.

        **Added In:** 17.3.4

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Requestable, mapsTo:requestable]]
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :param requestable: The requestable of this ExtensionRequestableGroup.
        :type: bool
        """
        self._requestable = requestable

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
