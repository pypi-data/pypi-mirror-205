# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .job_infrastructure_configuration_details import JobInfrastructureConfigurationDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class StandaloneJobInfrastructureConfigurationDetails(JobInfrastructureConfigurationDetails):
    """
    The standalone job infrastructure configuration.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new StandaloneJobInfrastructureConfigurationDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.data_science.models.StandaloneJobInfrastructureConfigurationDetails.job_infrastructure_type` attribute
        of this class is ``STANDALONE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param job_infrastructure_type:
            The value to assign to the job_infrastructure_type property of this StandaloneJobInfrastructureConfigurationDetails.
            Allowed values for this property are: "STANDALONE", "ME_STANDALONE"
        :type job_infrastructure_type: str

        :param shape_name:
            The value to assign to the shape_name property of this StandaloneJobInfrastructureConfigurationDetails.
        :type shape_name: str

        :param subnet_id:
            The value to assign to the subnet_id property of this StandaloneJobInfrastructureConfigurationDetails.
        :type subnet_id: str

        :param block_storage_size_in_gbs:
            The value to assign to the block_storage_size_in_gbs property of this StandaloneJobInfrastructureConfigurationDetails.
        :type block_storage_size_in_gbs: int

        :param job_shape_config_details:
            The value to assign to the job_shape_config_details property of this StandaloneJobInfrastructureConfigurationDetails.
        :type job_shape_config_details: oci.data_science.models.JobShapeConfigDetails

        """
        self.swagger_types = {
            'job_infrastructure_type': 'str',
            'shape_name': 'str',
            'subnet_id': 'str',
            'block_storage_size_in_gbs': 'int',
            'job_shape_config_details': 'JobShapeConfigDetails'
        }

        self.attribute_map = {
            'job_infrastructure_type': 'jobInfrastructureType',
            'shape_name': 'shapeName',
            'subnet_id': 'subnetId',
            'block_storage_size_in_gbs': 'blockStorageSizeInGBs',
            'job_shape_config_details': 'jobShapeConfigDetails'
        }

        self._job_infrastructure_type = None
        self._shape_name = None
        self._subnet_id = None
        self._block_storage_size_in_gbs = None
        self._job_shape_config_details = None
        self._job_infrastructure_type = 'STANDALONE'

    @property
    def shape_name(self):
        """
        **[Required]** Gets the shape_name of this StandaloneJobInfrastructureConfigurationDetails.
        The shape used to launch the job run instances.


        :return: The shape_name of this StandaloneJobInfrastructureConfigurationDetails.
        :rtype: str
        """
        return self._shape_name

    @shape_name.setter
    def shape_name(self, shape_name):
        """
        Sets the shape_name of this StandaloneJobInfrastructureConfigurationDetails.
        The shape used to launch the job run instances.


        :param shape_name: The shape_name of this StandaloneJobInfrastructureConfigurationDetails.
        :type: str
        """
        self._shape_name = shape_name

    @property
    def subnet_id(self):
        """
        **[Required]** Gets the subnet_id of this StandaloneJobInfrastructureConfigurationDetails.
        The subnet to create a secondary vnic in to attach to the instance running the job


        :return: The subnet_id of this StandaloneJobInfrastructureConfigurationDetails.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this StandaloneJobInfrastructureConfigurationDetails.
        The subnet to create a secondary vnic in to attach to the instance running the job


        :param subnet_id: The subnet_id of this StandaloneJobInfrastructureConfigurationDetails.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def block_storage_size_in_gbs(self):
        """
        **[Required]** Gets the block_storage_size_in_gbs of this StandaloneJobInfrastructureConfigurationDetails.
        The size of the block storage volume to attach to the instance running the job


        :return: The block_storage_size_in_gbs of this StandaloneJobInfrastructureConfigurationDetails.
        :rtype: int
        """
        return self._block_storage_size_in_gbs

    @block_storage_size_in_gbs.setter
    def block_storage_size_in_gbs(self, block_storage_size_in_gbs):
        """
        Sets the block_storage_size_in_gbs of this StandaloneJobInfrastructureConfigurationDetails.
        The size of the block storage volume to attach to the instance running the job


        :param block_storage_size_in_gbs: The block_storage_size_in_gbs of this StandaloneJobInfrastructureConfigurationDetails.
        :type: int
        """
        self._block_storage_size_in_gbs = block_storage_size_in_gbs

    @property
    def job_shape_config_details(self):
        """
        Gets the job_shape_config_details of this StandaloneJobInfrastructureConfigurationDetails.

        :return: The job_shape_config_details of this StandaloneJobInfrastructureConfigurationDetails.
        :rtype: oci.data_science.models.JobShapeConfigDetails
        """
        return self._job_shape_config_details

    @job_shape_config_details.setter
    def job_shape_config_details(self, job_shape_config_details):
        """
        Sets the job_shape_config_details of this StandaloneJobInfrastructureConfigurationDetails.

        :param job_shape_config_details: The job_shape_config_details of this StandaloneJobInfrastructureConfigurationDetails.
        :type: oci.data_science.models.JobShapeConfigDetails
        """
        self._job_shape_config_details = job_shape_config_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
