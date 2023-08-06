# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateOdaPrivateEndpointAttachmentDetails(object):
    """
    Properties that are required to create an ODA private endpoint attachment.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateOdaPrivateEndpointAttachmentDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param oda_instance_id:
            The value to assign to the oda_instance_id property of this CreateOdaPrivateEndpointAttachmentDetails.
        :type oda_instance_id: str

        :param oda_private_endpoint_id:
            The value to assign to the oda_private_endpoint_id property of this CreateOdaPrivateEndpointAttachmentDetails.
        :type oda_private_endpoint_id: str

        """
        self.swagger_types = {
            'oda_instance_id': 'str',
            'oda_private_endpoint_id': 'str'
        }

        self.attribute_map = {
            'oda_instance_id': 'odaInstanceId',
            'oda_private_endpoint_id': 'odaPrivateEndpointId'
        }

        self._oda_instance_id = None
        self._oda_private_endpoint_id = None

    @property
    def oda_instance_id(self):
        """
        **[Required]** Gets the oda_instance_id of this CreateOdaPrivateEndpointAttachmentDetails.
        The `OCID`__ of the attached ODA Instance.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The oda_instance_id of this CreateOdaPrivateEndpointAttachmentDetails.
        :rtype: str
        """
        return self._oda_instance_id

    @oda_instance_id.setter
    def oda_instance_id(self, oda_instance_id):
        """
        Sets the oda_instance_id of this CreateOdaPrivateEndpointAttachmentDetails.
        The `OCID`__ of the attached ODA Instance.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param oda_instance_id: The oda_instance_id of this CreateOdaPrivateEndpointAttachmentDetails.
        :type: str
        """
        self._oda_instance_id = oda_instance_id

    @property
    def oda_private_endpoint_id(self):
        """
        **[Required]** Gets the oda_private_endpoint_id of this CreateOdaPrivateEndpointAttachmentDetails.
        The `OCID`__ of the ODA Private Endpoint.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The oda_private_endpoint_id of this CreateOdaPrivateEndpointAttachmentDetails.
        :rtype: str
        """
        return self._oda_private_endpoint_id

    @oda_private_endpoint_id.setter
    def oda_private_endpoint_id(self, oda_private_endpoint_id):
        """
        Sets the oda_private_endpoint_id of this CreateOdaPrivateEndpointAttachmentDetails.
        The `OCID`__ of the ODA Private Endpoint.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param oda_private_endpoint_id: The oda_private_endpoint_id of this CreateOdaPrivateEndpointAttachmentDetails.
        :type: str
        """
        self._oda_private_endpoint_id = oda_private_endpoint_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
