# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyDevice(object):
    """
    Device Resource.
    """

    #: A constant which can be used with the idcs_prevented_operations property of a MyDevice.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a MyDevice.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a MyDevice.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    #: A constant which can be used with the platform property of a MyDevice.
    #: This constant has a value of "IOS"
    PLATFORM_IOS = "IOS"

    #: A constant which can be used with the platform property of a MyDevice.
    #: This constant has a value of "ANDROID"
    PLATFORM_ANDROID = "ANDROID"

    #: A constant which can be used with the platform property of a MyDevice.
    #: This constant has a value of "WINDOWS"
    PLATFORM_WINDOWS = "WINDOWS"

    #: A constant which can be used with the platform property of a MyDevice.
    #: This constant has a value of "CELLULAR"
    PLATFORM_CELLULAR = "CELLULAR"

    #: A constant which can be used with the status property of a MyDevice.
    #: This constant has a value of "INITIATED"
    STATUS_INITIATED = "INITIATED"

    #: A constant which can be used with the status property of a MyDevice.
    #: This constant has a value of "INPROGRESS"
    STATUS_INPROGRESS = "INPROGRESS"

    #: A constant which can be used with the status property of a MyDevice.
    #: This constant has a value of "INACTIVE"
    STATUS_INACTIVE = "INACTIVE"

    #: A constant which can be used with the status property of a MyDevice.
    #: This constant has a value of "ENROLLED"
    STATUS_ENROLLED = "ENROLLED"

    #: A constant which can be used with the status property of a MyDevice.
    #: This constant has a value of "LOCKED"
    STATUS_LOCKED = "LOCKED"

    #: A constant which can be used with the status property of a MyDevice.
    #: This constant has a value of "BLOCKED"
    STATUS_BLOCKED = "BLOCKED"

    def __init__(self, **kwargs):
        """
        Initializes a new MyDevice object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this MyDevice.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this MyDevice.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this MyDevice.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this MyDevice.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this MyDevice.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this MyDevice.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this MyDevice.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this MyDevice.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this MyDevice.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this MyDevice.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this MyDevice.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this MyDevice.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this MyDevice.
        :type tenancy_ocid: str

        :param external_id:
            The value to assign to the external_id property of this MyDevice.
        :type external_id: str

        :param display_name:
            The value to assign to the display_name property of this MyDevice.
        :type display_name: str

        :param platform:
            The value to assign to the platform property of this MyDevice.
            Allowed values for this property are: "IOS", "ANDROID", "WINDOWS", "CELLULAR", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type platform: str

        :param status:
            The value to assign to the status property of this MyDevice.
            Allowed values for this property are: "INITIATED", "INPROGRESS", "INACTIVE", "ENROLLED", "LOCKED", "BLOCKED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param reason:
            The value to assign to the reason property of this MyDevice.
        :type reason: str

        :param device_type:
            The value to assign to the device_type property of this MyDevice.
        :type device_type: str

        :param app_version:
            The value to assign to the app_version property of this MyDevice.
        :type app_version: str

        :param package_id:
            The value to assign to the package_id property of this MyDevice.
        :type package_id: str

        :param last_sync_time:
            The value to assign to the last_sync_time property of this MyDevice.
        :type last_sync_time: str

        :param last_validated_time:
            The value to assign to the last_validated_time property of this MyDevice.
        :type last_validated_time: str

        :param is_compliant:
            The value to assign to the is_compliant property of this MyDevice.
        :type is_compliant: bool

        :param country_code:
            The value to assign to the country_code property of this MyDevice.
        :type country_code: str

        :param phone_number:
            The value to assign to the phone_number property of this MyDevice.
        :type phone_number: str

        :param is_acc_rec_enabled:
            The value to assign to the is_acc_rec_enabled property of this MyDevice.
        :type is_acc_rec_enabled: bool

        :param device_uuid:
            The value to assign to the device_uuid property of this MyDevice.
        :type device_uuid: str

        :param base_public_key:
            The value to assign to the base_public_key property of this MyDevice.
        :type base_public_key: str

        :param authentication_method:
            The value to assign to the authentication_method property of this MyDevice.
        :type authentication_method: str

        :param expires_on:
            The value to assign to the expires_on property of this MyDevice.
        :type expires_on: int

        :param seed_dek_id:
            The value to assign to the seed_dek_id property of this MyDevice.
        :type seed_dek_id: str

        :param seed:
            The value to assign to the seed property of this MyDevice.
        :type seed: str

        :param third_party_factor:
            The value to assign to the third_party_factor property of this MyDevice.
        :type third_party_factor: oci.identity_domains.models.MyDeviceThirdPartyFactor

        :param user:
            The value to assign to the user property of this MyDevice.
        :type user: oci.identity_domains.models.MyDeviceUser

        :param push_notification_target:
            The value to assign to the push_notification_target property of this MyDevice.
        :type push_notification_target: oci.identity_domains.models.MyDevicePushNotificationTarget

        :param additional_attributes:
            The value to assign to the additional_attributes property of this MyDevice.
        :type additional_attributes: list[oci.identity_domains.models.MyDeviceAdditionalAttributes]

        :param authentication_factors:
            The value to assign to the authentication_factors property of this MyDevice.
        :type authentication_factors: list[oci.identity_domains.models.MyDeviceAuthenticationFactors]

        :param non_compliances:
            The value to assign to the non_compliances property of this MyDevice.
        :type non_compliances: list[oci.identity_domains.models.MyDeviceNonCompliances]

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
            'external_id': 'str',
            'display_name': 'str',
            'platform': 'str',
            'status': 'str',
            'reason': 'str',
            'device_type': 'str',
            'app_version': 'str',
            'package_id': 'str',
            'last_sync_time': 'str',
            'last_validated_time': 'str',
            'is_compliant': 'bool',
            'country_code': 'str',
            'phone_number': 'str',
            'is_acc_rec_enabled': 'bool',
            'device_uuid': 'str',
            'base_public_key': 'str',
            'authentication_method': 'str',
            'expires_on': 'int',
            'seed_dek_id': 'str',
            'seed': 'str',
            'third_party_factor': 'MyDeviceThirdPartyFactor',
            'user': 'MyDeviceUser',
            'push_notification_target': 'MyDevicePushNotificationTarget',
            'additional_attributes': 'list[MyDeviceAdditionalAttributes]',
            'authentication_factors': 'list[MyDeviceAuthenticationFactors]',
            'non_compliances': 'list[MyDeviceNonCompliances]'
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
            'external_id': 'externalId',
            'display_name': 'displayName',
            'platform': 'platform',
            'status': 'status',
            'reason': 'reason',
            'device_type': 'deviceType',
            'app_version': 'appVersion',
            'package_id': 'packageId',
            'last_sync_time': 'lastSyncTime',
            'last_validated_time': 'lastValidatedTime',
            'is_compliant': 'isCompliant',
            'country_code': 'countryCode',
            'phone_number': 'phoneNumber',
            'is_acc_rec_enabled': 'isAccRecEnabled',
            'device_uuid': 'deviceUUID',
            'base_public_key': 'basePublicKey',
            'authentication_method': 'authenticationMethod',
            'expires_on': 'expiresOn',
            'seed_dek_id': 'seedDekId',
            'seed': 'seed',
            'third_party_factor': 'thirdPartyFactor',
            'user': 'user',
            'push_notification_target': 'pushNotificationTarget',
            'additional_attributes': 'additionalAttributes',
            'authentication_factors': 'authenticationFactors',
            'non_compliances': 'nonCompliances'
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
        self._external_id = None
        self._display_name = None
        self._platform = None
        self._status = None
        self._reason = None
        self._device_type = None
        self._app_version = None
        self._package_id = None
        self._last_sync_time = None
        self._last_validated_time = None
        self._is_compliant = None
        self._country_code = None
        self._phone_number = None
        self._is_acc_rec_enabled = None
        self._device_uuid = None
        self._base_public_key = None
        self._authentication_method = None
        self._expires_on = None
        self._seed_dek_id = None
        self._seed = None
        self._third_party_factor = None
        self._user = None
        self._push_notification_target = None
        self._additional_attributes = None
        self._authentication_factors = None
        self._non_compliances = None

    @property
    def id(self):
        """
        Gets the id of this MyDevice.
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


        :return: The id of this MyDevice.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this MyDevice.
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


        :param id: The id of this MyDevice.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this MyDevice.
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


        :return: The ocid of this MyDevice.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this MyDevice.
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


        :param ocid: The ocid of this MyDevice.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this MyDevice.
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


        :return: The schemas of this MyDevice.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this MyDevice.
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


        :param schemas: The schemas of this MyDevice.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this MyDevice.

        :return: The meta of this MyDevice.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this MyDevice.

        :param meta: The meta of this MyDevice.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this MyDevice.

        :return: The idcs_created_by of this MyDevice.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this MyDevice.

        :param idcs_created_by: The idcs_created_by of this MyDevice.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this MyDevice.

        :return: The idcs_last_modified_by of this MyDevice.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this MyDevice.

        :param idcs_last_modified_by: The idcs_last_modified_by of this MyDevice.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this MyDevice.
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


        :return: The idcs_prevented_operations of this MyDevice.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this MyDevice.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this MyDevice.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this MyDevice.
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


        :return: The tags of this MyDevice.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this MyDevice.
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


        :param tags: The tags of this MyDevice.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this MyDevice.
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


        :return: The delete_in_progress of this MyDevice.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this MyDevice.
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


        :param delete_in_progress: The delete_in_progress of this MyDevice.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this MyDevice.
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


        :return: The idcs_last_upgraded_in_release of this MyDevice.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this MyDevice.
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


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this MyDevice.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this MyDevice.
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


        :return: The domain_ocid of this MyDevice.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this MyDevice.
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


        :param domain_ocid: The domain_ocid of this MyDevice.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this MyDevice.
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


        :return: The compartment_ocid of this MyDevice.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this MyDevice.
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


        :param compartment_ocid: The compartment_ocid of this MyDevice.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this MyDevice.
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


        :return: The tenancy_ocid of this MyDevice.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this MyDevice.
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


        :param tenancy_ocid: The tenancy_ocid of this MyDevice.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def external_id(self):
        """
        Gets the external_id of this MyDevice.
        An identifier for the Resource as defined by the Service Consumer. The externalId may simplify identification of the Resource between Service Consumer and Service Provider by allowing the Consumer to refer to the Resource with its own identifier, obviating the need to store a local mapping between the local identifier of the Resource and the identifier used by the Service Provider. Each Resource MAY include a non-empty externalId value. The value of the externalId attribute is always issued be the Service Consumer and can never be specified by the Service Provider. The Service Provider MUST always interpret the externalId as scoped to the Service Consumer's tenant.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The external_id of this MyDevice.
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """
        Sets the external_id of this MyDevice.
        An identifier for the Resource as defined by the Service Consumer. The externalId may simplify identification of the Resource between Service Consumer and Service Provider by allowing the Consumer to refer to the Resource with its own identifier, obviating the need to store a local mapping between the local identifier of the Resource and the identifier used by the Service Provider. Each Resource MAY include a non-empty externalId value. The value of the externalId attribute is always issued be the Service Consumer and can never be specified by the Service Provider. The Service Provider MUST always interpret the externalId as scoped to the Service Consumer's tenant.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param external_id: The external_id of this MyDevice.
        :type: str
        """
        self._external_id = external_id

    @property
    def display_name(self):
        """
        Gets the display_name of this MyDevice.
        Device friendly display name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display_name of this MyDevice.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this MyDevice.
        Device friendly display name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display_name: The display_name of this MyDevice.
        :type: str
        """
        self._display_name = display_name

    @property
    def platform(self):
        """
        Gets the platform of this MyDevice.
        Device Platform

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "IOS", "ANDROID", "WINDOWS", "CELLULAR", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The platform of this MyDevice.
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """
        Sets the platform of this MyDevice.
        Device Platform

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param platform: The platform of this MyDevice.
        :type: str
        """
        allowed_values = ["IOS", "ANDROID", "WINDOWS", "CELLULAR"]
        if not value_allowed_none_or_none_sentinel(platform, allowed_values):
            platform = 'UNKNOWN_ENUM_VALUE'
        self._platform = platform

    @property
    def status(self):
        """
        Gets the status of this MyDevice.
        Device Status

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "INITIATED", "INPROGRESS", "INACTIVE", "ENROLLED", "LOCKED", "BLOCKED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this MyDevice.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this MyDevice.
        Device Status

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param status: The status of this MyDevice.
        :type: str
        """
        allowed_values = ["INITIATED", "INPROGRESS", "INACTIVE", "ENROLLED", "LOCKED", "BLOCKED"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def reason(self):
        """
        Gets the reason of this MyDevice.
        Additional comments/reasons for the change in device status

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The reason of this MyDevice.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this MyDevice.
        Additional comments/reasons for the change in device status

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param reason: The reason of this MyDevice.
        :type: str
        """
        self._reason = reason

    @property
    def device_type(self):
        """
        Gets the device_type of this MyDevice.
        Device hardware name/model

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The device_type of this MyDevice.
        :rtype: str
        """
        return self._device_type

    @device_type.setter
    def device_type(self, device_type):
        """
        Sets the device_type of this MyDevice.
        Device hardware name/model

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param device_type: The device_type of this MyDevice.
        :type: str
        """
        self._device_type = device_type

    @property
    def app_version(self):
        """
        Gets the app_version of this MyDevice.
        Mobile Authenticator App Version

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The app_version of this MyDevice.
        :rtype: str
        """
        return self._app_version

    @app_version.setter
    def app_version(self, app_version):
        """
        Sets the app_version of this MyDevice.
        Mobile Authenticator App Version

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param app_version: The app_version of this MyDevice.
        :type: str
        """
        self._app_version = app_version

    @property
    def package_id(self):
        """
        Gets the package_id of this MyDevice.
        Mobile Authenticator App Package Id

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The package_id of this MyDevice.
        :rtype: str
        """
        return self._package_id

    @package_id.setter
    def package_id(self, package_id):
        """
        Sets the package_id of this MyDevice.
        Mobile Authenticator App Package Id

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param package_id: The package_id of this MyDevice.
        :type: str
        """
        self._package_id = package_id

    @property
    def last_sync_time(self):
        """
        Gets the last_sync_time of this MyDevice.
        Last Sync time for device

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :return: The last_sync_time of this MyDevice.
        :rtype: str
        """
        return self._last_sync_time

    @last_sync_time.setter
    def last_sync_time(self, last_sync_time):
        """
        Sets the last_sync_time of this MyDevice.
        Last Sync time for device

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :param last_sync_time: The last_sync_time of this MyDevice.
        :type: str
        """
        self._last_sync_time = last_sync_time

    @property
    def last_validated_time(self):
        """
        Gets the last_validated_time of this MyDevice.
        The most recent timestamp when the device was successfully validated using one time passcode

        **Added In:** 17.3.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsAllowUpdatesInReadOnlyMode: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :return: The last_validated_time of this MyDevice.
        :rtype: str
        """
        return self._last_validated_time

    @last_validated_time.setter
    def last_validated_time(self, last_validated_time):
        """
        Sets the last_validated_time of this MyDevice.
        The most recent timestamp when the device was successfully validated using one time passcode

        **Added In:** 17.3.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsAllowUpdatesInReadOnlyMode: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: dateTime
         - uniqueness: none


        :param last_validated_time: The last_validated_time of this MyDevice.
        :type: str
        """
        self._last_validated_time = last_validated_time

    @property
    def is_compliant(self):
        """
        Gets the is_compliant of this MyDevice.
        Device Compliance Status

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The is_compliant of this MyDevice.
        :rtype: bool
        """
        return self._is_compliant

    @is_compliant.setter
    def is_compliant(self, is_compliant):
        """
        Sets the is_compliant of this MyDevice.
        Device Compliance Status

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param is_compliant: The is_compliant of this MyDevice.
        :type: bool
        """
        self._is_compliant = is_compliant

    @property
    def country_code(self):
        """
        Gets the country_code of this MyDevice.
        Country code of user's Phone Number

        **Added In:** 19.1.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The country_code of this MyDevice.
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """
        Sets the country_code of this MyDevice.
        Country code of user's Phone Number

        **Added In:** 19.1.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param country_code: The country_code of this MyDevice.
        :type: str
        """
        self._country_code = country_code

    @property
    def phone_number(self):
        """
        Gets the phone_number of this MyDevice.
        User's Phone Number

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The phone_number of this MyDevice.
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """
        Sets the phone_number of this MyDevice.
        User's Phone Number

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param phone_number: The phone_number of this MyDevice.
        :type: str
        """
        self._phone_number = phone_number

    @property
    def is_acc_rec_enabled(self):
        """
        Gets the is_acc_rec_enabled of this MyDevice.
        Flag that indicates whether the device is enrolled for account recovery

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The is_acc_rec_enabled of this MyDevice.
        :rtype: bool
        """
        return self._is_acc_rec_enabled

    @is_acc_rec_enabled.setter
    def is_acc_rec_enabled(self, is_acc_rec_enabled):
        """
        Sets the is_acc_rec_enabled of this MyDevice.
        Flag that indicates whether the device is enrolled for account recovery

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param is_acc_rec_enabled: The is_acc_rec_enabled of this MyDevice.
        :type: bool
        """
        self._is_acc_rec_enabled = is_acc_rec_enabled

    @property
    def device_uuid(self):
        """
        Gets the device_uuid of this MyDevice.
        Unique id sent from device

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The device_uuid of this MyDevice.
        :rtype: str
        """
        return self._device_uuid

    @device_uuid.setter
    def device_uuid(self, device_uuid):
        """
        Sets the device_uuid of this MyDevice.
        Unique id sent from device

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param device_uuid: The device_uuid of this MyDevice.
        :type: str
        """
        self._device_uuid = device_uuid

    @property
    def base_public_key(self):
        """
        Gets the base_public_key of this MyDevice.
        Device base public Key

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The base_public_key of this MyDevice.
        :rtype: str
        """
        return self._base_public_key

    @base_public_key.setter
    def base_public_key(self, base_public_key):
        """
        Sets the base_public_key of this MyDevice.
        Device base public Key

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param base_public_key: The base_public_key of this MyDevice.
        :type: str
        """
        self._base_public_key = base_public_key

    @property
    def authentication_method(self):
        """
        Gets the authentication_method of this MyDevice.
        Authentication method used in device. For FIDO, it will contain SECURITY_KEY/WINDOWS_HELLO etc

        **Added In:** 2009232244

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The authentication_method of this MyDevice.
        :rtype: str
        """
        return self._authentication_method

    @authentication_method.setter
    def authentication_method(self, authentication_method):
        """
        Sets the authentication_method of this MyDevice.
        Authentication method used in device. For FIDO, it will contain SECURITY_KEY/WINDOWS_HELLO etc

        **Added In:** 2009232244

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param authentication_method: The authentication_method of this MyDevice.
        :type: str
        """
        self._authentication_method = authentication_method

    @property
    def expires_on(self):
        """
        Gets the expires_on of this MyDevice.
        Attribute added for replication log, it is not used by IDCS, just added as place holder

        **Added In:** 2111040242

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The expires_on of this MyDevice.
        :rtype: int
        """
        return self._expires_on

    @expires_on.setter
    def expires_on(self, expires_on):
        """
        Sets the expires_on of this MyDevice.
        Attribute added for replication log, it is not used by IDCS, just added as place holder

        **Added In:** 2111040242

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param expires_on: The expires_on of this MyDevice.
        :type: int
        """
        self._expires_on = expires_on

    @property
    def seed_dek_id(self):
        """
        Gets the seed_dek_id of this MyDevice.
        Attribute added for replication log, it is not used by IDCS, the DEK that encrypts the specific seed for that user

        **Added In:** 2111040242

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The seed_dek_id of this MyDevice.
        :rtype: str
        """
        return self._seed_dek_id

    @seed_dek_id.setter
    def seed_dek_id(self, seed_dek_id):
        """
        Sets the seed_dek_id of this MyDevice.
        Attribute added for replication log, it is not used by IDCS, the DEK that encrypts the specific seed for that user

        **Added In:** 2111040242

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param seed_dek_id: The seed_dek_id of this MyDevice.
        :type: str
        """
        self._seed_dek_id = seed_dek_id

    @property
    def seed(self):
        """
        Gets the seed of this MyDevice.
        Attribute added for replication log, it is not used by IDCS, it is actual encrypted TOTP seed for the user

        **Added In:** 2111040242

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The seed of this MyDevice.
        :rtype: str
        """
        return self._seed

    @seed.setter
    def seed(self, seed):
        """
        Sets the seed of this MyDevice.
        Attribute added for replication log, it is not used by IDCS, it is actual encrypted TOTP seed for the user

        **Added In:** 2111040242

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param seed: The seed of this MyDevice.
        :type: str
        """
        self._seed = seed

    @property
    def third_party_factor(self):
        """
        Gets the third_party_factor of this MyDevice.

        :return: The third_party_factor of this MyDevice.
        :rtype: oci.identity_domains.models.MyDeviceThirdPartyFactor
        """
        return self._third_party_factor

    @third_party_factor.setter
    def third_party_factor(self, third_party_factor):
        """
        Sets the third_party_factor of this MyDevice.

        :param third_party_factor: The third_party_factor of this MyDevice.
        :type: oci.identity_domains.models.MyDeviceThirdPartyFactor
        """
        self._third_party_factor = third_party_factor

    @property
    def user(self):
        """
        **[Required]** Gets the user of this MyDevice.

        :return: The user of this MyDevice.
        :rtype: oci.identity_domains.models.MyDeviceUser
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this MyDevice.

        :param user: The user of this MyDevice.
        :type: oci.identity_domains.models.MyDeviceUser
        """
        self._user = user

    @property
    def push_notification_target(self):
        """
        Gets the push_notification_target of this MyDevice.

        :return: The push_notification_target of this MyDevice.
        :rtype: oci.identity_domains.models.MyDevicePushNotificationTarget
        """
        return self._push_notification_target

    @push_notification_target.setter
    def push_notification_target(self, push_notification_target):
        """
        Sets the push_notification_target of this MyDevice.

        :param push_notification_target: The push_notification_target of this MyDevice.
        :type: oci.identity_domains.models.MyDevicePushNotificationTarget
        """
        self._push_notification_target = push_notification_target

    @property
    def additional_attributes(self):
        """
        Gets the additional_attributes of this MyDevice.
        Device additional attributes

        **SCIM++ Properties:**
         - idcsCompositeKey: [key, value]
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: default
         - type: complex


        :return: The additional_attributes of this MyDevice.
        :rtype: list[oci.identity_domains.models.MyDeviceAdditionalAttributes]
        """
        return self._additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes):
        """
        Sets the additional_attributes of this MyDevice.
        Device additional attributes

        **SCIM++ Properties:**
         - idcsCompositeKey: [key, value]
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: default
         - type: complex


        :param additional_attributes: The additional_attributes of this MyDevice.
        :type: list[oci.identity_domains.models.MyDeviceAdditionalAttributes]
        """
        self._additional_attributes = additional_attributes

    @property
    def authentication_factors(self):
        """
        **[Required]** Gets the authentication_factors of this MyDevice.
        Authentication Factors

        **SCIM++ Properties:**
         - caseExact: true
         - idcsCompositeKey: [type]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: true
         - returned: default
         - type: complex


        :return: The authentication_factors of this MyDevice.
        :rtype: list[oci.identity_domains.models.MyDeviceAuthenticationFactors]
        """
        return self._authentication_factors

    @authentication_factors.setter
    def authentication_factors(self, authentication_factors):
        """
        Sets the authentication_factors of this MyDevice.
        Authentication Factors

        **SCIM++ Properties:**
         - caseExact: true
         - idcsCompositeKey: [type]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: true
         - returned: default
         - type: complex


        :param authentication_factors: The authentication_factors of this MyDevice.
        :type: list[oci.identity_domains.models.MyDeviceAuthenticationFactors]
        """
        self._authentication_factors = authentication_factors

    @property
    def non_compliances(self):
        """
        Gets the non_compliances of this MyDevice.
        Device Non Compliances

        **SCIM++ Properties:**
         - idcsCompositeKey: [name, value]
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: default
         - type: complex


        :return: The non_compliances of this MyDevice.
        :rtype: list[oci.identity_domains.models.MyDeviceNonCompliances]
        """
        return self._non_compliances

    @non_compliances.setter
    def non_compliances(self, non_compliances):
        """
        Sets the non_compliances of this MyDevice.
        Device Non Compliances

        **SCIM++ Properties:**
         - idcsCompositeKey: [name, value]
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: default
         - type: complex


        :param non_compliances: The non_compliances of this MyDevice.
        :type: list[oci.identity_domains.models.MyDeviceNonCompliances]
        """
        self._non_compliances = non_compliances

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
