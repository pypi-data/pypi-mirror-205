# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class GenerateAgentDeployScriptDetails(object):
    """
    Attributes to generate agent deploy script for a Fleet.
    """

    #: A constant which can be used with the os_family property of a GenerateAgentDeployScriptDetails.
    #: This constant has a value of "LINUX"
    OS_FAMILY_LINUX = "LINUX"

    #: A constant which can be used with the os_family property of a GenerateAgentDeployScriptDetails.
    #: This constant has a value of "WINDOWS"
    OS_FAMILY_WINDOWS = "WINDOWS"

    #: A constant which can be used with the os_family property of a GenerateAgentDeployScriptDetails.
    #: This constant has a value of "MACOS"
    OS_FAMILY_MACOS = "MACOS"

    #: A constant which can be used with the os_family property of a GenerateAgentDeployScriptDetails.
    #: This constant has a value of "UNKNOWN"
    OS_FAMILY_UNKNOWN = "UNKNOWN"

    def __init__(self, **kwargs):
        """
        Initializes a new GenerateAgentDeployScriptDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param install_key_id:
            The value to assign to the install_key_id property of this GenerateAgentDeployScriptDetails.
        :type install_key_id: str

        :param os_family:
            The value to assign to the os_family property of this GenerateAgentDeployScriptDetails.
            Allowed values for this property are: "LINUX", "WINDOWS", "MACOS", "UNKNOWN"
        :type os_family: str

        :param is_user_name_enabled:
            The value to assign to the is_user_name_enabled property of this GenerateAgentDeployScriptDetails.
        :type is_user_name_enabled: bool

        """
        self.swagger_types = {
            'install_key_id': 'str',
            'os_family': 'str',
            'is_user_name_enabled': 'bool'
        }

        self.attribute_map = {
            'install_key_id': 'installKeyId',
            'os_family': 'osFamily',
            'is_user_name_enabled': 'isUserNameEnabled'
        }

        self._install_key_id = None
        self._os_family = None
        self._is_user_name_enabled = None

    @property
    def install_key_id(self):
        """
        **[Required]** Gets the install_key_id of this GenerateAgentDeployScriptDetails.
        The `OCID`__ of the install key for which to generate the script.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The install_key_id of this GenerateAgentDeployScriptDetails.
        :rtype: str
        """
        return self._install_key_id

    @install_key_id.setter
    def install_key_id(self, install_key_id):
        """
        Sets the install_key_id of this GenerateAgentDeployScriptDetails.
        The `OCID`__ of the install key for which to generate the script.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param install_key_id: The install_key_id of this GenerateAgentDeployScriptDetails.
        :type: str
        """
        self._install_key_id = install_key_id

    @property
    def os_family(self):
        """
        **[Required]** Gets the os_family of this GenerateAgentDeployScriptDetails.
        The operating system type for the script. Currently only 'LINUX' and 'WINDOWS' are supported.

        Allowed values for this property are: "LINUX", "WINDOWS", "MACOS", "UNKNOWN"


        :return: The os_family of this GenerateAgentDeployScriptDetails.
        :rtype: str
        """
        return self._os_family

    @os_family.setter
    def os_family(self, os_family):
        """
        Sets the os_family of this GenerateAgentDeployScriptDetails.
        The operating system type for the script. Currently only 'LINUX' and 'WINDOWS' are supported.


        :param os_family: The os_family of this GenerateAgentDeployScriptDetails.
        :type: str
        """
        allowed_values = ["LINUX", "WINDOWS", "MACOS", "UNKNOWN"]
        if not value_allowed_none_or_none_sentinel(os_family, allowed_values):
            raise ValueError(
                "Invalid value for `os_family`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._os_family = os_family

    @property
    def is_user_name_enabled(self):
        """
        **[Required]** Gets the is_user_name_enabled of this GenerateAgentDeployScriptDetails.
        Enable/disable user name collection on agent.


        :return: The is_user_name_enabled of this GenerateAgentDeployScriptDetails.
        :rtype: bool
        """
        return self._is_user_name_enabled

    @is_user_name_enabled.setter
    def is_user_name_enabled(self, is_user_name_enabled):
        """
        Sets the is_user_name_enabled of this GenerateAgentDeployScriptDetails.
        Enable/disable user name collection on agent.


        :param is_user_name_enabled: The is_user_name_enabled of this GenerateAgentDeployScriptDetails.
        :type: bool
        """
        self._is_user_name_enabled = is_user_name_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
