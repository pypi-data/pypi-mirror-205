# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateExternalDbSystemDetails(object):
    """
    The details required to create an external DB system.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateExternalDbSystemDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this CreateExternalDbSystemDetails.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateExternalDbSystemDetails.
        :type compartment_id: str

        :param db_system_discovery_id:
            The value to assign to the db_system_discovery_id property of this CreateExternalDbSystemDetails.
        :type db_system_discovery_id: str

        :param database_management_config:
            The value to assign to the database_management_config property of this CreateExternalDbSystemDetails.
        :type database_management_config: oci.database_management.models.ExternalDbSystemDatabaseManagementConfigDetails

        """
        self.swagger_types = {
            'display_name': 'str',
            'compartment_id': 'str',
            'db_system_discovery_id': 'str',
            'database_management_config': 'ExternalDbSystemDatabaseManagementConfigDetails'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'db_system_discovery_id': 'dbSystemDiscoveryId',
            'database_management_config': 'databaseManagementConfig'
        }

        self._display_name = None
        self._compartment_id = None
        self._db_system_discovery_id = None
        self._database_management_config = None

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateExternalDbSystemDetails.
        The user-friendly name for the DB system. The name does not have to be unique.


        :return: The display_name of this CreateExternalDbSystemDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateExternalDbSystemDetails.
        The user-friendly name for the DB system. The name does not have to be unique.


        :param display_name: The display_name of this CreateExternalDbSystemDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateExternalDbSystemDetails.
        The `OCID`__ of the compartment in which the external DB system resides.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateExternalDbSystemDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateExternalDbSystemDetails.
        The `OCID`__ of the compartment in which the external DB system resides.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateExternalDbSystemDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def db_system_discovery_id(self):
        """
        **[Required]** Gets the db_system_discovery_id of this CreateExternalDbSystemDetails.
        The `OCID`__ of the DB system discovery.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The db_system_discovery_id of this CreateExternalDbSystemDetails.
        :rtype: str
        """
        return self._db_system_discovery_id

    @db_system_discovery_id.setter
    def db_system_discovery_id(self, db_system_discovery_id):
        """
        Sets the db_system_discovery_id of this CreateExternalDbSystemDetails.
        The `OCID`__ of the DB system discovery.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param db_system_discovery_id: The db_system_discovery_id of this CreateExternalDbSystemDetails.
        :type: str
        """
        self._db_system_discovery_id = db_system_discovery_id

    @property
    def database_management_config(self):
        """
        Gets the database_management_config of this CreateExternalDbSystemDetails.

        :return: The database_management_config of this CreateExternalDbSystemDetails.
        :rtype: oci.database_management.models.ExternalDbSystemDatabaseManagementConfigDetails
        """
        return self._database_management_config

    @database_management_config.setter
    def database_management_config(self, database_management_config):
        """
        Sets the database_management_config of this CreateExternalDbSystemDetails.

        :param database_management_config: The database_management_config of this CreateExternalDbSystemDetails.
        :type: oci.database_management.models.ExternalDbSystemDatabaseManagementConfigDetails
        """
        self._database_management_config = database_management_config

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
