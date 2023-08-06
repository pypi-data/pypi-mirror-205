# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class IdentityProvider(object):
    """
    Federation trusted partner Identity Provider
    """

    #: A constant which can be used with the idcs_prevented_operations property of a IdentityProvider.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a IdentityProvider.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a IdentityProvider.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    #: A constant which can be used with the authn_request_binding property of a IdentityProvider.
    #: This constant has a value of "Redirect"
    AUTHN_REQUEST_BINDING_REDIRECT = "Redirect"

    #: A constant which can be used with the authn_request_binding property of a IdentityProvider.
    #: This constant has a value of "Post"
    AUTHN_REQUEST_BINDING_POST = "Post"

    #: A constant which can be used with the logout_binding property of a IdentityProvider.
    #: This constant has a value of "Redirect"
    LOGOUT_BINDING_REDIRECT = "Redirect"

    #: A constant which can be used with the logout_binding property of a IdentityProvider.
    #: This constant has a value of "Post"
    LOGOUT_BINDING_POST = "Post"

    #: A constant which can be used with the signature_hash_algorithm property of a IdentityProvider.
    #: This constant has a value of "SHA-1"
    SIGNATURE_HASH_ALGORITHM_SHA_1 = "SHA-1"

    #: A constant which can be used with the signature_hash_algorithm property of a IdentityProvider.
    #: This constant has a value of "SHA-256"
    SIGNATURE_HASH_ALGORITHM_SHA_256 = "SHA-256"

    #: A constant which can be used with the jit_user_prov_group_assignment_method property of a IdentityProvider.
    #: This constant has a value of "Overwrite"
    JIT_USER_PROV_GROUP_ASSIGNMENT_METHOD_OVERWRITE = "Overwrite"

    #: A constant which can be used with the jit_user_prov_group_assignment_method property of a IdentityProvider.
    #: This constant has a value of "Merge"
    JIT_USER_PROV_GROUP_ASSIGNMENT_METHOD_MERGE = "Merge"

    #: A constant which can be used with the jit_user_prov_group_mapping_mode property of a IdentityProvider.
    #: This constant has a value of "implicit"
    JIT_USER_PROV_GROUP_MAPPING_MODE_IMPLICIT = "implicit"

    #: A constant which can be used with the jit_user_prov_group_mapping_mode property of a IdentityProvider.
    #: This constant has a value of "explicit"
    JIT_USER_PROV_GROUP_MAPPING_MODE_EXPLICIT = "explicit"

    #: A constant which can be used with the user_mapping_method property of a IdentityProvider.
    #: This constant has a value of "NameIDToUserAttribute"
    USER_MAPPING_METHOD_NAME_ID_TO_USER_ATTRIBUTE = "NameIDToUserAttribute"

    #: A constant which can be used with the user_mapping_method property of a IdentityProvider.
    #: This constant has a value of "AssertionAttributeToUserAttribute"
    USER_MAPPING_METHOD_ASSERTION_ATTRIBUTE_TO_USER_ATTRIBUTE = "AssertionAttributeToUserAttribute"

    #: A constant which can be used with the user_mapping_method property of a IdentityProvider.
    #: This constant has a value of "CorrelationPolicyRule"
    USER_MAPPING_METHOD_CORRELATION_POLICY_RULE = "CorrelationPolicyRule"

    #: A constant which can be used with the type property of a IdentityProvider.
    #: This constant has a value of "SAML"
    TYPE_SAML = "SAML"

    #: A constant which can be used with the type property of a IdentityProvider.
    #: This constant has a value of "SOCIAL"
    TYPE_SOCIAL = "SOCIAL"

    #: A constant which can be used with the type property of a IdentityProvider.
    #: This constant has a value of "IWA"
    TYPE_IWA = "IWA"

    #: A constant which can be used with the type property of a IdentityProvider.
    #: This constant has a value of "X509"
    TYPE_X509 = "X509"

    #: A constant which can be used with the type property of a IdentityProvider.
    #: This constant has a value of "LOCAL"
    TYPE_LOCAL = "LOCAL"

    def __init__(self, **kwargs):
        """
        Initializes a new IdentityProvider object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this IdentityProvider.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this IdentityProvider.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this IdentityProvider.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this IdentityProvider.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this IdentityProvider.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this IdentityProvider.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this IdentityProvider.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this IdentityProvider.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this IdentityProvider.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this IdentityProvider.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this IdentityProvider.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this IdentityProvider.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this IdentityProvider.
        :type tenancy_ocid: str

        :param external_id:
            The value to assign to the external_id property of this IdentityProvider.
        :type external_id: str

        :param partner_name:
            The value to assign to the partner_name property of this IdentityProvider.
        :type partner_name: str

        :param description:
            The value to assign to the description property of this IdentityProvider.
        :type description: str

        :param metadata:
            The value to assign to the metadata property of this IdentityProvider.
        :type metadata: str

        :param partner_provider_id:
            The value to assign to the partner_provider_id property of this IdentityProvider.
        :type partner_provider_id: str

        :param tenant_provider_id:
            The value to assign to the tenant_provider_id property of this IdentityProvider.
        :type tenant_provider_id: str

        :param succinct_id:
            The value to assign to the succinct_id property of this IdentityProvider.
        :type succinct_id: str

        :param idp_sso_url:
            The value to assign to the idp_sso_url property of this IdentityProvider.
        :type idp_sso_url: str

        :param logout_request_url:
            The value to assign to the logout_request_url property of this IdentityProvider.
        :type logout_request_url: str

        :param logout_response_url:
            The value to assign to the logout_response_url property of this IdentityProvider.
        :type logout_response_url: str

        :param signing_certificate:
            The value to assign to the signing_certificate property of this IdentityProvider.
        :type signing_certificate: str

        :param encryption_certificate:
            The value to assign to the encryption_certificate property of this IdentityProvider.
        :type encryption_certificate: str

        :param name_id_format:
            The value to assign to the name_id_format property of this IdentityProvider.
        :type name_id_format: str

        :param include_signing_cert_in_signature:
            The value to assign to the include_signing_cert_in_signature property of this IdentityProvider.
        :type include_signing_cert_in_signature: bool

        :param authn_request_binding:
            The value to assign to the authn_request_binding property of this IdentityProvider.
            Allowed values for this property are: "Redirect", "Post", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type authn_request_binding: str

        :param logout_binding:
            The value to assign to the logout_binding property of this IdentityProvider.
            Allowed values for this property are: "Redirect", "Post", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type logout_binding: str

        :param logout_enabled:
            The value to assign to the logout_enabled property of this IdentityProvider.
        :type logout_enabled: bool

        :param signature_hash_algorithm:
            The value to assign to the signature_hash_algorithm property of this IdentityProvider.
            Allowed values for this property are: "SHA-1", "SHA-256", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type signature_hash_algorithm: str

        :param enabled:
            The value to assign to the enabled property of this IdentityProvider.
        :type enabled: bool

        :param icon_url:
            The value to assign to the icon_url property of this IdentityProvider.
        :type icon_url: str

        :param shown_on_login_page:
            The value to assign to the shown_on_login_page property of this IdentityProvider.
        :type shown_on_login_page: bool

        :param jit_user_prov_enabled:
            The value to assign to the jit_user_prov_enabled property of this IdentityProvider.
        :type jit_user_prov_enabled: bool

        :param jit_user_prov_group_assertion_attribute_enabled:
            The value to assign to the jit_user_prov_group_assertion_attribute_enabled property of this IdentityProvider.
        :type jit_user_prov_group_assertion_attribute_enabled: bool

        :param jit_user_prov_group_static_list_enabled:
            The value to assign to the jit_user_prov_group_static_list_enabled property of this IdentityProvider.
        :type jit_user_prov_group_static_list_enabled: bool

        :param jit_user_prov_create_user_enabled:
            The value to assign to the jit_user_prov_create_user_enabled property of this IdentityProvider.
        :type jit_user_prov_create_user_enabled: bool

        :param jit_user_prov_attribute_update_enabled:
            The value to assign to the jit_user_prov_attribute_update_enabled property of this IdentityProvider.
        :type jit_user_prov_attribute_update_enabled: bool

        :param jit_user_prov_group_assignment_method:
            The value to assign to the jit_user_prov_group_assignment_method property of this IdentityProvider.
            Allowed values for this property are: "Overwrite", "Merge", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type jit_user_prov_group_assignment_method: str

        :param jit_user_prov_group_mapping_mode:
            The value to assign to the jit_user_prov_group_mapping_mode property of this IdentityProvider.
            Allowed values for this property are: "implicit", "explicit", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type jit_user_prov_group_mapping_mode: str

        :param jit_user_prov_group_mappings:
            The value to assign to the jit_user_prov_group_mappings property of this IdentityProvider.
        :type jit_user_prov_group_mappings: list[oci.identity_domains.models.IdentityProviderJitUserProvGroupMappings]

        :param jit_user_prov_group_saml_attribute_name:
            The value to assign to the jit_user_prov_group_saml_attribute_name property of this IdentityProvider.
        :type jit_user_prov_group_saml_attribute_name: str

        :param service_instance_identifier:
            The value to assign to the service_instance_identifier property of this IdentityProvider.
        :type service_instance_identifier: str

        :param user_mapping_method:
            The value to assign to the user_mapping_method property of this IdentityProvider.
            Allowed values for this property are: "NameIDToUserAttribute", "AssertionAttributeToUserAttribute", "CorrelationPolicyRule", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type user_mapping_method: str

        :param user_mapping_store_attribute:
            The value to assign to the user_mapping_store_attribute property of this IdentityProvider.
        :type user_mapping_store_attribute: str

        :param assertion_attribute:
            The value to assign to the assertion_attribute property of this IdentityProvider.
        :type assertion_attribute: str

        :param type:
            The value to assign to the type property of this IdentityProvider.
            Allowed values for this property are: "SAML", "SOCIAL", "IWA", "X509", "LOCAL", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param require_force_authn:
            The value to assign to the require_force_authn property of this IdentityProvider.
        :type require_force_authn: bool

        :param requires_encrypted_assertion:
            The value to assign to the requires_encrypted_assertion property of this IdentityProvider.
        :type requires_encrypted_assertion: bool

        :param saml_ho_k_required:
            The value to assign to the saml_ho_k_required property of this IdentityProvider.
        :type saml_ho_k_required: bool

        :param requested_authentication_context:
            The value to assign to the requested_authentication_context property of this IdentityProvider.
        :type requested_authentication_context: list[str]

        :param jit_user_prov_ignore_error_on_absent_groups:
            The value to assign to the jit_user_prov_ignore_error_on_absent_groups property of this IdentityProvider.
        :type jit_user_prov_ignore_error_on_absent_groups: bool

        :param jit_user_prov_attributes:
            The value to assign to the jit_user_prov_attributes property of this IdentityProvider.
        :type jit_user_prov_attributes: oci.identity_domains.models.IdentityProviderJitUserProvAttributes

        :param jit_user_prov_assigned_groups:
            The value to assign to the jit_user_prov_assigned_groups property of this IdentityProvider.
        :type jit_user_prov_assigned_groups: list[oci.identity_domains.models.IdentityProviderJitUserProvAssignedGroups]

        :param correlation_policy:
            The value to assign to the correlation_policy property of this IdentityProvider.
        :type correlation_policy: oci.identity_domains.models.IdentityProviderCorrelationPolicy

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider property of this IdentityProvider.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider: oci.identity_domains.models.ExtensionSocialIdentityProvider

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider property of this IdentityProvider.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider: oci.identity_domains.models.ExtensionX509IdentityProvider

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
            'partner_name': 'str',
            'description': 'str',
            'metadata': 'str',
            'partner_provider_id': 'str',
            'tenant_provider_id': 'str',
            'succinct_id': 'str',
            'idp_sso_url': 'str',
            'logout_request_url': 'str',
            'logout_response_url': 'str',
            'signing_certificate': 'str',
            'encryption_certificate': 'str',
            'name_id_format': 'str',
            'include_signing_cert_in_signature': 'bool',
            'authn_request_binding': 'str',
            'logout_binding': 'str',
            'logout_enabled': 'bool',
            'signature_hash_algorithm': 'str',
            'enabled': 'bool',
            'icon_url': 'str',
            'shown_on_login_page': 'bool',
            'jit_user_prov_enabled': 'bool',
            'jit_user_prov_group_assertion_attribute_enabled': 'bool',
            'jit_user_prov_group_static_list_enabled': 'bool',
            'jit_user_prov_create_user_enabled': 'bool',
            'jit_user_prov_attribute_update_enabled': 'bool',
            'jit_user_prov_group_assignment_method': 'str',
            'jit_user_prov_group_mapping_mode': 'str',
            'jit_user_prov_group_mappings': 'list[IdentityProviderJitUserProvGroupMappings]',
            'jit_user_prov_group_saml_attribute_name': 'str',
            'service_instance_identifier': 'str',
            'user_mapping_method': 'str',
            'user_mapping_store_attribute': 'str',
            'assertion_attribute': 'str',
            'type': 'str',
            'require_force_authn': 'bool',
            'requires_encrypted_assertion': 'bool',
            'saml_ho_k_required': 'bool',
            'requested_authentication_context': 'list[str]',
            'jit_user_prov_ignore_error_on_absent_groups': 'bool',
            'jit_user_prov_attributes': 'IdentityProviderJitUserProvAttributes',
            'jit_user_prov_assigned_groups': 'list[IdentityProviderJitUserProvAssignedGroups]',
            'correlation_policy': 'IdentityProviderCorrelationPolicy',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider': 'ExtensionSocialIdentityProvider',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider': 'ExtensionX509IdentityProvider'
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
            'partner_name': 'partnerName',
            'description': 'description',
            'metadata': 'metadata',
            'partner_provider_id': 'partnerProviderId',
            'tenant_provider_id': 'tenantProviderId',
            'succinct_id': 'succinctId',
            'idp_sso_url': 'idpSsoUrl',
            'logout_request_url': 'logoutRequestUrl',
            'logout_response_url': 'logoutResponseUrl',
            'signing_certificate': 'signingCertificate',
            'encryption_certificate': 'encryptionCertificate',
            'name_id_format': 'nameIdFormat',
            'include_signing_cert_in_signature': 'includeSigningCertInSignature',
            'authn_request_binding': 'authnRequestBinding',
            'logout_binding': 'logoutBinding',
            'logout_enabled': 'logoutEnabled',
            'signature_hash_algorithm': 'signatureHashAlgorithm',
            'enabled': 'enabled',
            'icon_url': 'iconUrl',
            'shown_on_login_page': 'shownOnLoginPage',
            'jit_user_prov_enabled': 'jitUserProvEnabled',
            'jit_user_prov_group_assertion_attribute_enabled': 'jitUserProvGroupAssertionAttributeEnabled',
            'jit_user_prov_group_static_list_enabled': 'jitUserProvGroupStaticListEnabled',
            'jit_user_prov_create_user_enabled': 'jitUserProvCreateUserEnabled',
            'jit_user_prov_attribute_update_enabled': 'jitUserProvAttributeUpdateEnabled',
            'jit_user_prov_group_assignment_method': 'jitUserProvGroupAssignmentMethod',
            'jit_user_prov_group_mapping_mode': 'jitUserProvGroupMappingMode',
            'jit_user_prov_group_mappings': 'jitUserProvGroupMappings',
            'jit_user_prov_group_saml_attribute_name': 'jitUserProvGroupSAMLAttributeName',
            'service_instance_identifier': 'serviceInstanceIdentifier',
            'user_mapping_method': 'userMappingMethod',
            'user_mapping_store_attribute': 'userMappingStoreAttribute',
            'assertion_attribute': 'assertionAttribute',
            'type': 'type',
            'require_force_authn': 'requireForceAuthn',
            'requires_encrypted_assertion': 'requiresEncryptedAssertion',
            'saml_ho_k_required': 'samlHoKRequired',
            'requested_authentication_context': 'requestedAuthenticationContext',
            'jit_user_prov_ignore_error_on_absent_groups': 'jitUserProvIgnoreErrorOnAbsentGroups',
            'jit_user_prov_attributes': 'jitUserProvAttributes',
            'jit_user_prov_assigned_groups': 'jitUserProvAssignedGroups',
            'correlation_policy': 'correlationPolicy',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:social:IdentityProvider',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:x509:IdentityProvider'
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
        self._partner_name = None
        self._description = None
        self._metadata = None
        self._partner_provider_id = None
        self._tenant_provider_id = None
        self._succinct_id = None
        self._idp_sso_url = None
        self._logout_request_url = None
        self._logout_response_url = None
        self._signing_certificate = None
        self._encryption_certificate = None
        self._name_id_format = None
        self._include_signing_cert_in_signature = None
        self._authn_request_binding = None
        self._logout_binding = None
        self._logout_enabled = None
        self._signature_hash_algorithm = None
        self._enabled = None
        self._icon_url = None
        self._shown_on_login_page = None
        self._jit_user_prov_enabled = None
        self._jit_user_prov_group_assertion_attribute_enabled = None
        self._jit_user_prov_group_static_list_enabled = None
        self._jit_user_prov_create_user_enabled = None
        self._jit_user_prov_attribute_update_enabled = None
        self._jit_user_prov_group_assignment_method = None
        self._jit_user_prov_group_mapping_mode = None
        self._jit_user_prov_group_mappings = None
        self._jit_user_prov_group_saml_attribute_name = None
        self._service_instance_identifier = None
        self._user_mapping_method = None
        self._user_mapping_store_attribute = None
        self._assertion_attribute = None
        self._type = None
        self._require_force_authn = None
        self._requires_encrypted_assertion = None
        self._saml_ho_k_required = None
        self._requested_authentication_context = None
        self._jit_user_prov_ignore_error_on_absent_groups = None
        self._jit_user_prov_attributes = None
        self._jit_user_prov_assigned_groups = None
        self._correlation_policy = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider = None

    @property
    def id(self):
        """
        Gets the id of this IdentityProvider.
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


        :return: The id of this IdentityProvider.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this IdentityProvider.
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


        :param id: The id of this IdentityProvider.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this IdentityProvider.
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


        :return: The ocid of this IdentityProvider.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this IdentityProvider.
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


        :param ocid: The ocid of this IdentityProvider.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this IdentityProvider.
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


        :return: The schemas of this IdentityProvider.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this IdentityProvider.
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


        :param schemas: The schemas of this IdentityProvider.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this IdentityProvider.

        :return: The meta of this IdentityProvider.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this IdentityProvider.

        :param meta: The meta of this IdentityProvider.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this IdentityProvider.

        :return: The idcs_created_by of this IdentityProvider.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this IdentityProvider.

        :param idcs_created_by: The idcs_created_by of this IdentityProvider.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this IdentityProvider.

        :return: The idcs_last_modified_by of this IdentityProvider.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this IdentityProvider.

        :param idcs_last_modified_by: The idcs_last_modified_by of this IdentityProvider.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this IdentityProvider.
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


        :return: The idcs_prevented_operations of this IdentityProvider.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this IdentityProvider.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this IdentityProvider.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this IdentityProvider.
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


        :return: The tags of this IdentityProvider.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this IdentityProvider.
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


        :param tags: The tags of this IdentityProvider.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this IdentityProvider.
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


        :return: The delete_in_progress of this IdentityProvider.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this IdentityProvider.
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


        :param delete_in_progress: The delete_in_progress of this IdentityProvider.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this IdentityProvider.
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


        :return: The idcs_last_upgraded_in_release of this IdentityProvider.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this IdentityProvider.
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


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this IdentityProvider.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this IdentityProvider.
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


        :return: The domain_ocid of this IdentityProvider.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this IdentityProvider.
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


        :param domain_ocid: The domain_ocid of this IdentityProvider.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this IdentityProvider.
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


        :return: The compartment_ocid of this IdentityProvider.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this IdentityProvider.
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


        :param compartment_ocid: The compartment_ocid of this IdentityProvider.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this IdentityProvider.
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


        :return: The tenancy_ocid of this IdentityProvider.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this IdentityProvider.
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


        :param tenancy_ocid: The tenancy_ocid of this IdentityProvider.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def external_id(self):
        """
        Gets the external_id of this IdentityProvider.
        An identifier for the Resource as defined by the Service Consumer. The externalId may simplify identification of the Resource between Service Consumer and Service Provider by allowing the Consumer to refer to the Resource with its own identifier, obviating the need to store a local mapping between the local identifier of the Resource and the identifier used by the Service Provider. Each Resource MAY include a non-empty externalId value. The value of the externalId attribute is always issued by the Service Consumer and can never be specified by the Service Provider. The Service Provider MUST always interpret the externalId as scoped to the Service Consumer's tenant.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The external_id of this IdentityProvider.
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """
        Sets the external_id of this IdentityProvider.
        An identifier for the Resource as defined by the Service Consumer. The externalId may simplify identification of the Resource between Service Consumer and Service Provider by allowing the Consumer to refer to the Resource with its own identifier, obviating the need to store a local mapping between the local identifier of the Resource and the identifier used by the Service Provider. Each Resource MAY include a non-empty externalId value. The value of the externalId attribute is always issued by the Service Consumer and can never be specified by the Service Provider. The Service Provider MUST always interpret the externalId as scoped to the Service Consumer's tenant.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param external_id: The external_id of this IdentityProvider.
        :type: str
        """
        self._external_id = external_id

    @property
    def partner_name(self):
        """
        **[Required]** Gets the partner_name of this IdentityProvider.
        Unique name of the trusted Identity Provider.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: always
         - type: string
         - uniqueness: server


        :return: The partner_name of this IdentityProvider.
        :rtype: str
        """
        return self._partner_name

    @partner_name.setter
    def partner_name(self, partner_name):
        """
        Sets the partner_name of this IdentityProvider.
        Unique name of the trusted Identity Provider.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: always
         - type: string
         - uniqueness: server


        :param partner_name: The partner_name of this IdentityProvider.
        :type: str
        """
        self._partner_name = partner_name

    @property
    def description(self):
        """
        Gets the description of this IdentityProvider.
        Description

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The description of this IdentityProvider.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this IdentityProvider.
        Description

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param description: The description of this IdentityProvider.
        :type: str
        """
        self._description = description

    @property
    def metadata(self):
        """
        Gets the metadata of this IdentityProvider.
        Metadata

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The metadata of this IdentityProvider.
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this IdentityProvider.
        Metadata

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param metadata: The metadata of this IdentityProvider.
        :type: str
        """
        self._metadata = metadata

    @property
    def partner_provider_id(self):
        """
        Gets the partner_provider_id of this IdentityProvider.
        Provider ID

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: server


        :return: The partner_provider_id of this IdentityProvider.
        :rtype: str
        """
        return self._partner_provider_id

    @partner_provider_id.setter
    def partner_provider_id(self, partner_provider_id):
        """
        Sets the partner_provider_id of this IdentityProvider.
        Provider ID

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: server


        :param partner_provider_id: The partner_provider_id of this IdentityProvider.
        :type: str
        """
        self._partner_provider_id = partner_provider_id

    @property
    def tenant_provider_id(self):
        """
        Gets the tenant_provider_id of this IdentityProvider.
        The alternate Provider ID to be used as the Oracle Identity Cloud Service providerID (instead of the one in SamlSettings) when interacting with this IdP.

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The tenant_provider_id of this IdentityProvider.
        :rtype: str
        """
        return self._tenant_provider_id

    @tenant_provider_id.setter
    def tenant_provider_id(self, tenant_provider_id):
        """
        Sets the tenant_provider_id of this IdentityProvider.
        The alternate Provider ID to be used as the Oracle Identity Cloud Service providerID (instead of the one in SamlSettings) when interacting with this IdP.

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param tenant_provider_id: The tenant_provider_id of this IdentityProvider.
        :type: str
        """
        self._tenant_provider_id = tenant_provider_id

    @property
    def succinct_id(self):
        """
        Gets the succinct_id of this IdentityProvider.
        Succinct ID

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: server


        :return: The succinct_id of this IdentityProvider.
        :rtype: str
        """
        return self._succinct_id

    @succinct_id.setter
    def succinct_id(self, succinct_id):
        """
        Sets the succinct_id of this IdentityProvider.
        Succinct ID

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: server


        :param succinct_id: The succinct_id of this IdentityProvider.
        :type: str
        """
        self._succinct_id = succinct_id

    @property
    def idp_sso_url(self):
        """
        Gets the idp_sso_url of this IdentityProvider.
        Identity Provider SSO URL

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The idp_sso_url of this IdentityProvider.
        :rtype: str
        """
        return self._idp_sso_url

    @idp_sso_url.setter
    def idp_sso_url(self, idp_sso_url):
        """
        Sets the idp_sso_url of this IdentityProvider.
        Identity Provider SSO URL

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param idp_sso_url: The idp_sso_url of this IdentityProvider.
        :type: str
        """
        self._idp_sso_url = idp_sso_url

    @property
    def logout_request_url(self):
        """
        Gets the logout_request_url of this IdentityProvider.
        Logout request URL

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The logout_request_url of this IdentityProvider.
        :rtype: str
        """
        return self._logout_request_url

    @logout_request_url.setter
    def logout_request_url(self, logout_request_url):
        """
        Sets the logout_request_url of this IdentityProvider.
        Logout request URL

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param logout_request_url: The logout_request_url of this IdentityProvider.
        :type: str
        """
        self._logout_request_url = logout_request_url

    @property
    def logout_response_url(self):
        """
        Gets the logout_response_url of this IdentityProvider.
        Logout response URL

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The logout_response_url of this IdentityProvider.
        :rtype: str
        """
        return self._logout_response_url

    @logout_response_url.setter
    def logout_response_url(self, logout_response_url):
        """
        Sets the logout_response_url of this IdentityProvider.
        Logout response URL

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param logout_response_url: The logout_response_url of this IdentityProvider.
        :type: str
        """
        self._logout_response_url = logout_response_url

    @property
    def signing_certificate(self):
        """
        Gets the signing_certificate of this IdentityProvider.
        Signing certificate

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The signing_certificate of this IdentityProvider.
        :rtype: str
        """
        return self._signing_certificate

    @signing_certificate.setter
    def signing_certificate(self, signing_certificate):
        """
        Sets the signing_certificate of this IdentityProvider.
        Signing certificate

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param signing_certificate: The signing_certificate of this IdentityProvider.
        :type: str
        """
        self._signing_certificate = signing_certificate

    @property
    def encryption_certificate(self):
        """
        Gets the encryption_certificate of this IdentityProvider.
        Encryption certificate

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The encryption_certificate of this IdentityProvider.
        :rtype: str
        """
        return self._encryption_certificate

    @encryption_certificate.setter
    def encryption_certificate(self, encryption_certificate):
        """
        Sets the encryption_certificate of this IdentityProvider.
        Encryption certificate

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param encryption_certificate: The encryption_certificate of this IdentityProvider.
        :type: str
        """
        self._encryption_certificate = encryption_certificate

    @property
    def name_id_format(self):
        """
        Gets the name_id_format of this IdentityProvider.
        Default authentication request name ID format.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The name_id_format of this IdentityProvider.
        :rtype: str
        """
        return self._name_id_format

    @name_id_format.setter
    def name_id_format(self, name_id_format):
        """
        Sets the name_id_format of this IdentityProvider.
        Default authentication request name ID format.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param name_id_format: The name_id_format of this IdentityProvider.
        :type: str
        """
        self._name_id_format = name_id_format

    @property
    def include_signing_cert_in_signature(self):
        """
        Gets the include_signing_cert_in_signature of this IdentityProvider.
        Set to true to include the signing certificate in the signature.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The include_signing_cert_in_signature of this IdentityProvider.
        :rtype: bool
        """
        return self._include_signing_cert_in_signature

    @include_signing_cert_in_signature.setter
    def include_signing_cert_in_signature(self, include_signing_cert_in_signature):
        """
        Sets the include_signing_cert_in_signature of this IdentityProvider.
        Set to true to include the signing certificate in the signature.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param include_signing_cert_in_signature: The include_signing_cert_in_signature of this IdentityProvider.
        :type: bool
        """
        self._include_signing_cert_in_signature = include_signing_cert_in_signature

    @property
    def authn_request_binding(self):
        """
        Gets the authn_request_binding of this IdentityProvider.
        HTTP binding to use for authentication requests.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "Redirect", "Post", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The authn_request_binding of this IdentityProvider.
        :rtype: str
        """
        return self._authn_request_binding

    @authn_request_binding.setter
    def authn_request_binding(self, authn_request_binding):
        """
        Sets the authn_request_binding of this IdentityProvider.
        HTTP binding to use for authentication requests.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param authn_request_binding: The authn_request_binding of this IdentityProvider.
        :type: str
        """
        allowed_values = ["Redirect", "Post"]
        if not value_allowed_none_or_none_sentinel(authn_request_binding, allowed_values):
            authn_request_binding = 'UNKNOWN_ENUM_VALUE'
        self._authn_request_binding = authn_request_binding

    @property
    def logout_binding(self):
        """
        Gets the logout_binding of this IdentityProvider.
        HTTP binding to use for logout.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "Redirect", "Post", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The logout_binding of this IdentityProvider.
        :rtype: str
        """
        return self._logout_binding

    @logout_binding.setter
    def logout_binding(self, logout_binding):
        """
        Sets the logout_binding of this IdentityProvider.
        HTTP binding to use for logout.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param logout_binding: The logout_binding of this IdentityProvider.
        :type: str
        """
        allowed_values = ["Redirect", "Post"]
        if not value_allowed_none_or_none_sentinel(logout_binding, allowed_values):
            logout_binding = 'UNKNOWN_ENUM_VALUE'
        self._logout_binding = logout_binding

    @property
    def logout_enabled(self):
        """
        Gets the logout_enabled of this IdentityProvider.
        Set to true to enable logout.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The logout_enabled of this IdentityProvider.
        :rtype: bool
        """
        return self._logout_enabled

    @logout_enabled.setter
    def logout_enabled(self, logout_enabled):
        """
        Sets the logout_enabled of this IdentityProvider.
        Set to true to enable logout.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param logout_enabled: The logout_enabled of this IdentityProvider.
        :type: bool
        """
        self._logout_enabled = logout_enabled

    @property
    def signature_hash_algorithm(self):
        """
        Gets the signature_hash_algorithm of this IdentityProvider.
        Signature hash algorithm.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "SHA-1", "SHA-256", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The signature_hash_algorithm of this IdentityProvider.
        :rtype: str
        """
        return self._signature_hash_algorithm

    @signature_hash_algorithm.setter
    def signature_hash_algorithm(self, signature_hash_algorithm):
        """
        Sets the signature_hash_algorithm of this IdentityProvider.
        Signature hash algorithm.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param signature_hash_algorithm: The signature_hash_algorithm of this IdentityProvider.
        :type: str
        """
        allowed_values = ["SHA-1", "SHA-256"]
        if not value_allowed_none_or_none_sentinel(signature_hash_algorithm, allowed_values):
            signature_hash_algorithm = 'UNKNOWN_ENUM_VALUE'
        self._signature_hash_algorithm = signature_hash_algorithm

    @property
    def enabled(self):
        """
        **[Required]** Gets the enabled of this IdentityProvider.
        Set to true to indicate Partner enabled.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The enabled of this IdentityProvider.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this IdentityProvider.
        Set to true to indicate Partner enabled.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :param enabled: The enabled of this IdentityProvider.
        :type: bool
        """
        self._enabled = enabled

    @property
    def icon_url(self):
        """
        Gets the icon_url of this IdentityProvider.
        Identity Provider Icon URL.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The icon_url of this IdentityProvider.
        :rtype: str
        """
        return self._icon_url

    @icon_url.setter
    def icon_url(self, icon_url):
        """
        Sets the icon_url of this IdentityProvider.
        Identity Provider Icon URL.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param icon_url: The icon_url of this IdentityProvider.
        :type: str
        """
        self._icon_url = icon_url

    @property
    def shown_on_login_page(self):
        """
        Gets the shown_on_login_page of this IdentityProvider.
        Set to true to indicate whether to show IdP in login page or not.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The shown_on_login_page of this IdentityProvider.
        :rtype: bool
        """
        return self._shown_on_login_page

    @shown_on_login_page.setter
    def shown_on_login_page(self, shown_on_login_page):
        """
        Sets the shown_on_login_page of this IdentityProvider.
        Set to true to indicate whether to show IdP in login page or not.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param shown_on_login_page: The shown_on_login_page of this IdentityProvider.
        :type: bool
        """
        self._shown_on_login_page = shown_on_login_page

    @property
    def jit_user_prov_enabled(self):
        """
        Gets the jit_user_prov_enabled of this IdentityProvider.
        Set to true to indicate JIT User Provisioning is enabled

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The jit_user_prov_enabled of this IdentityProvider.
        :rtype: bool
        """
        return self._jit_user_prov_enabled

    @jit_user_prov_enabled.setter
    def jit_user_prov_enabled(self, jit_user_prov_enabled):
        """
        Sets the jit_user_prov_enabled of this IdentityProvider.
        Set to true to indicate JIT User Provisioning is enabled

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param jit_user_prov_enabled: The jit_user_prov_enabled of this IdentityProvider.
        :type: bool
        """
        self._jit_user_prov_enabled = jit_user_prov_enabled

    @property
    def jit_user_prov_group_assertion_attribute_enabled(self):
        """
        Gets the jit_user_prov_group_assertion_attribute_enabled of this IdentityProvider.
        Set to true to indicate JIT User Provisioning Groups should be assigned based on assertion attribute

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The jit_user_prov_group_assertion_attribute_enabled of this IdentityProvider.
        :rtype: bool
        """
        return self._jit_user_prov_group_assertion_attribute_enabled

    @jit_user_prov_group_assertion_attribute_enabled.setter
    def jit_user_prov_group_assertion_attribute_enabled(self, jit_user_prov_group_assertion_attribute_enabled):
        """
        Sets the jit_user_prov_group_assertion_attribute_enabled of this IdentityProvider.
        Set to true to indicate JIT User Provisioning Groups should be assigned based on assertion attribute

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param jit_user_prov_group_assertion_attribute_enabled: The jit_user_prov_group_assertion_attribute_enabled of this IdentityProvider.
        :type: bool
        """
        self._jit_user_prov_group_assertion_attribute_enabled = jit_user_prov_group_assertion_attribute_enabled

    @property
    def jit_user_prov_group_static_list_enabled(self):
        """
        Gets the jit_user_prov_group_static_list_enabled of this IdentityProvider.
        Set to true to indicate JIT User Provisioning Groups should be assigned from a static list

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The jit_user_prov_group_static_list_enabled of this IdentityProvider.
        :rtype: bool
        """
        return self._jit_user_prov_group_static_list_enabled

    @jit_user_prov_group_static_list_enabled.setter
    def jit_user_prov_group_static_list_enabled(self, jit_user_prov_group_static_list_enabled):
        """
        Sets the jit_user_prov_group_static_list_enabled of this IdentityProvider.
        Set to true to indicate JIT User Provisioning Groups should be assigned from a static list

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param jit_user_prov_group_static_list_enabled: The jit_user_prov_group_static_list_enabled of this IdentityProvider.
        :type: bool
        """
        self._jit_user_prov_group_static_list_enabled = jit_user_prov_group_static_list_enabled

    @property
    def jit_user_prov_create_user_enabled(self):
        """
        Gets the jit_user_prov_create_user_enabled of this IdentityProvider.
        Set to true to indicate JIT User Creation is enabled

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The jit_user_prov_create_user_enabled of this IdentityProvider.
        :rtype: bool
        """
        return self._jit_user_prov_create_user_enabled

    @jit_user_prov_create_user_enabled.setter
    def jit_user_prov_create_user_enabled(self, jit_user_prov_create_user_enabled):
        """
        Sets the jit_user_prov_create_user_enabled of this IdentityProvider.
        Set to true to indicate JIT User Creation is enabled

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param jit_user_prov_create_user_enabled: The jit_user_prov_create_user_enabled of this IdentityProvider.
        :type: bool
        """
        self._jit_user_prov_create_user_enabled = jit_user_prov_create_user_enabled

    @property
    def jit_user_prov_attribute_update_enabled(self):
        """
        Gets the jit_user_prov_attribute_update_enabled of this IdentityProvider.
        Set to true to indicate JIT User Creation is enabled

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The jit_user_prov_attribute_update_enabled of this IdentityProvider.
        :rtype: bool
        """
        return self._jit_user_prov_attribute_update_enabled

    @jit_user_prov_attribute_update_enabled.setter
    def jit_user_prov_attribute_update_enabled(self, jit_user_prov_attribute_update_enabled):
        """
        Sets the jit_user_prov_attribute_update_enabled of this IdentityProvider.
        Set to true to indicate JIT User Creation is enabled

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param jit_user_prov_attribute_update_enabled: The jit_user_prov_attribute_update_enabled of this IdentityProvider.
        :type: bool
        """
        self._jit_user_prov_attribute_update_enabled = jit_user_prov_attribute_update_enabled

    @property
    def jit_user_prov_group_assignment_method(self):
        """
        Gets the jit_user_prov_group_assignment_method of this IdentityProvider.
        The default value is 'Overwrite', which tells Just-In-Time user-provisioning to replace any current group-assignments for a User with those assigned by assertions and/or those assigned statically. Specify 'Merge' if you want Just-In-Time user-provisioning to combine its group-assignments with those the user already has.

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "Overwrite", "Merge", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The jit_user_prov_group_assignment_method of this IdentityProvider.
        :rtype: str
        """
        return self._jit_user_prov_group_assignment_method

    @jit_user_prov_group_assignment_method.setter
    def jit_user_prov_group_assignment_method(self, jit_user_prov_group_assignment_method):
        """
        Sets the jit_user_prov_group_assignment_method of this IdentityProvider.
        The default value is 'Overwrite', which tells Just-In-Time user-provisioning to replace any current group-assignments for a User with those assigned by assertions and/or those assigned statically. Specify 'Merge' if you want Just-In-Time user-provisioning to combine its group-assignments with those the user already has.

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param jit_user_prov_group_assignment_method: The jit_user_prov_group_assignment_method of this IdentityProvider.
        :type: str
        """
        allowed_values = ["Overwrite", "Merge"]
        if not value_allowed_none_or_none_sentinel(jit_user_prov_group_assignment_method, allowed_values):
            jit_user_prov_group_assignment_method = 'UNKNOWN_ENUM_VALUE'
        self._jit_user_prov_group_assignment_method = jit_user_prov_group_assignment_method

    @property
    def jit_user_prov_group_mapping_mode(self):
        """
        Gets the jit_user_prov_group_mapping_mode of this IdentityProvider.
        Property to indicate the mode of group mapping

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "implicit", "explicit", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The jit_user_prov_group_mapping_mode of this IdentityProvider.
        :rtype: str
        """
        return self._jit_user_prov_group_mapping_mode

    @jit_user_prov_group_mapping_mode.setter
    def jit_user_prov_group_mapping_mode(self, jit_user_prov_group_mapping_mode):
        """
        Sets the jit_user_prov_group_mapping_mode of this IdentityProvider.
        Property to indicate the mode of group mapping

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param jit_user_prov_group_mapping_mode: The jit_user_prov_group_mapping_mode of this IdentityProvider.
        :type: str
        """
        allowed_values = ["implicit", "explicit"]
        if not value_allowed_none_or_none_sentinel(jit_user_prov_group_mapping_mode, allowed_values):
            jit_user_prov_group_mapping_mode = 'UNKNOWN_ENUM_VALUE'
        self._jit_user_prov_group_mapping_mode = jit_user_prov_group_mapping_mode

    @property
    def jit_user_prov_group_mappings(self):
        """
        Gets the jit_user_prov_group_mappings of this IdentityProvider.
        The list of mappings between the Identity Domain Group and the IDP group.

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - idcsCompositeKey: [idpGroup]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The jit_user_prov_group_mappings of this IdentityProvider.
        :rtype: list[oci.identity_domains.models.IdentityProviderJitUserProvGroupMappings]
        """
        return self._jit_user_prov_group_mappings

    @jit_user_prov_group_mappings.setter
    def jit_user_prov_group_mappings(self, jit_user_prov_group_mappings):
        """
        Sets the jit_user_prov_group_mappings of this IdentityProvider.
        The list of mappings between the Identity Domain Group and the IDP group.

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - idcsCompositeKey: [idpGroup]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param jit_user_prov_group_mappings: The jit_user_prov_group_mappings of this IdentityProvider.
        :type: list[oci.identity_domains.models.IdentityProviderJitUserProvGroupMappings]
        """
        self._jit_user_prov_group_mappings = jit_user_prov_group_mappings

    @property
    def jit_user_prov_group_saml_attribute_name(self):
        """
        Gets the jit_user_prov_group_saml_attribute_name of this IdentityProvider.
        Name of the assertion attribute containing the users groups

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The jit_user_prov_group_saml_attribute_name of this IdentityProvider.
        :rtype: str
        """
        return self._jit_user_prov_group_saml_attribute_name

    @jit_user_prov_group_saml_attribute_name.setter
    def jit_user_prov_group_saml_attribute_name(self, jit_user_prov_group_saml_attribute_name):
        """
        Sets the jit_user_prov_group_saml_attribute_name of this IdentityProvider.
        Name of the assertion attribute containing the users groups

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param jit_user_prov_group_saml_attribute_name: The jit_user_prov_group_saml_attribute_name of this IdentityProvider.
        :type: str
        """
        self._jit_user_prov_group_saml_attribute_name = jit_user_prov_group_saml_attribute_name

    @property
    def service_instance_identifier(self):
        """
        Gets the service_instance_identifier of this IdentityProvider.
        The serviceInstanceIdentifier of the App that hosts this IdP. This value will match the opcServiceInstanceGUID of any service-instance that the IdP represents.

        **Added In:** 18.2.6

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: never
         - type: string
         - uniqueness: server


        :return: The service_instance_identifier of this IdentityProvider.
        :rtype: str
        """
        return self._service_instance_identifier

    @service_instance_identifier.setter
    def service_instance_identifier(self, service_instance_identifier):
        """
        Sets the service_instance_identifier of this IdentityProvider.
        The serviceInstanceIdentifier of the App that hosts this IdP. This value will match the opcServiceInstanceGUID of any service-instance that the IdP represents.

        **Added In:** 18.2.6

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: never
         - type: string
         - uniqueness: server


        :param service_instance_identifier: The service_instance_identifier of this IdentityProvider.
        :type: str
        """
        self._service_instance_identifier = service_instance_identifier

    @property
    def user_mapping_method(self):
        """
        Gets the user_mapping_method of this IdentityProvider.
        User mapping method.

        **Deprecated Since: 20.1.3**

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsValuePersistedInOtherAttribute: true

        Allowed values for this property are: "NameIDToUserAttribute", "AssertionAttributeToUserAttribute", "CorrelationPolicyRule", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The user_mapping_method of this IdentityProvider.
        :rtype: str
        """
        return self._user_mapping_method

    @user_mapping_method.setter
    def user_mapping_method(self, user_mapping_method):
        """
        Sets the user_mapping_method of this IdentityProvider.
        User mapping method.

        **Deprecated Since: 20.1.3**

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsValuePersistedInOtherAttribute: true


        :param user_mapping_method: The user_mapping_method of this IdentityProvider.
        :type: str
        """
        allowed_values = ["NameIDToUserAttribute", "AssertionAttributeToUserAttribute", "CorrelationPolicyRule"]
        if not value_allowed_none_or_none_sentinel(user_mapping_method, allowed_values):
            user_mapping_method = 'UNKNOWN_ENUM_VALUE'
        self._user_mapping_method = user_mapping_method

    @property
    def user_mapping_store_attribute(self):
        """
        Gets the user_mapping_store_attribute of this IdentityProvider.
        This property specifies the userstore attribute value that must match the incoming assertion attribute value or the incoming nameid attribute value in order to identify the user during SSO.<br>You can construct the userMappingStoreAttribute value by specifying attributes from the Oracle Identity Cloud Service Core Users schema. For examples of how to construct the userMappingStoreAttribute value, see the <b>Example of a Request Body</b> section of the Examples tab for the <a href='./op-admin-v1-identityproviders-post.html'>POST</a> and <a href='./op-admin-v1-identityproviders-id-put.html'>PUT</a> methods of the /IdentityProviders endpoint.

        **Deprecated Since: 20.1.3**

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsValuePersistedInOtherAttribute: true


        :return: The user_mapping_store_attribute of this IdentityProvider.
        :rtype: str
        """
        return self._user_mapping_store_attribute

    @user_mapping_store_attribute.setter
    def user_mapping_store_attribute(self, user_mapping_store_attribute):
        """
        Sets the user_mapping_store_attribute of this IdentityProvider.
        This property specifies the userstore attribute value that must match the incoming assertion attribute value or the incoming nameid attribute value in order to identify the user during SSO.<br>You can construct the userMappingStoreAttribute value by specifying attributes from the Oracle Identity Cloud Service Core Users schema. For examples of how to construct the userMappingStoreAttribute value, see the <b>Example of a Request Body</b> section of the Examples tab for the <a href='./op-admin-v1-identityproviders-post.html'>POST</a> and <a href='./op-admin-v1-identityproviders-id-put.html'>PUT</a> methods of the /IdentityProviders endpoint.

        **Deprecated Since: 20.1.3**

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsValuePersistedInOtherAttribute: true


        :param user_mapping_store_attribute: The user_mapping_store_attribute of this IdentityProvider.
        :type: str
        """
        self._user_mapping_store_attribute = user_mapping_store_attribute

    @property
    def assertion_attribute(self):
        """
        Gets the assertion_attribute of this IdentityProvider.
        Assertion attribute name.

        **Deprecated Since: 20.1.3**

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsValuePersistedInOtherAttribute: true


        :return: The assertion_attribute of this IdentityProvider.
        :rtype: str
        """
        return self._assertion_attribute

    @assertion_attribute.setter
    def assertion_attribute(self, assertion_attribute):
        """
        Sets the assertion_attribute of this IdentityProvider.
        Assertion attribute name.

        **Deprecated Since: 20.1.3**

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsValuePersistedInOtherAttribute: true


        :param assertion_attribute: The assertion_attribute of this IdentityProvider.
        :type: str
        """
        self._assertion_attribute = assertion_attribute

    @property
    def type(self):
        """
        Gets the type of this IdentityProvider.
        Identity Provider Type

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: always
         - type: string
         - uniqueness: none

        Allowed values for this property are: "SAML", "SOCIAL", "IWA", "X509", "LOCAL", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this IdentityProvider.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this IdentityProvider.
        Identity Provider Type

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: always
         - type: string
         - uniqueness: none


        :param type: The type of this IdentityProvider.
        :type: str
        """
        allowed_values = ["SAML", "SOCIAL", "IWA", "X509", "LOCAL"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def require_force_authn(self):
        """
        Gets the require_force_authn of this IdentityProvider.
        This SP requires requests SAML IdP to enforce re-authentication.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The require_force_authn of this IdentityProvider.
        :rtype: bool
        """
        return self._require_force_authn

    @require_force_authn.setter
    def require_force_authn(self, require_force_authn):
        """
        Sets the require_force_authn of this IdentityProvider.
        This SP requires requests SAML IdP to enforce re-authentication.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param require_force_authn: The require_force_authn of this IdentityProvider.
        :type: bool
        """
        self._require_force_authn = require_force_authn

    @property
    def requires_encrypted_assertion(self):
        """
        Gets the requires_encrypted_assertion of this IdentityProvider.
        SAML SP must accept encrypted assertion only.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The requires_encrypted_assertion of this IdentityProvider.
        :rtype: bool
        """
        return self._requires_encrypted_assertion

    @requires_encrypted_assertion.setter
    def requires_encrypted_assertion(self, requires_encrypted_assertion):
        """
        Sets the requires_encrypted_assertion of this IdentityProvider.
        SAML SP must accept encrypted assertion only.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param requires_encrypted_assertion: The requires_encrypted_assertion of this IdentityProvider.
        :type: bool
        """
        self._requires_encrypted_assertion = requires_encrypted_assertion

    @property
    def saml_ho_k_required(self):
        """
        Gets the saml_ho_k_required of this IdentityProvider.
        SAML SP HoK Enabled.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The saml_ho_k_required of this IdentityProvider.
        :rtype: bool
        """
        return self._saml_ho_k_required

    @saml_ho_k_required.setter
    def saml_ho_k_required(self, saml_ho_k_required):
        """
        Sets the saml_ho_k_required of this IdentityProvider.
        SAML SP HoK Enabled.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param saml_ho_k_required: The saml_ho_k_required of this IdentityProvider.
        :type: bool
        """
        self._saml_ho_k_required = saml_ho_k_required

    @property
    def requested_authentication_context(self):
        """
        Gets the requested_authentication_context of this IdentityProvider.
        SAML SP authentication type.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The requested_authentication_context of this IdentityProvider.
        :rtype: list[str]
        """
        return self._requested_authentication_context

    @requested_authentication_context.setter
    def requested_authentication_context(self, requested_authentication_context):
        """
        Sets the requested_authentication_context of this IdentityProvider.
        SAML SP authentication type.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param requested_authentication_context: The requested_authentication_context of this IdentityProvider.
        :type: list[str]
        """
        self._requested_authentication_context = requested_authentication_context

    @property
    def jit_user_prov_ignore_error_on_absent_groups(self):
        """
        Gets the jit_user_prov_ignore_error_on_absent_groups of this IdentityProvider.
        Set to true to indicate ignoring absence of group while provisioning

        **Added In:** 2111112015

        **SCIM++ Properties:**
         - caseExact: false
         - idcsAddedSinceVersion: 30
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The jit_user_prov_ignore_error_on_absent_groups of this IdentityProvider.
        :rtype: bool
        """
        return self._jit_user_prov_ignore_error_on_absent_groups

    @jit_user_prov_ignore_error_on_absent_groups.setter
    def jit_user_prov_ignore_error_on_absent_groups(self, jit_user_prov_ignore_error_on_absent_groups):
        """
        Sets the jit_user_prov_ignore_error_on_absent_groups of this IdentityProvider.
        Set to true to indicate ignoring absence of group while provisioning

        **Added In:** 2111112015

        **SCIM++ Properties:**
         - caseExact: false
         - idcsAddedSinceVersion: 30
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param jit_user_prov_ignore_error_on_absent_groups: The jit_user_prov_ignore_error_on_absent_groups of this IdentityProvider.
        :type: bool
        """
        self._jit_user_prov_ignore_error_on_absent_groups = jit_user_prov_ignore_error_on_absent_groups

    @property
    def jit_user_prov_attributes(self):
        """
        Gets the jit_user_prov_attributes of this IdentityProvider.

        :return: The jit_user_prov_attributes of this IdentityProvider.
        :rtype: oci.identity_domains.models.IdentityProviderJitUserProvAttributes
        """
        return self._jit_user_prov_attributes

    @jit_user_prov_attributes.setter
    def jit_user_prov_attributes(self, jit_user_prov_attributes):
        """
        Sets the jit_user_prov_attributes of this IdentityProvider.

        :param jit_user_prov_attributes: The jit_user_prov_attributes of this IdentityProvider.
        :type: oci.identity_domains.models.IdentityProviderJitUserProvAttributes
        """
        self._jit_user_prov_attributes = jit_user_prov_attributes

    @property
    def jit_user_prov_assigned_groups(self):
        """
        Gets the jit_user_prov_assigned_groups of this IdentityProvider.
        Refers to every group of which a JIT-provisioned User should be a member.  Just-in-Time user-provisioning applies this static list when jitUserProvGroupStaticListEnabled:true.

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The jit_user_prov_assigned_groups of this IdentityProvider.
        :rtype: list[oci.identity_domains.models.IdentityProviderJitUserProvAssignedGroups]
        """
        return self._jit_user_prov_assigned_groups

    @jit_user_prov_assigned_groups.setter
    def jit_user_prov_assigned_groups(self, jit_user_prov_assigned_groups):
        """
        Sets the jit_user_prov_assigned_groups of this IdentityProvider.
        Refers to every group of which a JIT-provisioned User should be a member.  Just-in-Time user-provisioning applies this static list when jitUserProvGroupStaticListEnabled:true.

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param jit_user_prov_assigned_groups: The jit_user_prov_assigned_groups of this IdentityProvider.
        :type: list[oci.identity_domains.models.IdentityProviderJitUserProvAssignedGroups]
        """
        self._jit_user_prov_assigned_groups = jit_user_prov_assigned_groups

    @property
    def correlation_policy(self):
        """
        Gets the correlation_policy of this IdentityProvider.

        :return: The correlation_policy of this IdentityProvider.
        :rtype: oci.identity_domains.models.IdentityProviderCorrelationPolicy
        """
        return self._correlation_policy

    @correlation_policy.setter
    def correlation_policy(self, correlation_policy):
        """
        Sets the correlation_policy of this IdentityProvider.

        :param correlation_policy: The correlation_policy of this IdentityProvider.
        :type: oci.identity_domains.models.IdentityProviderCorrelationPolicy
        """
        self._correlation_policy = correlation_policy

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider of this IdentityProvider.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider of this IdentityProvider.
        :rtype: oci.identity_domains.models.ExtensionSocialIdentityProvider
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider of this IdentityProvider.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider: The urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider of this IdentityProvider.
        :type: oci.identity_domains.models.ExtensionSocialIdentityProvider
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider = urn_ietf_params_scim_schemas_oracle_idcs_extension_social_identity_provider

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider of this IdentityProvider.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider of this IdentityProvider.
        :rtype: oci.identity_domains.models.ExtensionX509IdentityProvider
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider of this IdentityProvider.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider: The urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider of this IdentityProvider.
        :type: oci.identity_domains.models.ExtensionX509IdentityProvider
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider = urn_ietf_params_scim_schemas_oracle_idcs_extension_x509_identity_provider

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
