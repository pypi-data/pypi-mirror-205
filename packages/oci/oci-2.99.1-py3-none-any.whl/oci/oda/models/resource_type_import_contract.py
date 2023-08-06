# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourceTypeImportContract(object):
    """
    The contract guiding the import experience for the consumer and behavior of the resource provider for a single resourceType.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ResourceTypeImportContract object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param resource_type:
            The value to assign to the resource_type property of this ResourceTypeImportContract.
        :type resource_type: str

        :param parameters:
            The value to assign to the parameters property of this ResourceTypeImportContract.
        :type parameters: list[oci.oda.models.ParameterDefinition]

        """
        self.swagger_types = {
            'resource_type': 'str',
            'parameters': 'list[ParameterDefinition]'
        }

        self.attribute_map = {
            'resource_type': 'resourceType',
            'parameters': 'parameters'
        }

        self._resource_type = None
        self._parameters = None

    @property
    def resource_type(self):
        """
        **[Required]** Gets the resource_type of this ResourceTypeImportContract.
        The type of resource to which this resourceType-specific contract applies


        :return: The resource_type of this ResourceTypeImportContract.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """
        Sets the resource_type of this ResourceTypeImportContract.
        The type of resource to which this resourceType-specific contract applies


        :param resource_type: The resource_type of this ResourceTypeImportContract.
        :type: str
        """
        self._resource_type = resource_type

    @property
    def parameters(self):
        """
        **[Required]** Gets the parameters of this ResourceTypeImportContract.
        A list of definitions for parameters that are required to import this package into a target instance.


        :return: The parameters of this ResourceTypeImportContract.
        :rtype: list[oci.oda.models.ParameterDefinition]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this ResourceTypeImportContract.
        A list of definitions for parameters that are required to import this package into a target instance.


        :param parameters: The parameters of this ResourceTypeImportContract.
        :type: list[oci.oda.models.ParameterDefinition]
        """
        self._parameters = parameters

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
