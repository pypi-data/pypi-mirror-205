# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .ca_bundle import CaBundle
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CertificatesCertificateAuthority(CaBundle):
    """
    Certificate Authority from Certificates Service that should be used on the gateway for TLS validation
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CertificatesCertificateAuthority object with values from keyword arguments. The default value of the :py:attr:`~oci.apigateway.models.CertificatesCertificateAuthority.type` attribute
        of this class is ``CERTIFICATE_AUTHORITY`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this CertificatesCertificateAuthority.
            Allowed values for this property are: "CA_BUNDLE", "CERTIFICATE_AUTHORITY"
        :type type: str

        :param certificate_authority_id:
            The value to assign to the certificate_authority_id property of this CertificatesCertificateAuthority.
        :type certificate_authority_id: str

        """
        self.swagger_types = {
            'type': 'str',
            'certificate_authority_id': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'certificate_authority_id': 'certificateAuthorityId'
        }

        self._type = None
        self._certificate_authority_id = None
        self._type = 'CERTIFICATE_AUTHORITY'

    @property
    def certificate_authority_id(self):
        """
        Gets the certificate_authority_id of this CertificatesCertificateAuthority.
        The `OCID`__ of the resource.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The certificate_authority_id of this CertificatesCertificateAuthority.
        :rtype: str
        """
        return self._certificate_authority_id

    @certificate_authority_id.setter
    def certificate_authority_id(self, certificate_authority_id):
        """
        Sets the certificate_authority_id of this CertificatesCertificateAuthority.
        The `OCID`__ of the resource.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param certificate_authority_id: The certificate_authority_id of this CertificatesCertificateAuthority.
        :type: str
        """
        self._certificate_authority_id = certificate_authority_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
