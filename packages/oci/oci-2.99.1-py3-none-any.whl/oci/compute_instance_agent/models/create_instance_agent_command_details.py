# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateInstanceAgentCommandDetails(object):
    """
    Creation details for an Oracle Cloud Agent command.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateInstanceAgentCommandDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateInstanceAgentCommandDetails.
        :type compartment_id: str

        :param execution_time_out_in_seconds:
            The value to assign to the execution_time_out_in_seconds property of this CreateInstanceAgentCommandDetails.
        :type execution_time_out_in_seconds: int

        :param display_name:
            The value to assign to the display_name property of this CreateInstanceAgentCommandDetails.
        :type display_name: str

        :param target:
            The value to assign to the target property of this CreateInstanceAgentCommandDetails.
        :type target: oci.compute_instance_agent.models.InstanceAgentCommandTarget

        :param content:
            The value to assign to the content property of this CreateInstanceAgentCommandDetails.
        :type content: oci.compute_instance_agent.models.InstanceAgentCommandContent

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'execution_time_out_in_seconds': 'int',
            'display_name': 'str',
            'target': 'InstanceAgentCommandTarget',
            'content': 'InstanceAgentCommandContent'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'execution_time_out_in_seconds': 'executionTimeOutInSeconds',
            'display_name': 'displayName',
            'target': 'target',
            'content': 'content'
        }

        self._compartment_id = None
        self._execution_time_out_in_seconds = None
        self._display_name = None
        self._target = None
        self._content = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateInstanceAgentCommandDetails.
        The `OCID`__ of the compartment to create the command in.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateInstanceAgentCommandDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateInstanceAgentCommandDetails.
        The `OCID`__ of the compartment to create the command in.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateInstanceAgentCommandDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def execution_time_out_in_seconds(self):
        """
        **[Required]** Gets the execution_time_out_in_seconds of this CreateInstanceAgentCommandDetails.
        The amount of time that Oracle Cloud Agent is given to run the command on the instance before timing
        out. The timer starts when Oracle Cloud Agent starts the command. Zero means no timeout.


        :return: The execution_time_out_in_seconds of this CreateInstanceAgentCommandDetails.
        :rtype: int
        """
        return self._execution_time_out_in_seconds

    @execution_time_out_in_seconds.setter
    def execution_time_out_in_seconds(self, execution_time_out_in_seconds):
        """
        Sets the execution_time_out_in_seconds of this CreateInstanceAgentCommandDetails.
        The amount of time that Oracle Cloud Agent is given to run the command on the instance before timing
        out. The timer starts when Oracle Cloud Agent starts the command. Zero means no timeout.


        :param execution_time_out_in_seconds: The execution_time_out_in_seconds of this CreateInstanceAgentCommandDetails.
        :type: int
        """
        self._execution_time_out_in_seconds = execution_time_out_in_seconds

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateInstanceAgentCommandDetails.
        A user-friendly name for the command. It does not have to be unique.
        Avoid entering confidential information.

        Example: `Database Backup Script`


        :return: The display_name of this CreateInstanceAgentCommandDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateInstanceAgentCommandDetails.
        A user-friendly name for the command. It does not have to be unique.
        Avoid entering confidential information.

        Example: `Database Backup Script`


        :param display_name: The display_name of this CreateInstanceAgentCommandDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def target(self):
        """
        **[Required]** Gets the target of this CreateInstanceAgentCommandDetails.
        The target instance to run the command on.


        :return: The target of this CreateInstanceAgentCommandDetails.
        :rtype: oci.compute_instance_agent.models.InstanceAgentCommandTarget
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        Sets the target of this CreateInstanceAgentCommandDetails.
        The target instance to run the command on.


        :param target: The target of this CreateInstanceAgentCommandDetails.
        :type: oci.compute_instance_agent.models.InstanceAgentCommandTarget
        """
        self._target = target

    @property
    def content(self):
        """
        **[Required]** Gets the content of this CreateInstanceAgentCommandDetails.
        The contents of the command.


        :return: The content of this CreateInstanceAgentCommandDetails.
        :rtype: oci.compute_instance_agent.models.InstanceAgentCommandContent
        """
        return self._content

    @content.setter
    def content(self, content):
        """
        Sets the content of this CreateInstanceAgentCommandDetails.
        The contents of the command.


        :param content: The content of this CreateInstanceAgentCommandDetails.
        :type: oci.compute_instance_agent.models.InstanceAgentCommandContent
        """
        self._content = content

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
