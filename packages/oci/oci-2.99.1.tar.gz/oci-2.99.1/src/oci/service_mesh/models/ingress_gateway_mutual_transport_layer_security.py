# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class IngressGatewayMutualTransportLayerSecurity(object):
    """
    Mutual TLS settings used when sending requests to virtual services within the mesh.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new IngressGatewayMutualTransportLayerSecurity object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param certificate_id:
            The value to assign to the certificate_id property of this IngressGatewayMutualTransportLayerSecurity.
        :type certificate_id: str

        :param maximum_validity:
            The value to assign to the maximum_validity property of this IngressGatewayMutualTransportLayerSecurity.
        :type maximum_validity: int

        """
        self.swagger_types = {
            'certificate_id': 'str',
            'maximum_validity': 'int'
        }

        self.attribute_map = {
            'certificate_id': 'certificateId',
            'maximum_validity': 'maximumValidity'
        }

        self._certificate_id = None
        self._maximum_validity = None

    @property
    def certificate_id(self):
        """
        **[Required]** Gets the certificate_id of this IngressGatewayMutualTransportLayerSecurity.
        The OCID of the certificate resource that will be used for mTLS authentication with other virtual services in the mesh.


        :return: The certificate_id of this IngressGatewayMutualTransportLayerSecurity.
        :rtype: str
        """
        return self._certificate_id

    @certificate_id.setter
    def certificate_id(self, certificate_id):
        """
        Sets the certificate_id of this IngressGatewayMutualTransportLayerSecurity.
        The OCID of the certificate resource that will be used for mTLS authentication with other virtual services in the mesh.


        :param certificate_id: The certificate_id of this IngressGatewayMutualTransportLayerSecurity.
        :type: str
        """
        self._certificate_id = certificate_id

    @property
    def maximum_validity(self):
        """
        Gets the maximum_validity of this IngressGatewayMutualTransportLayerSecurity.
        The number of days the mTLS certificate is valid.  This value should be less than the Maximum Validity Duration
        for Certificates (Days) setting on the Certificate Authority associated with this Mesh.  The certificate will
        be automatically renewed after 2/3 of the validity period, so a certificate with a maximum validity of 45 days
        will be renewed every 30 days.


        :return: The maximum_validity of this IngressGatewayMutualTransportLayerSecurity.
        :rtype: int
        """
        return self._maximum_validity

    @maximum_validity.setter
    def maximum_validity(self, maximum_validity):
        """
        Sets the maximum_validity of this IngressGatewayMutualTransportLayerSecurity.
        The number of days the mTLS certificate is valid.  This value should be less than the Maximum Validity Duration
        for Certificates (Days) setting on the Certificate Authority associated with this Mesh.  The certificate will
        be automatically renewed after 2/3 of the validity period, so a certificate with a maximum validity of 45 days
        will be renewed every 30 days.


        :param maximum_validity: The maximum_validity of this IngressGatewayMutualTransportLayerSecurity.
        :type: int
        """
        self._maximum_validity = maximum_validity

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
