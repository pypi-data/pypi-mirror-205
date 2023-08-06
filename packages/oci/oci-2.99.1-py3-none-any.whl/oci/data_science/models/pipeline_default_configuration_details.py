# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .pipeline_configuration_details import PipelineConfigurationDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PipelineDefaultConfigurationDetails(PipelineConfigurationDetails):
    """
    The default pipeline configuration.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PipelineDefaultConfigurationDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.data_science.models.PipelineDefaultConfigurationDetails.type` attribute
        of this class is ``DEFAULT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this PipelineDefaultConfigurationDetails.
            Allowed values for this property are: "DEFAULT"
        :type type: str

        :param maximum_runtime_in_minutes:
            The value to assign to the maximum_runtime_in_minutes property of this PipelineDefaultConfigurationDetails.
        :type maximum_runtime_in_minutes: int

        :param environment_variables:
            The value to assign to the environment_variables property of this PipelineDefaultConfigurationDetails.
        :type environment_variables: dict(str, str)

        :param command_line_arguments:
            The value to assign to the command_line_arguments property of this PipelineDefaultConfigurationDetails.
        :type command_line_arguments: str

        """
        self.swagger_types = {
            'type': 'str',
            'maximum_runtime_in_minutes': 'int',
            'environment_variables': 'dict(str, str)',
            'command_line_arguments': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'maximum_runtime_in_minutes': 'maximumRuntimeInMinutes',
            'environment_variables': 'environmentVariables',
            'command_line_arguments': 'commandLineArguments'
        }

        self._type = None
        self._maximum_runtime_in_minutes = None
        self._environment_variables = None
        self._command_line_arguments = None
        self._type = 'DEFAULT'

    @property
    def maximum_runtime_in_minutes(self):
        """
        Gets the maximum_runtime_in_minutes of this PipelineDefaultConfigurationDetails.
        A time bound for the execution of the entire Pipeline. Timer starts when the Pipeline Run is in progress.


        :return: The maximum_runtime_in_minutes of this PipelineDefaultConfigurationDetails.
        :rtype: int
        """
        return self._maximum_runtime_in_minutes

    @maximum_runtime_in_minutes.setter
    def maximum_runtime_in_minutes(self, maximum_runtime_in_minutes):
        """
        Sets the maximum_runtime_in_minutes of this PipelineDefaultConfigurationDetails.
        A time bound for the execution of the entire Pipeline. Timer starts when the Pipeline Run is in progress.


        :param maximum_runtime_in_minutes: The maximum_runtime_in_minutes of this PipelineDefaultConfigurationDetails.
        :type: int
        """
        self._maximum_runtime_in_minutes = maximum_runtime_in_minutes

    @property
    def environment_variables(self):
        """
        Gets the environment_variables of this PipelineDefaultConfigurationDetails.
        Environment variables to set for steps in the pipeline.


        :return: The environment_variables of this PipelineDefaultConfigurationDetails.
        :rtype: dict(str, str)
        """
        return self._environment_variables

    @environment_variables.setter
    def environment_variables(self, environment_variables):
        """
        Sets the environment_variables of this PipelineDefaultConfigurationDetails.
        Environment variables to set for steps in the pipeline.


        :param environment_variables: The environment_variables of this PipelineDefaultConfigurationDetails.
        :type: dict(str, str)
        """
        self._environment_variables = environment_variables

    @property
    def command_line_arguments(self):
        """
        Gets the command_line_arguments of this PipelineDefaultConfigurationDetails.
        The command line arguments to set for steps in the pipeline.


        :return: The command_line_arguments of this PipelineDefaultConfigurationDetails.
        :rtype: str
        """
        return self._command_line_arguments

    @command_line_arguments.setter
    def command_line_arguments(self, command_line_arguments):
        """
        Sets the command_line_arguments of this PipelineDefaultConfigurationDetails.
        The command line arguments to set for steps in the pipeline.


        :param command_line_arguments: The command_line_arguments of this PipelineDefaultConfigurationDetails.
        :type: str
        """
        self._command_line_arguments = command_line_arguments

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
