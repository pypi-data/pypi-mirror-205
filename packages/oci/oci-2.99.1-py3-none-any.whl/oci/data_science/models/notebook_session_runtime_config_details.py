# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class NotebookSessionRuntimeConfigDetails(object):
    """
    Notebook Session runtime configuration details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new NotebookSessionRuntimeConfigDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param custom_environment_variables:
            The value to assign to the custom_environment_variables property of this NotebookSessionRuntimeConfigDetails.
        :type custom_environment_variables: dict(str, str)

        :param notebook_session_git_config_details:
            The value to assign to the notebook_session_git_config_details property of this NotebookSessionRuntimeConfigDetails.
        :type notebook_session_git_config_details: oci.data_science.models.NotebookSessionGitConfigDetails

        """
        self.swagger_types = {
            'custom_environment_variables': 'dict(str, str)',
            'notebook_session_git_config_details': 'NotebookSessionGitConfigDetails'
        }

        self.attribute_map = {
            'custom_environment_variables': 'customEnvironmentVariables',
            'notebook_session_git_config_details': 'notebookSessionGitConfigDetails'
        }

        self._custom_environment_variables = None
        self._notebook_session_git_config_details = None

    @property
    def custom_environment_variables(self):
        """
        Gets the custom_environment_variables of this NotebookSessionRuntimeConfigDetails.
        Custom environment variables for Notebook Session. These key-value pairs will be available for customers in Notebook Sessions.


        :return: The custom_environment_variables of this NotebookSessionRuntimeConfigDetails.
        :rtype: dict(str, str)
        """
        return self._custom_environment_variables

    @custom_environment_variables.setter
    def custom_environment_variables(self, custom_environment_variables):
        """
        Sets the custom_environment_variables of this NotebookSessionRuntimeConfigDetails.
        Custom environment variables for Notebook Session. These key-value pairs will be available for customers in Notebook Sessions.


        :param custom_environment_variables: The custom_environment_variables of this NotebookSessionRuntimeConfigDetails.
        :type: dict(str, str)
        """
        self._custom_environment_variables = custom_environment_variables

    @property
    def notebook_session_git_config_details(self):
        """
        Gets the notebook_session_git_config_details of this NotebookSessionRuntimeConfigDetails.

        :return: The notebook_session_git_config_details of this NotebookSessionRuntimeConfigDetails.
        :rtype: oci.data_science.models.NotebookSessionGitConfigDetails
        """
        return self._notebook_session_git_config_details

    @notebook_session_git_config_details.setter
    def notebook_session_git_config_details(self, notebook_session_git_config_details):
        """
        Sets the notebook_session_git_config_details of this NotebookSessionRuntimeConfigDetails.

        :param notebook_session_git_config_details: The notebook_session_git_config_details of this NotebookSessionRuntimeConfigDetails.
        :type: oci.data_science.models.NotebookSessionGitConfigDetails
        """
        self._notebook_session_git_config_details = notebook_session_git_config_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
