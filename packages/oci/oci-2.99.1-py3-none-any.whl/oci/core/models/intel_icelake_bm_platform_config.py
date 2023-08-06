# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .platform_config import PlatformConfig
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class IntelIcelakeBmPlatformConfig(PlatformConfig):
    """
    The platform configuration of a bare metal instance that uses the BM.Standard3.64 shape or the
    BM.Optimized3.36 shape (the Intel Ice Lake platform).
    """

    #: A constant which can be used with the numa_nodes_per_socket property of a IntelIcelakeBmPlatformConfig.
    #: This constant has a value of "NPS1"
    NUMA_NODES_PER_SOCKET_NPS1 = "NPS1"

    #: A constant which can be used with the numa_nodes_per_socket property of a IntelIcelakeBmPlatformConfig.
    #: This constant has a value of "NPS2"
    NUMA_NODES_PER_SOCKET_NPS2 = "NPS2"

    def __init__(self, **kwargs):
        """
        Initializes a new IntelIcelakeBmPlatformConfig object with values from keyword arguments. The default value of the :py:attr:`~oci.core.models.IntelIcelakeBmPlatformConfig.type` attribute
        of this class is ``INTEL_ICELAKE_BM`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this IntelIcelakeBmPlatformConfig.
            Allowed values for this property are: "AMD_MILAN_BM", "AMD_MILAN_BM_GPU", "AMD_ROME_BM", "AMD_ROME_BM_GPU", "INTEL_ICELAKE_BM", "INTEL_SKYLAKE_BM", "AMD_VM", "INTEL_VM", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param is_secure_boot_enabled:
            The value to assign to the is_secure_boot_enabled property of this IntelIcelakeBmPlatformConfig.
        :type is_secure_boot_enabled: bool

        :param is_trusted_platform_module_enabled:
            The value to assign to the is_trusted_platform_module_enabled property of this IntelIcelakeBmPlatformConfig.
        :type is_trusted_platform_module_enabled: bool

        :param is_measured_boot_enabled:
            The value to assign to the is_measured_boot_enabled property of this IntelIcelakeBmPlatformConfig.
        :type is_measured_boot_enabled: bool

        :param is_memory_encryption_enabled:
            The value to assign to the is_memory_encryption_enabled property of this IntelIcelakeBmPlatformConfig.
        :type is_memory_encryption_enabled: bool

        :param numa_nodes_per_socket:
            The value to assign to the numa_nodes_per_socket property of this IntelIcelakeBmPlatformConfig.
            Allowed values for this property are: "NPS1", "NPS2", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type numa_nodes_per_socket: str

        :param is_symmetric_multi_threading_enabled:
            The value to assign to the is_symmetric_multi_threading_enabled property of this IntelIcelakeBmPlatformConfig.
        :type is_symmetric_multi_threading_enabled: bool

        :param is_input_output_memory_management_unit_enabled:
            The value to assign to the is_input_output_memory_management_unit_enabled property of this IntelIcelakeBmPlatformConfig.
        :type is_input_output_memory_management_unit_enabled: bool

        :param percentage_of_cores_enabled:
            The value to assign to the percentage_of_cores_enabled property of this IntelIcelakeBmPlatformConfig.
        :type percentage_of_cores_enabled: int

        """
        self.swagger_types = {
            'type': 'str',
            'is_secure_boot_enabled': 'bool',
            'is_trusted_platform_module_enabled': 'bool',
            'is_measured_boot_enabled': 'bool',
            'is_memory_encryption_enabled': 'bool',
            'numa_nodes_per_socket': 'str',
            'is_symmetric_multi_threading_enabled': 'bool',
            'is_input_output_memory_management_unit_enabled': 'bool',
            'percentage_of_cores_enabled': 'int'
        }

        self.attribute_map = {
            'type': 'type',
            'is_secure_boot_enabled': 'isSecureBootEnabled',
            'is_trusted_platform_module_enabled': 'isTrustedPlatformModuleEnabled',
            'is_measured_boot_enabled': 'isMeasuredBootEnabled',
            'is_memory_encryption_enabled': 'isMemoryEncryptionEnabled',
            'numa_nodes_per_socket': 'numaNodesPerSocket',
            'is_symmetric_multi_threading_enabled': 'isSymmetricMultiThreadingEnabled',
            'is_input_output_memory_management_unit_enabled': 'isInputOutputMemoryManagementUnitEnabled',
            'percentage_of_cores_enabled': 'percentageOfCoresEnabled'
        }

        self._type = None
        self._is_secure_boot_enabled = None
        self._is_trusted_platform_module_enabled = None
        self._is_measured_boot_enabled = None
        self._is_memory_encryption_enabled = None
        self._numa_nodes_per_socket = None
        self._is_symmetric_multi_threading_enabled = None
        self._is_input_output_memory_management_unit_enabled = None
        self._percentage_of_cores_enabled = None
        self._type = 'INTEL_ICELAKE_BM'

    @property
    def numa_nodes_per_socket(self):
        """
        Gets the numa_nodes_per_socket of this IntelIcelakeBmPlatformConfig.
        The number of NUMA nodes per socket (NPS).

        Allowed values for this property are: "NPS1", "NPS2", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The numa_nodes_per_socket of this IntelIcelakeBmPlatformConfig.
        :rtype: str
        """
        return self._numa_nodes_per_socket

    @numa_nodes_per_socket.setter
    def numa_nodes_per_socket(self, numa_nodes_per_socket):
        """
        Sets the numa_nodes_per_socket of this IntelIcelakeBmPlatformConfig.
        The number of NUMA nodes per socket (NPS).


        :param numa_nodes_per_socket: The numa_nodes_per_socket of this IntelIcelakeBmPlatformConfig.
        :type: str
        """
        allowed_values = ["NPS1", "NPS2"]
        if not value_allowed_none_or_none_sentinel(numa_nodes_per_socket, allowed_values):
            numa_nodes_per_socket = 'UNKNOWN_ENUM_VALUE'
        self._numa_nodes_per_socket = numa_nodes_per_socket

    @property
    def is_symmetric_multi_threading_enabled(self):
        """
        Gets the is_symmetric_multi_threading_enabled of this IntelIcelakeBmPlatformConfig.
        Whether symmetric multithreading is enabled on the instance. Symmetric multithreading is also
        called simultaneous multithreading (SMT) or Intel Hyper-Threading.

        Intel and AMD processors have two hardware execution threads per core (OCPU). SMT permits multiple
        independent threads of execution, to better use the resources and increase the efficiency
        of the CPU. When multithreading is disabled, only one thread is permitted to run on each core, which
        can provide higher or more predictable performance for some workloads.


        :return: The is_symmetric_multi_threading_enabled of this IntelIcelakeBmPlatformConfig.
        :rtype: bool
        """
        return self._is_symmetric_multi_threading_enabled

    @is_symmetric_multi_threading_enabled.setter
    def is_symmetric_multi_threading_enabled(self, is_symmetric_multi_threading_enabled):
        """
        Sets the is_symmetric_multi_threading_enabled of this IntelIcelakeBmPlatformConfig.
        Whether symmetric multithreading is enabled on the instance. Symmetric multithreading is also
        called simultaneous multithreading (SMT) or Intel Hyper-Threading.

        Intel and AMD processors have two hardware execution threads per core (OCPU). SMT permits multiple
        independent threads of execution, to better use the resources and increase the efficiency
        of the CPU. When multithreading is disabled, only one thread is permitted to run on each core, which
        can provide higher or more predictable performance for some workloads.


        :param is_symmetric_multi_threading_enabled: The is_symmetric_multi_threading_enabled of this IntelIcelakeBmPlatformConfig.
        :type: bool
        """
        self._is_symmetric_multi_threading_enabled = is_symmetric_multi_threading_enabled

    @property
    def is_input_output_memory_management_unit_enabled(self):
        """
        Gets the is_input_output_memory_management_unit_enabled of this IntelIcelakeBmPlatformConfig.
        Whether the input-output memory management unit is enabled.


        :return: The is_input_output_memory_management_unit_enabled of this IntelIcelakeBmPlatformConfig.
        :rtype: bool
        """
        return self._is_input_output_memory_management_unit_enabled

    @is_input_output_memory_management_unit_enabled.setter
    def is_input_output_memory_management_unit_enabled(self, is_input_output_memory_management_unit_enabled):
        """
        Sets the is_input_output_memory_management_unit_enabled of this IntelIcelakeBmPlatformConfig.
        Whether the input-output memory management unit is enabled.


        :param is_input_output_memory_management_unit_enabled: The is_input_output_memory_management_unit_enabled of this IntelIcelakeBmPlatformConfig.
        :type: bool
        """
        self._is_input_output_memory_management_unit_enabled = is_input_output_memory_management_unit_enabled

    @property
    def percentage_of_cores_enabled(self):
        """
        Gets the percentage_of_cores_enabled of this IntelIcelakeBmPlatformConfig.
        The percentage of cores enabled. Value must be a multiple of 25%. If the requested percentage
        results in a fractional number of cores, the system rounds up the number of cores across processors
        and provisions an instance with a whole number of cores.

        If the applications that you run on the instance use a core-based licensing model and need fewer cores
        than the full size of the shape, you can disable cores to reduce your licensing costs. The instance
        itself is billed for the full shape, regardless of whether all cores are enabled.


        :return: The percentage_of_cores_enabled of this IntelIcelakeBmPlatformConfig.
        :rtype: int
        """
        return self._percentage_of_cores_enabled

    @percentage_of_cores_enabled.setter
    def percentage_of_cores_enabled(self, percentage_of_cores_enabled):
        """
        Sets the percentage_of_cores_enabled of this IntelIcelakeBmPlatformConfig.
        The percentage of cores enabled. Value must be a multiple of 25%. If the requested percentage
        results in a fractional number of cores, the system rounds up the number of cores across processors
        and provisions an instance with a whole number of cores.

        If the applications that you run on the instance use a core-based licensing model and need fewer cores
        than the full size of the shape, you can disable cores to reduce your licensing costs. The instance
        itself is billed for the full shape, regardless of whether all cores are enabled.


        :param percentage_of_cores_enabled: The percentage_of_cores_enabled of this IntelIcelakeBmPlatformConfig.
        :type: int
        """
        self._percentage_of_cores_enabled = percentage_of_cores_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
