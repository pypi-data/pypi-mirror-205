# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ImportDeploymentWalletDetails(object):
    """
    Metadata required to import wallet to deployment
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ImportDeploymentWalletDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param vault_id:
            The value to assign to the vault_id property of this ImportDeploymentWalletDetails.
        :type vault_id: str

        :param new_wallet_secret_id:
            The value to assign to the new_wallet_secret_id property of this ImportDeploymentWalletDetails.
        :type new_wallet_secret_id: str

        :param wallet_backup_secret_name:
            The value to assign to the wallet_backup_secret_name property of this ImportDeploymentWalletDetails.
        :type wallet_backup_secret_name: str

        :param master_encryption_key_id:
            The value to assign to the master_encryption_key_id property of this ImportDeploymentWalletDetails.
        :type master_encryption_key_id: str

        :param description:
            The value to assign to the description property of this ImportDeploymentWalletDetails.
        :type description: str

        """
        self.swagger_types = {
            'vault_id': 'str',
            'new_wallet_secret_id': 'str',
            'wallet_backup_secret_name': 'str',
            'master_encryption_key_id': 'str',
            'description': 'str'
        }

        self.attribute_map = {
            'vault_id': 'vaultId',
            'new_wallet_secret_id': 'newWalletSecretId',
            'wallet_backup_secret_name': 'walletBackupSecretName',
            'master_encryption_key_id': 'masterEncryptionKeyId',
            'description': 'description'
        }

        self._vault_id = None
        self._new_wallet_secret_id = None
        self._wallet_backup_secret_name = None
        self._master_encryption_key_id = None
        self._description = None

    @property
    def vault_id(self):
        """
        **[Required]** Gets the vault_id of this ImportDeploymentWalletDetails.
        Refers to the customer's vault OCID.
        If provided, it references a vault where GoldenGate can manage secrets. Customers must add policies to permit GoldenGate
        to manage secrets contained within this vault.


        :return: The vault_id of this ImportDeploymentWalletDetails.
        :rtype: str
        """
        return self._vault_id

    @vault_id.setter
    def vault_id(self, vault_id):
        """
        Sets the vault_id of this ImportDeploymentWalletDetails.
        Refers to the customer's vault OCID.
        If provided, it references a vault where GoldenGate can manage secrets. Customers must add policies to permit GoldenGate
        to manage secrets contained within this vault.


        :param vault_id: The vault_id of this ImportDeploymentWalletDetails.
        :type: str
        """
        self._vault_id = vault_id

    @property
    def new_wallet_secret_id(self):
        """
        **[Required]** Gets the new_wallet_secret_id of this ImportDeploymentWalletDetails.
        The OCID of the customer's GoldenGate Service Secret.
        If provided, it references a key that customers will be required to ensure the policies are established
        to permit GoldenGate to use this Secret.


        :return: The new_wallet_secret_id of this ImportDeploymentWalletDetails.
        :rtype: str
        """
        return self._new_wallet_secret_id

    @new_wallet_secret_id.setter
    def new_wallet_secret_id(self, new_wallet_secret_id):
        """
        Sets the new_wallet_secret_id of this ImportDeploymentWalletDetails.
        The OCID of the customer's GoldenGate Service Secret.
        If provided, it references a key that customers will be required to ensure the policies are established
        to permit GoldenGate to use this Secret.


        :param new_wallet_secret_id: The new_wallet_secret_id of this ImportDeploymentWalletDetails.
        :type: str
        """
        self._new_wallet_secret_id = new_wallet_secret_id

    @property
    def wallet_backup_secret_name(self):
        """
        Gets the wallet_backup_secret_name of this ImportDeploymentWalletDetails.
        Name of the secret with which secret is shown in vault


        :return: The wallet_backup_secret_name of this ImportDeploymentWalletDetails.
        :rtype: str
        """
        return self._wallet_backup_secret_name

    @wallet_backup_secret_name.setter
    def wallet_backup_secret_name(self, wallet_backup_secret_name):
        """
        Sets the wallet_backup_secret_name of this ImportDeploymentWalletDetails.
        Name of the secret with which secret is shown in vault


        :param wallet_backup_secret_name: The wallet_backup_secret_name of this ImportDeploymentWalletDetails.
        :type: str
        """
        self._wallet_backup_secret_name = wallet_backup_secret_name

    @property
    def master_encryption_key_id(self):
        """
        Gets the master_encryption_key_id of this ImportDeploymentWalletDetails.
        Refers to the customer's master key OCID.
        If provided, it references a key to manage secrets. Customers must add policies to permit GoldenGate to use this key.


        :return: The master_encryption_key_id of this ImportDeploymentWalletDetails.
        :rtype: str
        """
        return self._master_encryption_key_id

    @master_encryption_key_id.setter
    def master_encryption_key_id(self, master_encryption_key_id):
        """
        Sets the master_encryption_key_id of this ImportDeploymentWalletDetails.
        Refers to the customer's master key OCID.
        If provided, it references a key to manage secrets. Customers must add policies to permit GoldenGate to use this key.


        :param master_encryption_key_id: The master_encryption_key_id of this ImportDeploymentWalletDetails.
        :type: str
        """
        self._master_encryption_key_id = master_encryption_key_id

    @property
    def description(self):
        """
        Gets the description of this ImportDeploymentWalletDetails.
        Metadata about this specific object.


        :return: The description of this ImportDeploymentWalletDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ImportDeploymentWalletDetails.
        Metadata about this specific object.


        :param description: The description of this ImportDeploymentWalletDetails.
        :type: str
        """
        self._description = description

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
