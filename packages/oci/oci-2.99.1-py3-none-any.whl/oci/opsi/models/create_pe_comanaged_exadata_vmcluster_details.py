# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreatePeComanagedExadataVmclusterDetails(object):
    """
    The information of the VM Cluster which contains databases. Either an opsiPrivateEndpointId or dbmPrivateEndpointId must be specified. If the dbmPrivateEndpointId is specified, a new Operations Insights private endpoint will be created.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreatePeComanagedExadataVmclusterDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param vmcluster_id:
            The value to assign to the vmcluster_id property of this CreatePeComanagedExadataVmclusterDetails.
        :type vmcluster_id: str

        :param opsi_private_endpoint_id:
            The value to assign to the opsi_private_endpoint_id property of this CreatePeComanagedExadataVmclusterDetails.
        :type opsi_private_endpoint_id: str

        :param member_database_details:
            The value to assign to the member_database_details property of this CreatePeComanagedExadataVmclusterDetails.
        :type member_database_details: list[oci.opsi.models.CreatePeComanagedDatabaseInsightDetails]

        :param compartment_id:
            The value to assign to the compartment_id property of this CreatePeComanagedExadataVmclusterDetails.
        :type compartment_id: str

        """
        self.swagger_types = {
            'vmcluster_id': 'str',
            'opsi_private_endpoint_id': 'str',
            'member_database_details': 'list[CreatePeComanagedDatabaseInsightDetails]',
            'compartment_id': 'str'
        }

        self.attribute_map = {
            'vmcluster_id': 'vmclusterId',
            'opsi_private_endpoint_id': 'opsiPrivateEndpointId',
            'member_database_details': 'memberDatabaseDetails',
            'compartment_id': 'compartmentId'
        }

        self._vmcluster_id = None
        self._opsi_private_endpoint_id = None
        self._member_database_details = None
        self._compartment_id = None

    @property
    def vmcluster_id(self):
        """
        **[Required]** Gets the vmcluster_id of this CreatePeComanagedExadataVmclusterDetails.
        The `OCID`__ of the VM Cluster.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The vmcluster_id of this CreatePeComanagedExadataVmclusterDetails.
        :rtype: str
        """
        return self._vmcluster_id

    @vmcluster_id.setter
    def vmcluster_id(self, vmcluster_id):
        """
        Sets the vmcluster_id of this CreatePeComanagedExadataVmclusterDetails.
        The `OCID`__ of the VM Cluster.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param vmcluster_id: The vmcluster_id of this CreatePeComanagedExadataVmclusterDetails.
        :type: str
        """
        self._vmcluster_id = vmcluster_id

    @property
    def opsi_private_endpoint_id(self):
        """
        Gets the opsi_private_endpoint_id of this CreatePeComanagedExadataVmclusterDetails.
        The `OCID`__ of the OPSI private endpoint

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The opsi_private_endpoint_id of this CreatePeComanagedExadataVmclusterDetails.
        :rtype: str
        """
        return self._opsi_private_endpoint_id

    @opsi_private_endpoint_id.setter
    def opsi_private_endpoint_id(self, opsi_private_endpoint_id):
        """
        Sets the opsi_private_endpoint_id of this CreatePeComanagedExadataVmclusterDetails.
        The `OCID`__ of the OPSI private endpoint

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param opsi_private_endpoint_id: The opsi_private_endpoint_id of this CreatePeComanagedExadataVmclusterDetails.
        :type: str
        """
        self._opsi_private_endpoint_id = opsi_private_endpoint_id

    @property
    def member_database_details(self):
        """
        Gets the member_database_details of this CreatePeComanagedExadataVmclusterDetails.
        The databases that belong to the VM Cluster


        :return: The member_database_details of this CreatePeComanagedExadataVmclusterDetails.
        :rtype: list[oci.opsi.models.CreatePeComanagedDatabaseInsightDetails]
        """
        return self._member_database_details

    @member_database_details.setter
    def member_database_details(self, member_database_details):
        """
        Sets the member_database_details of this CreatePeComanagedExadataVmclusterDetails.
        The databases that belong to the VM Cluster


        :param member_database_details: The member_database_details of this CreatePeComanagedExadataVmclusterDetails.
        :type: list[oci.opsi.models.CreatePeComanagedDatabaseInsightDetails]
        """
        self._member_database_details = member_database_details

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreatePeComanagedExadataVmclusterDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreatePeComanagedExadataVmclusterDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreatePeComanagedExadataVmclusterDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreatePeComanagedExadataVmclusterDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
