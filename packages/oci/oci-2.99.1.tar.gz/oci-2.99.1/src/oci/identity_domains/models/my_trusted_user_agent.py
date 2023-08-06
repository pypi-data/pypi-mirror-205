# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyTrustedUserAgent(object):
    """
    This schema defines the attributes of Trusted User Agents owned by users. Multi-Factor Authentication uses Trusted User Agents to authenticate users.  A User Agent is software application that a user uses to issue requests.\r
    For example, a User Agent could be a particular browser (possibly one of several executing on a desktop or laptop) or a particular mobile application (again, one of several executing on a particular mobile device). \r
    A User Agent is trusted once the Multi-Factor Authentication has verified it in some way.
    """

    #: A constant which can be used with the idcs_prevented_operations property of a MyTrustedUserAgent.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a MyTrustedUserAgent.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a MyTrustedUserAgent.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    #: A constant which can be used with the token_type property of a MyTrustedUserAgent.
    #: This constant has a value of "KMSI"
    TOKEN_TYPE_KMSI = "KMSI"

    #: A constant which can be used with the token_type property of a MyTrustedUserAgent.
    #: This constant has a value of "TRUSTED"
    TOKEN_TYPE_TRUSTED = "TRUSTED"

    def __init__(self, **kwargs):
        """
        Initializes a new MyTrustedUserAgent object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this MyTrustedUserAgent.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this MyTrustedUserAgent.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this MyTrustedUserAgent.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this MyTrustedUserAgent.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this MyTrustedUserAgent.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this MyTrustedUserAgent.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this MyTrustedUserAgent.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this MyTrustedUserAgent.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this MyTrustedUserAgent.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this MyTrustedUserAgent.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this MyTrustedUserAgent.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this MyTrustedUserAgent.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this MyTrustedUserAgent.
        :type tenancy_ocid: str

        :param name:
            The value to assign to the name property of this MyTrustedUserAgent.
        :type name: str

        :param trust_token:
            The value to assign to the trust_token property of this MyTrustedUserAgent.
        :type trust_token: str

        :param location:
            The value to assign to the location property of this MyTrustedUserAgent.
        :type location: str

        :param platform:
            The value to assign to the platform property of this MyTrustedUserAgent.
        :type platform: str

        :param expiry_time:
            The value to assign to the expiry_time property of this MyTrustedUserAgent.
        :type expiry_time: str

        :param last_used_on:
            The value to assign to the last_used_on property of this MyTrustedUserAgent.
        :type last_used_on: str

        :param token_type:
            The value to assign to the token_type property of this MyTrustedUserAgent.
            Allowed values for this property are: "KMSI", "TRUSTED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type token_type: str

        :param trusted_factors:
            The value to assign to the trusted_factors property of this MyTrustedUserAgent.
        :type trusted_factors: list[oci.identity_domains.models.MyTrustedUserAgentTrustedFactors]

        :param user:
            The value to assign to the user property of this MyTrustedUserAgent.
        :type user: oci.identity_domains.models.MyTrustedUserAgentUser

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
            'name': 'str',
            'trust_token': 'str',
            'location': 'str',
            'platform': 'str',
            'expiry_time': 'str',
            'last_used_on': 'str',
            'token_type': 'str',
            'trusted_factors': 'list[MyTrustedUserAgentTrustedFactors]',
            'user': 'MyTrustedUserAgentUser'
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
            'name': 'name',
            'trust_token': 'trustToken',
            'location': 'location',
            'platform': 'platform',
            'expiry_time': 'expiryTime',
            'last_used_on': 'lastUsedOn',
            'token_type': 'tokenType',
            'trusted_factors': 'trustedFactors',
            'user': 'user'
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
        self._name = None
        self._trust_token = None
        self._location = None
        self._platform = None
        self._expiry_time = None
        self._last_used_on = None
        self._token_type = None
        self._trusted_factors = None
        self._user = None

    @property
    def id(self):
        """
        Gets the id of this MyTrustedUserAgent.
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


        :return: The id of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this MyTrustedUserAgent.
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


        :param id: The id of this MyTrustedUserAgent.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this MyTrustedUserAgent.
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


        :return: The ocid of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this MyTrustedUserAgent.
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


        :param ocid: The ocid of this MyTrustedUserAgent.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this MyTrustedUserAgent.
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


        :return: The schemas of this MyTrustedUserAgent.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this MyTrustedUserAgent.
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


        :param schemas: The schemas of this MyTrustedUserAgent.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this MyTrustedUserAgent.

        :return: The meta of this MyTrustedUserAgent.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this MyTrustedUserAgent.

        :param meta: The meta of this MyTrustedUserAgent.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this MyTrustedUserAgent.

        :return: The idcs_created_by of this MyTrustedUserAgent.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this MyTrustedUserAgent.

        :param idcs_created_by: The idcs_created_by of this MyTrustedUserAgent.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this MyTrustedUserAgent.

        :return: The idcs_last_modified_by of this MyTrustedUserAgent.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this MyTrustedUserAgent.

        :param idcs_last_modified_by: The idcs_last_modified_by of this MyTrustedUserAgent.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this MyTrustedUserAgent.
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


        :return: The idcs_prevented_operations of this MyTrustedUserAgent.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this MyTrustedUserAgent.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this MyTrustedUserAgent.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this MyTrustedUserAgent.
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


        :return: The tags of this MyTrustedUserAgent.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this MyTrustedUserAgent.
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


        :param tags: The tags of this MyTrustedUserAgent.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this MyTrustedUserAgent.
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


        :return: The delete_in_progress of this MyTrustedUserAgent.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this MyTrustedUserAgent.
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


        :param delete_in_progress: The delete_in_progress of this MyTrustedUserAgent.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this MyTrustedUserAgent.
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


        :return: The idcs_last_upgraded_in_release of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this MyTrustedUserAgent.
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


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this MyTrustedUserAgent.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this MyTrustedUserAgent.
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


        :return: The domain_ocid of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this MyTrustedUserAgent.
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


        :param domain_ocid: The domain_ocid of this MyTrustedUserAgent.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this MyTrustedUserAgent.
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


        :return: The compartment_ocid of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this MyTrustedUserAgent.
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


        :param compartment_ocid: The compartment_ocid of this MyTrustedUserAgent.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this MyTrustedUserAgent.
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


        :return: The tenancy_ocid of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this MyTrustedUserAgent.
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


        :param tenancy_ocid: The tenancy_ocid of this MyTrustedUserAgent.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def name(self):
        """
        **[Required]** Gets the name of this MyTrustedUserAgent.
        The name of the User Agent that the user wants the system to trust and to use in Multi-Factor Authentication.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :return: The name of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this MyTrustedUserAgent.
        The name of the User Agent that the user wants the system to trust and to use in Multi-Factor Authentication.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :param name: The name of this MyTrustedUserAgent.
        :type: str
        """
        self._name = name

    @property
    def trust_token(self):
        """
        **[Required]** Gets the trust_token of this MyTrustedUserAgent.
        Trust token for the user agent. This is a random string value that will be updated whenever a token that has been issued is verified successfully.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - idcsSensitive: none
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :return: The trust_token of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._trust_token

    @trust_token.setter
    def trust_token(self, trust_token):
        """
        Sets the trust_token of this MyTrustedUserAgent.
        Trust token for the user agent. This is a random string value that will be updated whenever a token that has been issued is verified successfully.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - idcsSensitive: none
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :param trust_token: The trust_token of this MyTrustedUserAgent.
        :type: str
        """
        self._trust_token = trust_token

    @property
    def location(self):
        """
        Gets the location of this MyTrustedUserAgent.
        Trust token issued geo-location.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The location of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Sets the location of this MyTrustedUserAgent.
        Trust token issued geo-location.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param location: The location of this MyTrustedUserAgent.
        :type: str
        """
        self._location = location

    @property
    def platform(self):
        """
        Gets the platform of this MyTrustedUserAgent.
        User agent platform for which the trust token has been issued.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The platform of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """
        Sets the platform of this MyTrustedUserAgent.
        User agent platform for which the trust token has been issued.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param platform: The platform of this MyTrustedUserAgent.
        :type: str
        """
        self._platform = platform

    @property
    def expiry_time(self):
        """
        Gets the expiry_time of this MyTrustedUserAgent.
        Validation period of the trust token.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :return: The expiry_time of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._expiry_time

    @expiry_time.setter
    def expiry_time(self, expiry_time):
        """
        Sets the expiry_time of this MyTrustedUserAgent.
        Validation period of the trust token.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :param expiry_time: The expiry_time of this MyTrustedUserAgent.
        :type: str
        """
        self._expiry_time = expiry_time

    @property
    def last_used_on(self):
        """
        Gets the last_used_on of this MyTrustedUserAgent.
        Indicates when this token was used lastime.

        **Added In:** 2111190457

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :return: The last_used_on of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._last_used_on

    @last_used_on.setter
    def last_used_on(self, last_used_on):
        """
        Sets the last_used_on of this MyTrustedUserAgent.
        Indicates when this token was used lastime.

        **Added In:** 2111190457

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :param last_used_on: The last_used_on of this MyTrustedUserAgent.
        :type: str
        """
        self._last_used_on = last_used_on

    @property
    def token_type(self):
        """
        Gets the token_type of this MyTrustedUserAgent.
        The token type being created. This token is used as trusted and kmsi token.

        **Added In:** 2111190457

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "KMSI", "TRUSTED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The token_type of this MyTrustedUserAgent.
        :rtype: str
        """
        return self._token_type

    @token_type.setter
    def token_type(self, token_type):
        """
        Sets the token_type of this MyTrustedUserAgent.
        The token type being created. This token is used as trusted and kmsi token.

        **Added In:** 2111190457

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param token_type: The token_type of this MyTrustedUserAgent.
        :type: str
        """
        allowed_values = ["KMSI", "TRUSTED"]
        if not value_allowed_none_or_none_sentinel(token_type, allowed_values):
            token_type = 'UNKNOWN_ENUM_VALUE'
        self._token_type = token_type

    @property
    def trusted_factors(self):
        """
        Gets the trusted_factors of this MyTrustedUserAgent.
        Trusted 2FA Factors

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: true
         - idcsCompositeKey: [type]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex


        :return: The trusted_factors of this MyTrustedUserAgent.
        :rtype: list[oci.identity_domains.models.MyTrustedUserAgentTrustedFactors]
        """
        return self._trusted_factors

    @trusted_factors.setter
    def trusted_factors(self, trusted_factors):
        """
        Sets the trusted_factors of this MyTrustedUserAgent.
        Trusted 2FA Factors

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: true
         - idcsCompositeKey: [type]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex


        :param trusted_factors: The trusted_factors of this MyTrustedUserAgent.
        :type: list[oci.identity_domains.models.MyTrustedUserAgentTrustedFactors]
        """
        self._trusted_factors = trusted_factors

    @property
    def user(self):
        """
        **[Required]** Gets the user of this MyTrustedUserAgent.

        :return: The user of this MyTrustedUserAgent.
        :rtype: oci.identity_domains.models.MyTrustedUserAgentUser
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this MyTrustedUserAgent.

        :param user: The user of this MyTrustedUserAgent.
        :type: oci.identity_domains.models.MyTrustedUserAgentUser
        """
        self._user = user

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
