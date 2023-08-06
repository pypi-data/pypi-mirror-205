# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PasswordPolicy(object):
    """
    PasswordPolicy resource.
    """

    #: A constant which can be used with the idcs_prevented_operations property of a PasswordPolicy.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a PasswordPolicy.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a PasswordPolicy.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    #: A constant which can be used with the password_strength property of a PasswordPolicy.
    #: This constant has a value of "Simple"
    PASSWORD_STRENGTH_SIMPLE = "Simple"

    #: A constant which can be used with the password_strength property of a PasswordPolicy.
    #: This constant has a value of "Standard"
    PASSWORD_STRENGTH_STANDARD = "Standard"

    #: A constant which can be used with the password_strength property of a PasswordPolicy.
    #: This constant has a value of "Custom"
    PASSWORD_STRENGTH_CUSTOM = "Custom"

    def __init__(self, **kwargs):
        """
        Initializes a new PasswordPolicy object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this PasswordPolicy.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this PasswordPolicy.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this PasswordPolicy.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this PasswordPolicy.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this PasswordPolicy.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this PasswordPolicy.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this PasswordPolicy.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this PasswordPolicy.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this PasswordPolicy.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this PasswordPolicy.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this PasswordPolicy.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this PasswordPolicy.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this PasswordPolicy.
        :type tenancy_ocid: str

        :param external_id:
            The value to assign to the external_id property of this PasswordPolicy.
        :type external_id: str

        :param name:
            The value to assign to the name property of this PasswordPolicy.
        :type name: str

        :param description:
            The value to assign to the description property of this PasswordPolicy.
        :type description: str

        :param max_length:
            The value to assign to the max_length property of this PasswordPolicy.
        :type max_length: int

        :param min_length:
            The value to assign to the min_length property of this PasswordPolicy.
        :type min_length: int

        :param min_alphas:
            The value to assign to the min_alphas property of this PasswordPolicy.
        :type min_alphas: int

        :param min_numerals:
            The value to assign to the min_numerals property of this PasswordPolicy.
        :type min_numerals: int

        :param min_alpha_numerals:
            The value to assign to the min_alpha_numerals property of this PasswordPolicy.
        :type min_alpha_numerals: int

        :param min_special_chars:
            The value to assign to the min_special_chars property of this PasswordPolicy.
        :type min_special_chars: int

        :param max_special_chars:
            The value to assign to the max_special_chars property of this PasswordPolicy.
        :type max_special_chars: int

        :param min_lower_case:
            The value to assign to the min_lower_case property of this PasswordPolicy.
        :type min_lower_case: int

        :param min_upper_case:
            The value to assign to the min_upper_case property of this PasswordPolicy.
        :type min_upper_case: int

        :param min_unique_chars:
            The value to assign to the min_unique_chars property of this PasswordPolicy.
        :type min_unique_chars: int

        :param max_repeated_chars:
            The value to assign to the max_repeated_chars property of this PasswordPolicy.
        :type max_repeated_chars: int

        :param starts_with_alphabet:
            The value to assign to the starts_with_alphabet property of this PasswordPolicy.
        :type starts_with_alphabet: bool

        :param first_name_disallowed:
            The value to assign to the first_name_disallowed property of this PasswordPolicy.
        :type first_name_disallowed: bool

        :param last_name_disallowed:
            The value to assign to the last_name_disallowed property of this PasswordPolicy.
        :type last_name_disallowed: bool

        :param user_name_disallowed:
            The value to assign to the user_name_disallowed property of this PasswordPolicy.
        :type user_name_disallowed: bool

        :param min_password_age:
            The value to assign to the min_password_age property of this PasswordPolicy.
        :type min_password_age: int

        :param password_expires_after:
            The value to assign to the password_expires_after property of this PasswordPolicy.
        :type password_expires_after: int

        :param password_expire_warning:
            The value to assign to the password_expire_warning property of this PasswordPolicy.
        :type password_expire_warning: int

        :param required_chars:
            The value to assign to the required_chars property of this PasswordPolicy.
        :type required_chars: str

        :param disallowed_chars:
            The value to assign to the disallowed_chars property of this PasswordPolicy.
        :type disallowed_chars: str

        :param allowed_chars:
            The value to assign to the allowed_chars property of this PasswordPolicy.
        :type allowed_chars: str

        :param disallowed_substrings:
            The value to assign to the disallowed_substrings property of this PasswordPolicy.
        :type disallowed_substrings: list[str]

        :param dictionary_word_disallowed:
            The value to assign to the dictionary_word_disallowed property of this PasswordPolicy.
        :type dictionary_word_disallowed: bool

        :param dictionary_location:
            The value to assign to the dictionary_location property of this PasswordPolicy.
        :type dictionary_location: str

        :param dictionary_delimiter:
            The value to assign to the dictionary_delimiter property of this PasswordPolicy.
        :type dictionary_delimiter: str

        :param max_incorrect_attempts:
            The value to assign to the max_incorrect_attempts property of this PasswordPolicy.
        :type max_incorrect_attempts: int

        :param lockout_duration:
            The value to assign to the lockout_duration property of this PasswordPolicy.
        :type lockout_duration: int

        :param num_passwords_in_history:
            The value to assign to the num_passwords_in_history property of this PasswordPolicy.
        :type num_passwords_in_history: int

        :param password_strength:
            The value to assign to the password_strength property of this PasswordPolicy.
            Allowed values for this property are: "Simple", "Standard", "Custom", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type password_strength: str

        :param force_password_reset:
            The value to assign to the force_password_reset property of this PasswordPolicy.
        :type force_password_reset: bool

        :param groups:
            The value to assign to the groups property of this PasswordPolicy.
        :type groups: list[oci.identity_domains.models.PasswordPolicyGroups]

        :param priority:
            The value to assign to the priority property of this PasswordPolicy.
        :type priority: int

        :param configured_password_policy_rules:
            The value to assign to the configured_password_policy_rules property of this PasswordPolicy.
        :type configured_password_policy_rules: list[oci.identity_domains.models.PasswordPolicyConfiguredPasswordPolicyRules]

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
            'name': 'str',
            'description': 'str',
            'max_length': 'int',
            'min_length': 'int',
            'min_alphas': 'int',
            'min_numerals': 'int',
            'min_alpha_numerals': 'int',
            'min_special_chars': 'int',
            'max_special_chars': 'int',
            'min_lower_case': 'int',
            'min_upper_case': 'int',
            'min_unique_chars': 'int',
            'max_repeated_chars': 'int',
            'starts_with_alphabet': 'bool',
            'first_name_disallowed': 'bool',
            'last_name_disallowed': 'bool',
            'user_name_disallowed': 'bool',
            'min_password_age': 'int',
            'password_expires_after': 'int',
            'password_expire_warning': 'int',
            'required_chars': 'str',
            'disallowed_chars': 'str',
            'allowed_chars': 'str',
            'disallowed_substrings': 'list[str]',
            'dictionary_word_disallowed': 'bool',
            'dictionary_location': 'str',
            'dictionary_delimiter': 'str',
            'max_incorrect_attempts': 'int',
            'lockout_duration': 'int',
            'num_passwords_in_history': 'int',
            'password_strength': 'str',
            'force_password_reset': 'bool',
            'groups': 'list[PasswordPolicyGroups]',
            'priority': 'int',
            'configured_password_policy_rules': 'list[PasswordPolicyConfiguredPasswordPolicyRules]'
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
            'name': 'name',
            'description': 'description',
            'max_length': 'maxLength',
            'min_length': 'minLength',
            'min_alphas': 'minAlphas',
            'min_numerals': 'minNumerals',
            'min_alpha_numerals': 'minAlphaNumerals',
            'min_special_chars': 'minSpecialChars',
            'max_special_chars': 'maxSpecialChars',
            'min_lower_case': 'minLowerCase',
            'min_upper_case': 'minUpperCase',
            'min_unique_chars': 'minUniqueChars',
            'max_repeated_chars': 'maxRepeatedChars',
            'starts_with_alphabet': 'startsWithAlphabet',
            'first_name_disallowed': 'firstNameDisallowed',
            'last_name_disallowed': 'lastNameDisallowed',
            'user_name_disallowed': 'userNameDisallowed',
            'min_password_age': 'minPasswordAge',
            'password_expires_after': 'passwordExpiresAfter',
            'password_expire_warning': 'passwordExpireWarning',
            'required_chars': 'requiredChars',
            'disallowed_chars': 'disallowedChars',
            'allowed_chars': 'allowedChars',
            'disallowed_substrings': 'disallowedSubstrings',
            'dictionary_word_disallowed': 'dictionaryWordDisallowed',
            'dictionary_location': 'dictionaryLocation',
            'dictionary_delimiter': 'dictionaryDelimiter',
            'max_incorrect_attempts': 'maxIncorrectAttempts',
            'lockout_duration': 'lockoutDuration',
            'num_passwords_in_history': 'numPasswordsInHistory',
            'password_strength': 'passwordStrength',
            'force_password_reset': 'forcePasswordReset',
            'groups': 'groups',
            'priority': 'priority',
            'configured_password_policy_rules': 'configuredPasswordPolicyRules'
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
        self._name = None
        self._description = None
        self._max_length = None
        self._min_length = None
        self._min_alphas = None
        self._min_numerals = None
        self._min_alpha_numerals = None
        self._min_special_chars = None
        self._max_special_chars = None
        self._min_lower_case = None
        self._min_upper_case = None
        self._min_unique_chars = None
        self._max_repeated_chars = None
        self._starts_with_alphabet = None
        self._first_name_disallowed = None
        self._last_name_disallowed = None
        self._user_name_disallowed = None
        self._min_password_age = None
        self._password_expires_after = None
        self._password_expire_warning = None
        self._required_chars = None
        self._disallowed_chars = None
        self._allowed_chars = None
        self._disallowed_substrings = None
        self._dictionary_word_disallowed = None
        self._dictionary_location = None
        self._dictionary_delimiter = None
        self._max_incorrect_attempts = None
        self._lockout_duration = None
        self._num_passwords_in_history = None
        self._password_strength = None
        self._force_password_reset = None
        self._groups = None
        self._priority = None
        self._configured_password_policy_rules = None

    @property
    def id(self):
        """
        Gets the id of this PasswordPolicy.
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


        :return: The id of this PasswordPolicy.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PasswordPolicy.
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


        :param id: The id of this PasswordPolicy.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this PasswordPolicy.
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


        :return: The ocid of this PasswordPolicy.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this PasswordPolicy.
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


        :param ocid: The ocid of this PasswordPolicy.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this PasswordPolicy.
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


        :return: The schemas of this PasswordPolicy.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this PasswordPolicy.
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


        :param schemas: The schemas of this PasswordPolicy.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this PasswordPolicy.

        :return: The meta of this PasswordPolicy.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this PasswordPolicy.

        :param meta: The meta of this PasswordPolicy.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this PasswordPolicy.

        :return: The idcs_created_by of this PasswordPolicy.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this PasswordPolicy.

        :param idcs_created_by: The idcs_created_by of this PasswordPolicy.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this PasswordPolicy.

        :return: The idcs_last_modified_by of this PasswordPolicy.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this PasswordPolicy.

        :param idcs_last_modified_by: The idcs_last_modified_by of this PasswordPolicy.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this PasswordPolicy.
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


        :return: The idcs_prevented_operations of this PasswordPolicy.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this PasswordPolicy.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this PasswordPolicy.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this PasswordPolicy.
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


        :return: The tags of this PasswordPolicy.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this PasswordPolicy.
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


        :param tags: The tags of this PasswordPolicy.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this PasswordPolicy.
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


        :return: The delete_in_progress of this PasswordPolicy.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this PasswordPolicy.
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


        :param delete_in_progress: The delete_in_progress of this PasswordPolicy.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this PasswordPolicy.
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


        :return: The idcs_last_upgraded_in_release of this PasswordPolicy.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this PasswordPolicy.
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


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this PasswordPolicy.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this PasswordPolicy.
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


        :return: The domain_ocid of this PasswordPolicy.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this PasswordPolicy.
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


        :param domain_ocid: The domain_ocid of this PasswordPolicy.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this PasswordPolicy.
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


        :return: The compartment_ocid of this PasswordPolicy.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this PasswordPolicy.
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


        :param compartment_ocid: The compartment_ocid of this PasswordPolicy.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this PasswordPolicy.
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


        :return: The tenancy_ocid of this PasswordPolicy.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this PasswordPolicy.
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


        :param tenancy_ocid: The tenancy_ocid of this PasswordPolicy.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def external_id(self):
        """
        Gets the external_id of this PasswordPolicy.
        An identifier for the Resource as defined by the Service Consumer. The externalId may simplify identification of the Resource between Service Consumer and Service Provider by allowing the Consumer to refer to the Resource with its own identifier, obviating the need to store a local mapping between the local identifier of the Resource and the identifier used by the Service Provider. Each Resource MAY include a non-empty externalId value. The value of the externalId attribute is always issued by the Service Consumer and can never be specified by the Service Provider. The Service Provider MUST always interpret the externalId as scoped to the Service Consumer's tenant.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The external_id of this PasswordPolicy.
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """
        Sets the external_id of this PasswordPolicy.
        An identifier for the Resource as defined by the Service Consumer. The externalId may simplify identification of the Resource between Service Consumer and Service Provider by allowing the Consumer to refer to the Resource with its own identifier, obviating the need to store a local mapping between the local identifier of the Resource and the identifier used by the Service Provider. Each Resource MAY include a non-empty externalId value. The value of the externalId attribute is always issued by the Service Consumer and can never be specified by the Service Provider. The Service Provider MUST always interpret the externalId as scoped to the Service Consumer's tenant.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param external_id: The external_id of this PasswordPolicy.
        :type: str
        """
        self._external_id = external_id

    @property
    def name(self):
        """
        **[Required]** Gets the name of this PasswordPolicy.
        A String that is the name of the policy to display to the user. This is the only mandatory attribute for a password policy.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: always
         - type: string
         - uniqueness: server


        :return: The name of this PasswordPolicy.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PasswordPolicy.
        A String that is the name of the policy to display to the user. This is the only mandatory attribute for a password policy.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: always
         - type: string
         - uniqueness: server


        :param name: The name of this PasswordPolicy.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this PasswordPolicy.
        A String that describes the password policy

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The description of this PasswordPolicy.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PasswordPolicy.
        A String that describes the password policy

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param description: The description of this PasswordPolicy.
        :type: str
        """
        self._description = description

    @property
    def max_length(self):
        """
        Gets the max_length of this PasswordPolicy.
        The maximum password length (in characters). A value of 0 or no value indicates no maximum length restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The max_length of this PasswordPolicy.
        :rtype: int
        """
        return self._max_length

    @max_length.setter
    def max_length(self, max_length):
        """
        Sets the max_length of this PasswordPolicy.
        The maximum password length (in characters). A value of 0 or no value indicates no maximum length restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param max_length: The max_length of this PasswordPolicy.
        :type: int
        """
        self._max_length = max_length

    @property
    def min_length(self):
        """
        Gets the min_length of this PasswordPolicy.
        The minimum password length (in characters). A value of 0 or no value indicates no minimum length restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_length of this PasswordPolicy.
        :rtype: int
        """
        return self._min_length

    @min_length.setter
    def min_length(self, min_length):
        """
        Sets the min_length of this PasswordPolicy.
        The minimum password length (in characters). A value of 0 or no value indicates no minimum length restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_length: The min_length of this PasswordPolicy.
        :type: int
        """
        self._min_length = min_length

    @property
    def min_alphas(self):
        """
        Gets the min_alphas of this PasswordPolicy.
        The minimum number of alphabetic characters in a password.  A value of 0 or no value indicates no minimum alphas restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_alphas of this PasswordPolicy.
        :rtype: int
        """
        return self._min_alphas

    @min_alphas.setter
    def min_alphas(self, min_alphas):
        """
        Sets the min_alphas of this PasswordPolicy.
        The minimum number of alphabetic characters in a password.  A value of 0 or no value indicates no minimum alphas restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_alphas: The min_alphas of this PasswordPolicy.
        :type: int
        """
        self._min_alphas = min_alphas

    @property
    def min_numerals(self):
        """
        Gets the min_numerals of this PasswordPolicy.
        The minimum number of numeric characters in a password.  A value of 0 or no value indicates no minimum numeric character restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_numerals of this PasswordPolicy.
        :rtype: int
        """
        return self._min_numerals

    @min_numerals.setter
    def min_numerals(self, min_numerals):
        """
        Sets the min_numerals of this PasswordPolicy.
        The minimum number of numeric characters in a password.  A value of 0 or no value indicates no minimum numeric character restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_numerals: The min_numerals of this PasswordPolicy.
        :type: int
        """
        self._min_numerals = min_numerals

    @property
    def min_alpha_numerals(self):
        """
        Gets the min_alpha_numerals of this PasswordPolicy.
        The minimum number of a combination of alphabetic and numeric characters in a password.  A value of 0 or no value indicates no minimum alphanumeric character restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_alpha_numerals of this PasswordPolicy.
        :rtype: int
        """
        return self._min_alpha_numerals

    @min_alpha_numerals.setter
    def min_alpha_numerals(self, min_alpha_numerals):
        """
        Sets the min_alpha_numerals of this PasswordPolicy.
        The minimum number of a combination of alphabetic and numeric characters in a password.  A value of 0 or no value indicates no minimum alphanumeric character restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_alpha_numerals: The min_alpha_numerals of this PasswordPolicy.
        :type: int
        """
        self._min_alpha_numerals = min_alpha_numerals

    @property
    def min_special_chars(self):
        """
        Gets the min_special_chars of this PasswordPolicy.
        The minimum number of special characters in a password. A value of 0 or no value indicates no minimum special characters restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_special_chars of this PasswordPolicy.
        :rtype: int
        """
        return self._min_special_chars

    @min_special_chars.setter
    def min_special_chars(self, min_special_chars):
        """
        Sets the min_special_chars of this PasswordPolicy.
        The minimum number of special characters in a password. A value of 0 or no value indicates no minimum special characters restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_special_chars: The min_special_chars of this PasswordPolicy.
        :type: int
        """
        self._min_special_chars = min_special_chars

    @property
    def max_special_chars(self):
        """
        Gets the max_special_chars of this PasswordPolicy.
        The maximum number of special characters in a password.  A value of 0 or no value indicates no maximum special characters restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The max_special_chars of this PasswordPolicy.
        :rtype: int
        """
        return self._max_special_chars

    @max_special_chars.setter
    def max_special_chars(self, max_special_chars):
        """
        Sets the max_special_chars of this PasswordPolicy.
        The maximum number of special characters in a password.  A value of 0 or no value indicates no maximum special characters restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param max_special_chars: The max_special_chars of this PasswordPolicy.
        :type: int
        """
        self._max_special_chars = max_special_chars

    @property
    def min_lower_case(self):
        """
        Gets the min_lower_case of this PasswordPolicy.
        The minimum number of lowercase alphabetic characters in a password.  A value of 0 or no value indicates no minimum lowercase restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_lower_case of this PasswordPolicy.
        :rtype: int
        """
        return self._min_lower_case

    @min_lower_case.setter
    def min_lower_case(self, min_lower_case):
        """
        Sets the min_lower_case of this PasswordPolicy.
        The minimum number of lowercase alphabetic characters in a password.  A value of 0 or no value indicates no minimum lowercase restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_lower_case: The min_lower_case of this PasswordPolicy.
        :type: int
        """
        self._min_lower_case = min_lower_case

    @property
    def min_upper_case(self):
        """
        Gets the min_upper_case of this PasswordPolicy.
        The minimum number of uppercase alphabetic characters in a password. A value of 0 or no value indicates no minimum uppercase restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_upper_case of this PasswordPolicy.
        :rtype: int
        """
        return self._min_upper_case

    @min_upper_case.setter
    def min_upper_case(self, min_upper_case):
        """
        Sets the min_upper_case of this PasswordPolicy.
        The minimum number of uppercase alphabetic characters in a password. A value of 0 or no value indicates no minimum uppercase restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_upper_case: The min_upper_case of this PasswordPolicy.
        :type: int
        """
        self._min_upper_case = min_upper_case

    @property
    def min_unique_chars(self):
        """
        Gets the min_unique_chars of this PasswordPolicy.
        The minimum number of unique characters in a password.  A value of 0 or no value indicates no minimum unique characters restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_unique_chars of this PasswordPolicy.
        :rtype: int
        """
        return self._min_unique_chars

    @min_unique_chars.setter
    def min_unique_chars(self, min_unique_chars):
        """
        Sets the min_unique_chars of this PasswordPolicy.
        The minimum number of unique characters in a password.  A value of 0 or no value indicates no minimum unique characters restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_unique_chars: The min_unique_chars of this PasswordPolicy.
        :type: int
        """
        self._min_unique_chars = min_unique_chars

    @property
    def max_repeated_chars(self):
        """
        Gets the max_repeated_chars of this PasswordPolicy.
        The maximum number of repeated characters allowed in a password.  A value of 0 or no value indicates no such restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The max_repeated_chars of this PasswordPolicy.
        :rtype: int
        """
        return self._max_repeated_chars

    @max_repeated_chars.setter
    def max_repeated_chars(self, max_repeated_chars):
        """
        Sets the max_repeated_chars of this PasswordPolicy.
        The maximum number of repeated characters allowed in a password.  A value of 0 or no value indicates no such restriction.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param max_repeated_chars: The max_repeated_chars of this PasswordPolicy.
        :type: int
        """
        self._max_repeated_chars = max_repeated_chars

    @property
    def starts_with_alphabet(self):
        """
        Gets the starts_with_alphabet of this PasswordPolicy.
        Indicates that the password must begin with an alphabetic character

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The starts_with_alphabet of this PasswordPolicy.
        :rtype: bool
        """
        return self._starts_with_alphabet

    @starts_with_alphabet.setter
    def starts_with_alphabet(self, starts_with_alphabet):
        """
        Sets the starts_with_alphabet of this PasswordPolicy.
        Indicates that the password must begin with an alphabetic character

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param starts_with_alphabet: The starts_with_alphabet of this PasswordPolicy.
        :type: bool
        """
        self._starts_with_alphabet = starts_with_alphabet

    @property
    def first_name_disallowed(self):
        """
        Gets the first_name_disallowed of this PasswordPolicy.
        Indicates a sequence of characters that match the user's first name of given name cannot be the password. Password validation against policy will be ignored if length of first name is less than or equal to 3 characters.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The first_name_disallowed of this PasswordPolicy.
        :rtype: bool
        """
        return self._first_name_disallowed

    @first_name_disallowed.setter
    def first_name_disallowed(self, first_name_disallowed):
        """
        Sets the first_name_disallowed of this PasswordPolicy.
        Indicates a sequence of characters that match the user's first name of given name cannot be the password. Password validation against policy will be ignored if length of first name is less than or equal to 3 characters.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param first_name_disallowed: The first_name_disallowed of this PasswordPolicy.
        :type: bool
        """
        self._first_name_disallowed = first_name_disallowed

    @property
    def last_name_disallowed(self):
        """
        Gets the last_name_disallowed of this PasswordPolicy.
        Indicates a sequence of characters that match the user's last name of given name cannot be the password. Password validation against policy will be ignored if length of last name is less than or equal to 3 characters.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The last_name_disallowed of this PasswordPolicy.
        :rtype: bool
        """
        return self._last_name_disallowed

    @last_name_disallowed.setter
    def last_name_disallowed(self, last_name_disallowed):
        """
        Sets the last_name_disallowed of this PasswordPolicy.
        Indicates a sequence of characters that match the user's last name of given name cannot be the password. Password validation against policy will be ignored if length of last name is less than or equal to 3 characters.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param last_name_disallowed: The last_name_disallowed of this PasswordPolicy.
        :type: bool
        """
        self._last_name_disallowed = last_name_disallowed

    @property
    def user_name_disallowed(self):
        """
        Gets the user_name_disallowed of this PasswordPolicy.
        Indicates a sequence of characters that match the username cannot be the password. Password validation against policy will be ignored if length of user name is less than or equal to 3 characters.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The user_name_disallowed of this PasswordPolicy.
        :rtype: bool
        """
        return self._user_name_disallowed

    @user_name_disallowed.setter
    def user_name_disallowed(self, user_name_disallowed):
        """
        Sets the user_name_disallowed of this PasswordPolicy.
        Indicates a sequence of characters that match the username cannot be the password. Password validation against policy will be ignored if length of user name is less than or equal to 3 characters.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param user_name_disallowed: The user_name_disallowed of this PasswordPolicy.
        :type: bool
        """
        self._user_name_disallowed = user_name_disallowed

    @property
    def min_password_age(self):
        """
        Gets the min_password_age of this PasswordPolicy.
        Minimum time after which the user can resubmit the reset password request

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The min_password_age of this PasswordPolicy.
        :rtype: int
        """
        return self._min_password_age

    @min_password_age.setter
    def min_password_age(self, min_password_age):
        """
        Sets the min_password_age of this PasswordPolicy.
        Minimum time after which the user can resubmit the reset password request

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param min_password_age: The min_password_age of this PasswordPolicy.
        :type: int
        """
        self._min_password_age = min_password_age

    @property
    def password_expires_after(self):
        """
        Gets the password_expires_after of this PasswordPolicy.
        The number of days after which the password expires automatically

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The password_expires_after of this PasswordPolicy.
        :rtype: int
        """
        return self._password_expires_after

    @password_expires_after.setter
    def password_expires_after(self, password_expires_after):
        """
        Sets the password_expires_after of this PasswordPolicy.
        The number of days after which the password expires automatically

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param password_expires_after: The password_expires_after of this PasswordPolicy.
        :type: int
        """
        self._password_expires_after = password_expires_after

    @property
    def password_expire_warning(self):
        """
        Gets the password_expire_warning of this PasswordPolicy.
        An integer indicating the number of days before which the user should be warned about password expiry.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The password_expire_warning of this PasswordPolicy.
        :rtype: int
        """
        return self._password_expire_warning

    @password_expire_warning.setter
    def password_expire_warning(self, password_expire_warning):
        """
        Sets the password_expire_warning of this PasswordPolicy.
        An integer indicating the number of days before which the user should be warned about password expiry.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param password_expire_warning: The password_expire_warning of this PasswordPolicy.
        :type: int
        """
        self._password_expire_warning = password_expire_warning

    @property
    def required_chars(self):
        """
        Gets the required_chars of this PasswordPolicy.
        A String value whose contents indicate a set of characters that must appear, in any sequence, in a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The required_chars of this PasswordPolicy.
        :rtype: str
        """
        return self._required_chars

    @required_chars.setter
    def required_chars(self, required_chars):
        """
        Sets the required_chars of this PasswordPolicy.
        A String value whose contents indicate a set of characters that must appear, in any sequence, in a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param required_chars: The required_chars of this PasswordPolicy.
        :type: str
        """
        self._required_chars = required_chars

    @property
    def disallowed_chars(self):
        """
        Gets the disallowed_chars of this PasswordPolicy.
        A String value whose contents indicate a set of characters that cannot appear, in any sequence, in a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The disallowed_chars of this PasswordPolicy.
        :rtype: str
        """
        return self._disallowed_chars

    @disallowed_chars.setter
    def disallowed_chars(self, disallowed_chars):
        """
        Sets the disallowed_chars of this PasswordPolicy.
        A String value whose contents indicate a set of characters that cannot appear, in any sequence, in a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param disallowed_chars: The disallowed_chars of this PasswordPolicy.
        :type: str
        """
        self._disallowed_chars = disallowed_chars

    @property
    def allowed_chars(self):
        """
        Gets the allowed_chars of this PasswordPolicy.
        A String value whose contents indicate a set of characters that can appear, in any sequence, in a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The allowed_chars of this PasswordPolicy.
        :rtype: str
        """
        return self._allowed_chars

    @allowed_chars.setter
    def allowed_chars(self, allowed_chars):
        """
        Sets the allowed_chars of this PasswordPolicy.
        A String value whose contents indicate a set of characters that can appear, in any sequence, in a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param allowed_chars: The allowed_chars of this PasswordPolicy.
        :type: str
        """
        self._allowed_chars = allowed_chars

    @property
    def disallowed_substrings(self):
        """
        Gets the disallowed_substrings of this PasswordPolicy.
        A String value whose contents indicate a set of substrings that cannot appear, in any sequence, in a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The disallowed_substrings of this PasswordPolicy.
        :rtype: list[str]
        """
        return self._disallowed_substrings

    @disallowed_substrings.setter
    def disallowed_substrings(self, disallowed_substrings):
        """
        Sets the disallowed_substrings of this PasswordPolicy.
        A String value whose contents indicate a set of substrings that cannot appear, in any sequence, in a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param disallowed_substrings: The disallowed_substrings of this PasswordPolicy.
        :type: list[str]
        """
        self._disallowed_substrings = disallowed_substrings

    @property
    def dictionary_word_disallowed(self):
        """
        Gets the dictionary_word_disallowed of this PasswordPolicy.
        Indicates whether the password can match a dictionary word

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The dictionary_word_disallowed of this PasswordPolicy.
        :rtype: bool
        """
        return self._dictionary_word_disallowed

    @dictionary_word_disallowed.setter
    def dictionary_word_disallowed(self, dictionary_word_disallowed):
        """
        Sets the dictionary_word_disallowed of this PasswordPolicy.
        Indicates whether the password can match a dictionary word

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param dictionary_word_disallowed: The dictionary_word_disallowed of this PasswordPolicy.
        :type: bool
        """
        self._dictionary_word_disallowed = dictionary_word_disallowed

    @property
    def dictionary_location(self):
        """
        Gets the dictionary_location of this PasswordPolicy.
        A Reference value that contains the URI of a dictionary of words not allowed to appear within a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The dictionary_location of this PasswordPolicy.
        :rtype: str
        """
        return self._dictionary_location

    @dictionary_location.setter
    def dictionary_location(self, dictionary_location):
        """
        Sets the dictionary_location of this PasswordPolicy.
        A Reference value that contains the URI of a dictionary of words not allowed to appear within a password value

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param dictionary_location: The dictionary_location of this PasswordPolicy.
        :type: str
        """
        self._dictionary_location = dictionary_location

    @property
    def dictionary_delimiter(self):
        """
        Gets the dictionary_delimiter of this PasswordPolicy.
        A delimiter used to separate characters in the dictionary file

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The dictionary_delimiter of this PasswordPolicy.
        :rtype: str
        """
        return self._dictionary_delimiter

    @dictionary_delimiter.setter
    def dictionary_delimiter(self, dictionary_delimiter):
        """
        Sets the dictionary_delimiter of this PasswordPolicy.
        A delimiter used to separate characters in the dictionary file

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param dictionary_delimiter: The dictionary_delimiter of this PasswordPolicy.
        :type: str
        """
        self._dictionary_delimiter = dictionary_delimiter

    @property
    def max_incorrect_attempts(self):
        """
        Gets the max_incorrect_attempts of this PasswordPolicy.
        An integer that represents the maximum number of failed logins before an account is locked

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The max_incorrect_attempts of this PasswordPolicy.
        :rtype: int
        """
        return self._max_incorrect_attempts

    @max_incorrect_attempts.setter
    def max_incorrect_attempts(self, max_incorrect_attempts):
        """
        Sets the max_incorrect_attempts of this PasswordPolicy.
        An integer that represents the maximum number of failed logins before an account is locked

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param max_incorrect_attempts: The max_incorrect_attempts of this PasswordPolicy.
        :type: int
        """
        self._max_incorrect_attempts = max_incorrect_attempts

    @property
    def lockout_duration(self):
        """
        Gets the lockout_duration of this PasswordPolicy.
        The time period in minutes to lock out a user account when the threshold of invalid login attempts is reached. The available range is from 5 through 1440 minutes (24 hours).

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The lockout_duration of this PasswordPolicy.
        :rtype: int
        """
        return self._lockout_duration

    @lockout_duration.setter
    def lockout_duration(self, lockout_duration):
        """
        Sets the lockout_duration of this PasswordPolicy.
        The time period in minutes to lock out a user account when the threshold of invalid login attempts is reached. The available range is from 5 through 1440 minutes (24 hours).

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param lockout_duration: The lockout_duration of this PasswordPolicy.
        :type: int
        """
        self._lockout_duration = lockout_duration

    @property
    def num_passwords_in_history(self):
        """
        Gets the num_passwords_in_history of this PasswordPolicy.
        The number of passwords that will be kept in history that may not be used as a password

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The num_passwords_in_history of this PasswordPolicy.
        :rtype: int
        """
        return self._num_passwords_in_history

    @num_passwords_in_history.setter
    def num_passwords_in_history(self, num_passwords_in_history):
        """
        Sets the num_passwords_in_history of this PasswordPolicy.
        The number of passwords that will be kept in history that may not be used as a password

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param num_passwords_in_history: The num_passwords_in_history of this PasswordPolicy.
        :type: int
        """
        self._num_passwords_in_history = num_passwords_in_history

    @property
    def password_strength(self):
        """
        Gets the password_strength of this PasswordPolicy.
        Indicates whether the password policy is configured as Simple, Standard, or Custom.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "Simple", "Standard", "Custom", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The password_strength of this PasswordPolicy.
        :rtype: str
        """
        return self._password_strength

    @password_strength.setter
    def password_strength(self, password_strength):
        """
        Sets the password_strength of this PasswordPolicy.
        Indicates whether the password policy is configured as Simple, Standard, or Custom.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param password_strength: The password_strength of this PasswordPolicy.
        :type: str
        """
        allowed_values = ["Simple", "Standard", "Custom"]
        if not value_allowed_none_or_none_sentinel(password_strength, allowed_values):
            password_strength = 'UNKNOWN_ENUM_VALUE'
        self._password_strength = password_strength

    @property
    def force_password_reset(self):
        """
        Gets the force_password_reset of this PasswordPolicy.
        Indicates whether all of the users should be forced to reset their password on the next login (to comply with new password policy changes)

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: writeOnly
         - required: false
         - returned: never
         - type: boolean
         - uniqueness: none


        :return: The force_password_reset of this PasswordPolicy.
        :rtype: bool
        """
        return self._force_password_reset

    @force_password_reset.setter
    def force_password_reset(self, force_password_reset):
        """
        Sets the force_password_reset of this PasswordPolicy.
        Indicates whether all of the users should be forced to reset their password on the next login (to comply with new password policy changes)

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: writeOnly
         - required: false
         - returned: never
         - type: boolean
         - uniqueness: none


        :param force_password_reset: The force_password_reset of this PasswordPolicy.
        :type: bool
        """
        self._force_password_reset = force_password_reset

    @property
    def groups(self):
        """
        Gets the groups of this PasswordPolicy.
        A list of groups that the password policy belongs to.

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The groups of this PasswordPolicy.
        :rtype: list[oci.identity_domains.models.PasswordPolicyGroups]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """
        Sets the groups of this PasswordPolicy.
        A list of groups that the password policy belongs to.

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param groups: The groups of this PasswordPolicy.
        :type: list[oci.identity_domains.models.PasswordPolicyGroups]
        """
        self._groups = groups

    @property
    def priority(self):
        """
        Gets the priority of this PasswordPolicy.
        Password policy priority

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - idcsMinValue: 1
         - uniqueness: server


        :return: The priority of this PasswordPolicy.
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """
        Sets the priority of this PasswordPolicy.
        Password policy priority

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - idcsMinValue: 1
         - uniqueness: server


        :param priority: The priority of this PasswordPolicy.
        :type: int
        """
        self._priority = priority

    @property
    def configured_password_policy_rules(self):
        """
        Gets the configured_password_policy_rules of this PasswordPolicy.
        List of password policy rules that have values set. This map of stringKey:stringValue pairs can be used to aid users while setting/resetting password

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [key]
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The configured_password_policy_rules of this PasswordPolicy.
        :rtype: list[oci.identity_domains.models.PasswordPolicyConfiguredPasswordPolicyRules]
        """
        return self._configured_password_policy_rules

    @configured_password_policy_rules.setter
    def configured_password_policy_rules(self, configured_password_policy_rules):
        """
        Sets the configured_password_policy_rules of this PasswordPolicy.
        List of password policy rules that have values set. This map of stringKey:stringValue pairs can be used to aid users while setting/resetting password

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [key]
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param configured_password_policy_rules: The configured_password_policy_rules of this PasswordPolicy.
        :type: list[oci.identity_domains.models.PasswordPolicyConfiguredPasswordPolicyRules]
        """
        self._configured_password_policy_rules = configured_password_policy_rules

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
