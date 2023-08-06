# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyDeviceThirdPartyFactor(object):
    """
    User's third-party authentication factor details

    **Added In:** 19.2.1

    **SCIM++ Properties:**
    - idcsSearchable: false
    - multiValued: false
    - mutability: immutable
    - required: false
    - returned: default
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MyDeviceThirdPartyFactor object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param third_party_vendor_name:
            The value to assign to the third_party_vendor_name property of this MyDeviceThirdPartyFactor.
        :type third_party_vendor_name: str

        :param third_party_factor_type:
            The value to assign to the third_party_factor_type property of this MyDeviceThirdPartyFactor.
        :type third_party_factor_type: str

        :param value:
            The value to assign to the value property of this MyDeviceThirdPartyFactor.
        :type value: str

        :param ref:
            The value to assign to the ref property of this MyDeviceThirdPartyFactor.
        :type ref: str

        """
        self.swagger_types = {
            'third_party_vendor_name': 'str',
            'third_party_factor_type': 'str',
            'value': 'str',
            'ref': 'str'
        }

        self.attribute_map = {
            'third_party_vendor_name': 'thirdPartyVendorName',
            'third_party_factor_type': 'thirdPartyFactorType',
            'value': 'value',
            'ref': '$ref'
        }

        self._third_party_vendor_name = None
        self._third_party_factor_type = None
        self._value = None
        self._ref = None

    @property
    def third_party_vendor_name(self):
        """
        **[Required]** Gets the third_party_vendor_name of this MyDeviceThirdPartyFactor.
        The vendor name of the third party factor

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The third_party_vendor_name of this MyDeviceThirdPartyFactor.
        :rtype: str
        """
        return self._third_party_vendor_name

    @third_party_vendor_name.setter
    def third_party_vendor_name(self, third_party_vendor_name):
        """
        Sets the third_party_vendor_name of this MyDeviceThirdPartyFactor.
        The vendor name of the third party factor

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param third_party_vendor_name: The third_party_vendor_name of this MyDeviceThirdPartyFactor.
        :type: str
        """
        self._third_party_vendor_name = third_party_vendor_name

    @property
    def third_party_factor_type(self):
        """
        Gets the third_party_factor_type of this MyDeviceThirdPartyFactor.
        Type of the third party authentication factor

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The third_party_factor_type of this MyDeviceThirdPartyFactor.
        :rtype: str
        """
        return self._third_party_factor_type

    @third_party_factor_type.setter
    def third_party_factor_type(self, third_party_factor_type):
        """
        Sets the third_party_factor_type of this MyDeviceThirdPartyFactor.
        Type of the third party authentication factor

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param third_party_factor_type: The third_party_factor_type of this MyDeviceThirdPartyFactor.
        :type: str
        """
        self._third_party_factor_type = third_party_factor_type

    @property
    def value(self):
        """
        **[Required]** Gets the value of this MyDeviceThirdPartyFactor.
        The identifier of third party device

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this MyDeviceThirdPartyFactor.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this MyDeviceThirdPartyFactor.
        The identifier of third party device

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this MyDeviceThirdPartyFactor.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this MyDeviceThirdPartyFactor.
        The URI that corresponds to the third party device resource

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this MyDeviceThirdPartyFactor.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this MyDeviceThirdPartyFactor.
        The URI that corresponds to the third party device resource

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this MyDeviceThirdPartyFactor.
        :type: str
        """
        self._ref = ref

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
