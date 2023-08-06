# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .mapped_secret import MappedSecret
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VaultMappedSecret(MappedSecret):
    """
    Mapped secret stored in OCI vault used in the firewall policy rules.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VaultMappedSecret object with values from keyword arguments. The default value of the :py:attr:`~oci.network_firewall.models.VaultMappedSecret.source` attribute
        of this class is ``OCI_VAULT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source:
            The value to assign to the source property of this VaultMappedSecret.
        :type source: str

        :param type:
            The value to assign to the type property of this VaultMappedSecret.
            Allowed values for this property are: "SSL_INBOUND_INSPECTION", "SSL_FORWARD_PROXY"
        :type type: str

        :param vault_secret_id:
            The value to assign to the vault_secret_id property of this VaultMappedSecret.
        :type vault_secret_id: str

        :param version_number:
            The value to assign to the version_number property of this VaultMappedSecret.
        :type version_number: int

        """
        self.swagger_types = {
            'source': 'str',
            'type': 'str',
            'vault_secret_id': 'str',
            'version_number': 'int'
        }

        self.attribute_map = {
            'source': 'source',
            'type': 'type',
            'vault_secret_id': 'vaultSecretId',
            'version_number': 'versionNumber'
        }

        self._source = None
        self._type = None
        self._vault_secret_id = None
        self._version_number = None
        self._source = 'OCI_VAULT'

    @property
    def vault_secret_id(self):
        """
        **[Required]** Gets the vault_secret_id of this VaultMappedSecret.
        OCID for the Vault Secret to be used.


        :return: The vault_secret_id of this VaultMappedSecret.
        :rtype: str
        """
        return self._vault_secret_id

    @vault_secret_id.setter
    def vault_secret_id(self, vault_secret_id):
        """
        Sets the vault_secret_id of this VaultMappedSecret.
        OCID for the Vault Secret to be used.


        :param vault_secret_id: The vault_secret_id of this VaultMappedSecret.
        :type: str
        """
        self._vault_secret_id = vault_secret_id

    @property
    def version_number(self):
        """
        **[Required]** Gets the version_number of this VaultMappedSecret.
        Version number of the secret to be used.


        :return: The version_number of this VaultMappedSecret.
        :rtype: int
        """
        return self._version_number

    @version_number.setter
    def version_number(self, version_number):
        """
        Sets the version_number of this VaultMappedSecret.
        Version number of the secret to be used.


        :param version_number: The version_number of this VaultMappedSecret.
        :type: int
        """
        self._version_number = version_number

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
