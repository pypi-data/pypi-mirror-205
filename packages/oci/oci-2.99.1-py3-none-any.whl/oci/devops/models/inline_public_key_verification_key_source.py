# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .verification_key_source import VerificationKeySource
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class InlinePublicKeyVerificationKeySource(VerificationKeySource):
    """
    Specifies the Inline public key verification source details
    """

    def __init__(self, **kwargs):
        """
        Initializes a new InlinePublicKeyVerificationKeySource object with values from keyword arguments. The default value of the :py:attr:`~oci.devops.models.InlinePublicKeyVerificationKeySource.verification_key_source_type` attribute
        of this class is ``INLINE_PUBLIC_KEY`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param verification_key_source_type:
            The value to assign to the verification_key_source_type property of this InlinePublicKeyVerificationKeySource.
            Allowed values for this property are: "VAULT_SECRET", "INLINE_PUBLIC_KEY", "NONE"
        :type verification_key_source_type: str

        :param current_public_key:
            The value to assign to the current_public_key property of this InlinePublicKeyVerificationKeySource.
        :type current_public_key: str

        :param previous_public_key:
            The value to assign to the previous_public_key property of this InlinePublicKeyVerificationKeySource.
        :type previous_public_key: str

        """
        self.swagger_types = {
            'verification_key_source_type': 'str',
            'current_public_key': 'str',
            'previous_public_key': 'str'
        }

        self.attribute_map = {
            'verification_key_source_type': 'verificationKeySourceType',
            'current_public_key': 'currentPublicKey',
            'previous_public_key': 'previousPublicKey'
        }

        self._verification_key_source_type = None
        self._current_public_key = None
        self._previous_public_key = None
        self._verification_key_source_type = 'INLINE_PUBLIC_KEY'

    @property
    def current_public_key(self):
        """
        **[Required]** Gets the current_public_key of this InlinePublicKeyVerificationKeySource.
        Current version of Base64 encoding of the public key which is in binary GPG exported format.


        :return: The current_public_key of this InlinePublicKeyVerificationKeySource.
        :rtype: str
        """
        return self._current_public_key

    @current_public_key.setter
    def current_public_key(self, current_public_key):
        """
        Sets the current_public_key of this InlinePublicKeyVerificationKeySource.
        Current version of Base64 encoding of the public key which is in binary GPG exported format.


        :param current_public_key: The current_public_key of this InlinePublicKeyVerificationKeySource.
        :type: str
        """
        self._current_public_key = current_public_key

    @property
    def previous_public_key(self):
        """
        Gets the previous_public_key of this InlinePublicKeyVerificationKeySource.
        Previous version of Base64 encoding of the public key which is in binary GPG exported format. This would be used for key rotation scenarios.


        :return: The previous_public_key of this InlinePublicKeyVerificationKeySource.
        :rtype: str
        """
        return self._previous_public_key

    @previous_public_key.setter
    def previous_public_key(self, previous_public_key):
        """
        Sets the previous_public_key of this InlinePublicKeyVerificationKeySource.
        Previous version of Base64 encoding of the public key which is in binary GPG exported format. This would be used for key rotation scenarios.


        :param previous_public_key: The previous_public_key of this InlinePublicKeyVerificationKeySource.
        :type: str
        """
        self._previous_public_key = previous_public_key

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
