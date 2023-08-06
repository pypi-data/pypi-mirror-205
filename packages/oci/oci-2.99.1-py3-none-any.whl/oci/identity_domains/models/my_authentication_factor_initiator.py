# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyAuthenticationFactorInitiator(object):
    """
    This schema defines the attributes of Initiator call.
    """

    #: A constant which can be used with the idcs_prevented_operations property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "EMAIL"
    AUTH_FACTOR_EMAIL = "EMAIL"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "TOTP"
    AUTH_FACTOR_TOTP = "TOTP"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "PUSH"
    AUTH_FACTOR_PUSH = "PUSH"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "SMS"
    AUTH_FACTOR_SMS = "SMS"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "VOICE"
    AUTH_FACTOR_VOICE = "VOICE"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "PHONE_CALL"
    AUTH_FACTOR_PHONE_CALL = "PHONE_CALL"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "THIRDPARTY"
    AUTH_FACTOR_THIRDPARTY = "THIRDPARTY"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "FIDO_AUTHENTICATOR"
    AUTH_FACTOR_FIDO_AUTHENTICATOR = "FIDO_AUTHENTICATOR"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "YUBICO_OTP"
    AUTH_FACTOR_YUBICO_OTP = "YUBICO_OTP"

    #: A constant which can be used with the type property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "SAML"
    TYPE_SAML = "SAML"

    #: A constant which can be used with the type property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "OIDC"
    TYPE_OIDC = "OIDC"

    #: A constant which can be used with the scenario property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "ENROLLMENT"
    SCENARIO_ENROLLMENT = "ENROLLMENT"

    #: A constant which can be used with the scenario property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "AUTHENTICATION"
    SCENARIO_AUTHENTICATION = "AUTHENTICATION"

    #: A constant which can be used with the preference_type property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "PASSWORDLESS"
    PREFERENCE_TYPE_PASSWORDLESS = "PASSWORDLESS"

    #: A constant which can be used with the preference_type property of a MyAuthenticationFactorInitiator.
    #: This constant has a value of "MFA"
    PREFERENCE_TYPE_MFA = "MFA"

    def __init__(self, **kwargs):
        """
        Initializes a new MyAuthenticationFactorInitiator object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this MyAuthenticationFactorInitiator.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this MyAuthenticationFactorInitiator.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this MyAuthenticationFactorInitiator.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this MyAuthenticationFactorInitiator.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this MyAuthenticationFactorInitiator.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this MyAuthenticationFactorInitiator.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this MyAuthenticationFactorInitiator.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this MyAuthenticationFactorInitiator.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this MyAuthenticationFactorInitiator.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this MyAuthenticationFactorInitiator.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this MyAuthenticationFactorInitiator.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this MyAuthenticationFactorInitiator.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this MyAuthenticationFactorInitiator.
        :type tenancy_ocid: str

        :param auth_factor:
            The value to assign to the auth_factor property of this MyAuthenticationFactorInitiator.
            Allowed values for this property are: "EMAIL", "TOTP", "PUSH", "SMS", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type auth_factor: str

        :param device_id:
            The value to assign to the device_id property of this MyAuthenticationFactorInitiator.
        :type device_id: str

        :param type:
            The value to assign to the type property of this MyAuthenticationFactorInitiator.
            Allowed values for this property are: "SAML", "OIDC", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param request_id:
            The value to assign to the request_id property of this MyAuthenticationFactorInitiator.
        :type request_id: str

        :param user_name:
            The value to assign to the user_name property of this MyAuthenticationFactorInitiator.
        :type user_name: str

        :param scenario:
            The value to assign to the scenario property of this MyAuthenticationFactorInitiator.
            Allowed values for this property are: "ENROLLMENT", "AUTHENTICATION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type scenario: str

        :param third_party_factor:
            The value to assign to the third_party_factor property of this MyAuthenticationFactorInitiator.
        :type third_party_factor: oci.identity_domains.models.MyAuthenticationFactorInitiatorThirdPartyFactor

        :param preference_type:
            The value to assign to the preference_type property of this MyAuthenticationFactorInitiator.
            Allowed values for this property are: "PASSWORDLESS", "MFA", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type preference_type: str

        :param additional_attributes:
            The value to assign to the additional_attributes property of this MyAuthenticationFactorInitiator.
        :type additional_attributes: list[oci.identity_domains.models.MyAuthenticationFactorInitiatorAdditionalAttributes]

        :param is_acc_rec_enabled:
            The value to assign to the is_acc_rec_enabled property of this MyAuthenticationFactorInitiator.
        :type is_acc_rec_enabled: bool

        """
        self.swagger_types = {
            'id': 'str',
            'ocid': 'str',
            'schemas': 'list[str]',
            'meta': 'Meta',
            'idcs_created_by': 'IdcsCreatedBy',
            'idcs_last_modified_by': 'IdcsLastModifiedBy',
            'idcs_prevented_operations': 'list[str]',
            'tags': 'list[Tags]',
            'delete_in_progress': 'bool',
            'idcs_last_upgraded_in_release': 'str',
            'domain_ocid': 'str',
            'compartment_ocid': 'str',
            'tenancy_ocid': 'str',
            'auth_factor': 'str',
            'device_id': 'str',
            'type': 'str',
            'request_id': 'str',
            'user_name': 'str',
            'scenario': 'str',
            'third_party_factor': 'MyAuthenticationFactorInitiatorThirdPartyFactor',
            'preference_type': 'str',
            'additional_attributes': 'list[MyAuthenticationFactorInitiatorAdditionalAttributes]',
            'is_acc_rec_enabled': 'bool'
        }

        self.attribute_map = {
            'id': 'id',
            'ocid': 'ocid',
            'schemas': 'schemas',
            'meta': 'meta',
            'idcs_created_by': 'idcsCreatedBy',
            'idcs_last_modified_by': 'idcsLastModifiedBy',
            'idcs_prevented_operations': 'idcsPreventedOperations',
            'tags': 'tags',
            'delete_in_progress': 'deleteInProgress',
            'idcs_last_upgraded_in_release': 'idcsLastUpgradedInRelease',
            'domain_ocid': 'domainOcid',
            'compartment_ocid': 'compartmentOcid',
            'tenancy_ocid': 'tenancyOcid',
            'auth_factor': 'authFactor',
            'device_id': 'deviceId',
            'type': 'type',
            'request_id': 'requestId',
            'user_name': 'userName',
            'scenario': 'scenario',
            'third_party_factor': 'thirdPartyFactor',
            'preference_type': 'preferenceType',
            'additional_attributes': 'additionalAttributes',
            'is_acc_rec_enabled': 'isAccRecEnabled'
        }

        self._id = None
        self._ocid = None
        self._schemas = None
        self._meta = None
        self._idcs_created_by = None
        self._idcs_last_modified_by = None
        self._idcs_prevented_operations = None
        self._tags = None
        self._delete_in_progress = None
        self._idcs_last_upgraded_in_release = None
        self._domain_ocid = None
        self._compartment_ocid = None
        self._tenancy_ocid = None
        self._auth_factor = None
        self._device_id = None
        self._type = None
        self._request_id = None
        self._user_name = None
        self._scenario = None
        self._third_party_factor = None
        self._preference_type = None
        self._additional_attributes = None
        self._is_acc_rec_enabled = None

    @property
    def id(self):
        """
        Gets the id of this MyAuthenticationFactorInitiator.
        Unique identifier for the SCIM Resource as defined by the Service Provider. Each representation of the Resource MUST include a non-empty id value. This identifier MUST be unique across the Service Provider's entire set of Resources. It MUST be a stable, non-reassignable identifier that does not change when the same Resource is returned in subsequent requests. The value of the id attribute is always issued by the Service Provider and MUST never be specified by the Service Consumer. bulkId: is a reserved keyword and MUST NOT be used in the unique identifier.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: always
         - type: string
         - uniqueness: global


        :return: The id of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this MyAuthenticationFactorInitiator.
        Unique identifier for the SCIM Resource as defined by the Service Provider. Each representation of the Resource MUST include a non-empty id value. This identifier MUST be unique across the Service Provider's entire set of Resources. It MUST be a stable, non-reassignable identifier that does not change when the same Resource is returned in subsequent requests. The value of the id attribute is always issued by the Service Provider and MUST never be specified by the Service Consumer. bulkId: is a reserved keyword and MUST NOT be used in the unique identifier.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: always
         - type: string
         - uniqueness: global


        :param id: The id of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this MyAuthenticationFactorInitiator.
        Unique OCI identifier for the SCIM Resource.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: global


        :return: The ocid of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this MyAuthenticationFactorInitiator.
        Unique OCI identifier for the SCIM Resource.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: global


        :param ocid: The ocid of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this MyAuthenticationFactorInitiator.
        REQUIRED. The schemas attribute is an array of Strings which allows introspection of the supported schema version for a SCIM representation as well any schema extensions supported by that representation. Each String value must be a unique URI. This specification defines URIs for User, Group, and a standard \\\"enterprise\\\" extension. All representations of SCIM schema MUST include a non-zero value array with value(s) of the URIs supported by that representation. Duplicate values MUST NOT be included. Value order is not specified and MUST not impact behavior.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The schemas of this MyAuthenticationFactorInitiator.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this MyAuthenticationFactorInitiator.
        REQUIRED. The schemas attribute is an array of Strings which allows introspection of the supported schema version for a SCIM representation as well any schema extensions supported by that representation. Each String value must be a unique URI. This specification defines URIs for User, Group, and a standard \\\"enterprise\\\" extension. All representations of SCIM schema MUST include a non-zero value array with value(s) of the URIs supported by that representation. Duplicate values MUST NOT be included. Value order is not specified and MUST not impact behavior.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param schemas: The schemas of this MyAuthenticationFactorInitiator.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this MyAuthenticationFactorInitiator.

        :return: The meta of this MyAuthenticationFactorInitiator.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this MyAuthenticationFactorInitiator.

        :param meta: The meta of this MyAuthenticationFactorInitiator.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this MyAuthenticationFactorInitiator.

        :return: The idcs_created_by of this MyAuthenticationFactorInitiator.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this MyAuthenticationFactorInitiator.

        :param idcs_created_by: The idcs_created_by of this MyAuthenticationFactorInitiator.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this MyAuthenticationFactorInitiator.

        :return: The idcs_last_modified_by of this MyAuthenticationFactorInitiator.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this MyAuthenticationFactorInitiator.

        :param idcs_last_modified_by: The idcs_last_modified_by of this MyAuthenticationFactorInitiator.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this MyAuthenticationFactorInitiator.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none

        Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The idcs_prevented_operations of this MyAuthenticationFactorInitiator.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this MyAuthenticationFactorInitiator.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this MyAuthenticationFactorInitiator.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this MyAuthenticationFactorInitiator.
        A list of tags on this resource.

        **SCIM++ Properties:**
         - idcsCompositeKey: [key, value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The tags of this MyAuthenticationFactorInitiator.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this MyAuthenticationFactorInitiator.
        A list of tags on this resource.

        **SCIM++ Properties:**
         - idcsCompositeKey: [key, value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param tags: The tags of this MyAuthenticationFactorInitiator.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this MyAuthenticationFactorInitiator.
        A boolean flag indicating this resource in the process of being deleted. Usually set to true when synchronous deletion of the resource would take too long.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The delete_in_progress of this MyAuthenticationFactorInitiator.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this MyAuthenticationFactorInitiator.
        A boolean flag indicating this resource in the process of being deleted. Usually set to true when synchronous deletion of the resource would take too long.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param delete_in_progress: The delete_in_progress of this MyAuthenticationFactorInitiator.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this MyAuthenticationFactorInitiator.
        The release number when the resource was upgraded.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :return: The idcs_last_upgraded_in_release of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this MyAuthenticationFactorInitiator.
        The release number when the resource was upgraded.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this MyAuthenticationFactorInitiator.
        OCI Domain Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The domain_ocid of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this MyAuthenticationFactorInitiator.
        OCI Domain Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param domain_ocid: The domain_ocid of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this MyAuthenticationFactorInitiator.
        OCI Compartment Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The compartment_ocid of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this MyAuthenticationFactorInitiator.
        OCI Compartment Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param compartment_ocid: The compartment_ocid of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this MyAuthenticationFactorInitiator.
        OCI Tenant Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The tenancy_ocid of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this MyAuthenticationFactorInitiator.
        OCI Tenant Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param tenancy_ocid: The tenancy_ocid of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def auth_factor(self):
        """
        **[Required]** Gets the auth_factor of this MyAuthenticationFactorInitiator.
        Auth Factor represents the type of multi-factor authentication channel for which the request has been initiated.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "EMAIL", "TOTP", "PUSH", "SMS", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The auth_factor of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._auth_factor

    @auth_factor.setter
    def auth_factor(self, auth_factor):
        """
        Sets the auth_factor of this MyAuthenticationFactorInitiator.
        Auth Factor represents the type of multi-factor authentication channel for which the request has been initiated.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param auth_factor: The auth_factor of this MyAuthenticationFactorInitiator.
        :type: str
        """
        allowed_values = ["EMAIL", "TOTP", "PUSH", "SMS", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP"]
        if not value_allowed_none_or_none_sentinel(auth_factor, allowed_values):
            auth_factor = 'UNKNOWN_ENUM_VALUE'
        self._auth_factor = auth_factor

    @property
    def device_id(self):
        """
        **[Required]** Gets the device_id of this MyAuthenticationFactorInitiator.
        Enrolled Device id on which the multi factor has been initiated.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The device_id of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._device_id

    @device_id.setter
    def device_id(self, device_id):
        """
        Sets the device_id of this MyAuthenticationFactorInitiator.
        Enrolled Device id on which the multi factor has been initiated.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param device_id: The device_id of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._device_id = device_id

    @property
    def type(self):
        """
        Gets the type of this MyAuthenticationFactorInitiator.
        Authentication flow type either SAML / OIDC

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "SAML", "OIDC", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this MyAuthenticationFactorInitiator.
        Authentication flow type either SAML / OIDC

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param type: The type of this MyAuthenticationFactorInitiator.
        :type: str
        """
        allowed_values = ["SAML", "OIDC"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def request_id(self):
        """
        Gets the request_id of this MyAuthenticationFactorInitiator.
        Unique RequestId generated for each initiator request.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The request_id of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this MyAuthenticationFactorInitiator.
        Unique RequestId generated for each initiator request.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param request_id: The request_id of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._request_id = request_id

    @property
    def user_name(self):
        """
        Gets the user_name of this MyAuthenticationFactorInitiator.
        Name of the user who initiates the request.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsPii: true


        :return: The user_name of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """
        Sets the user_name of this MyAuthenticationFactorInitiator.
        Name of the user who initiates the request.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsPii: true


        :param user_name: The user_name of this MyAuthenticationFactorInitiator.
        :type: str
        """
        self._user_name = user_name

    @property
    def scenario(self):
        """
        Gets the scenario of this MyAuthenticationFactorInitiator.
        Specifies the scenario to initiate.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false

        Allowed values for this property are: "ENROLLMENT", "AUTHENTICATION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The scenario of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._scenario

    @scenario.setter
    def scenario(self, scenario):
        """
        Sets the scenario of this MyAuthenticationFactorInitiator.
        Specifies the scenario to initiate.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param scenario: The scenario of this MyAuthenticationFactorInitiator.
        :type: str
        """
        allowed_values = ["ENROLLMENT", "AUTHENTICATION"]
        if not value_allowed_none_or_none_sentinel(scenario, allowed_values):
            scenario = 'UNKNOWN_ENUM_VALUE'
        self._scenario = scenario

    @property
    def third_party_factor(self):
        """
        Gets the third_party_factor of this MyAuthenticationFactorInitiator.

        :return: The third_party_factor of this MyAuthenticationFactorInitiator.
        :rtype: oci.identity_domains.models.MyAuthenticationFactorInitiatorThirdPartyFactor
        """
        return self._third_party_factor

    @third_party_factor.setter
    def third_party_factor(self, third_party_factor):
        """
        Sets the third_party_factor of this MyAuthenticationFactorInitiator.

        :param third_party_factor: The third_party_factor of this MyAuthenticationFactorInitiator.
        :type: oci.identity_domains.models.MyAuthenticationFactorInitiatorThirdPartyFactor
        """
        self._third_party_factor = third_party_factor

    @property
    def preference_type(self):
        """
        Gets the preference_type of this MyAuthenticationFactorInitiator.
        Indicates whether to user passwordless factor to be updated or mfa factor to be updated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none

        Allowed values for this property are: "PASSWORDLESS", "MFA", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The preference_type of this MyAuthenticationFactorInitiator.
        :rtype: str
        """
        return self._preference_type

    @preference_type.setter
    def preference_type(self, preference_type):
        """
        Sets the preference_type of this MyAuthenticationFactorInitiator.
        Indicates whether to user passwordless factor to be updated or mfa factor to be updated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param preference_type: The preference_type of this MyAuthenticationFactorInitiator.
        :type: str
        """
        allowed_values = ["PASSWORDLESS", "MFA"]
        if not value_allowed_none_or_none_sentinel(preference_type, allowed_values):
            preference_type = 'UNKNOWN_ENUM_VALUE'
        self._preference_type = preference_type

    @property
    def additional_attributes(self):
        """
        Gets the additional_attributes of this MyAuthenticationFactorInitiator.
        Additional attributes which will be sent as part of a push notification

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The additional_attributes of this MyAuthenticationFactorInitiator.
        :rtype: list[oci.identity_domains.models.MyAuthenticationFactorInitiatorAdditionalAttributes]
        """
        return self._additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes):
        """
        Sets the additional_attributes of this MyAuthenticationFactorInitiator.
        Additional attributes which will be sent as part of a push notification

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param additional_attributes: The additional_attributes of this MyAuthenticationFactorInitiator.
        :type: list[oci.identity_domains.models.MyAuthenticationFactorInitiatorAdditionalAttributes]
        """
        self._additional_attributes = additional_attributes

    @property
    def is_acc_rec_enabled(self):
        """
        Gets the is_acc_rec_enabled of this MyAuthenticationFactorInitiator.
        Flag indicates whether the device is enrolled in account recovery

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The is_acc_rec_enabled of this MyAuthenticationFactorInitiator.
        :rtype: bool
        """
        return self._is_acc_rec_enabled

    @is_acc_rec_enabled.setter
    def is_acc_rec_enabled(self, is_acc_rec_enabled):
        """
        Sets the is_acc_rec_enabled of this MyAuthenticationFactorInitiator.
        Flag indicates whether the device is enrolled in account recovery

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param is_acc_rec_enabled: The is_acc_rec_enabled of this MyAuthenticationFactorInitiator.
        :type: bool
        """
        self._is_acc_rec_enabled = is_acc_rec_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
