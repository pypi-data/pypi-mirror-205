# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class OpensearchClusterSummary(object):
    """
    The summary of information about an OpenSearch cluster.
    """

    #: A constant which can be used with the security_mode property of a OpensearchClusterSummary.
    #: This constant has a value of "DISABLED"
    SECURITY_MODE_DISABLED = "DISABLED"

    #: A constant which can be used with the security_mode property of a OpensearchClusterSummary.
    #: This constant has a value of "PERMISSIVE"
    SECURITY_MODE_PERMISSIVE = "PERMISSIVE"

    #: A constant which can be used with the security_mode property of a OpensearchClusterSummary.
    #: This constant has a value of "ENFORCING"
    SECURITY_MODE_ENFORCING = "ENFORCING"

    def __init__(self, **kwargs):
        """
        Initializes a new OpensearchClusterSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this OpensearchClusterSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this OpensearchClusterSummary.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this OpensearchClusterSummary.
        :type compartment_id: str

        :param time_created:
            The value to assign to the time_created property of this OpensearchClusterSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this OpensearchClusterSummary.
        :type time_updated: datetime

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this OpensearchClusterSummary.
        :type lifecycle_details: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this OpensearchClusterSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this OpensearchClusterSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this OpensearchClusterSummary.
        :type system_tags: dict(str, dict(str, object))

        :param software_version:
            The value to assign to the software_version property of this OpensearchClusterSummary.
        :type software_version: str

        :param total_storage_gb:
            The value to assign to the total_storage_gb property of this OpensearchClusterSummary.
        :type total_storage_gb: int

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this OpensearchClusterSummary.
        :type lifecycle_state: str

        :param availability_domains:
            The value to assign to the availability_domains property of this OpensearchClusterSummary.
        :type availability_domains: list[str]

        :param security_mode:
            The value to assign to the security_mode property of this OpensearchClusterSummary.
            Allowed values for this property are: "DISABLED", "PERMISSIVE", "ENFORCING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type security_mode: str

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_details': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'software_version': 'str',
            'total_storage_gb': 'int',
            'lifecycle_state': 'str',
            'availability_domains': 'list[str]',
            'security_mode': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_details': 'lifecycleDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'software_version': 'softwareVersion',
            'total_storage_gb': 'totalStorageGB',
            'lifecycle_state': 'lifecycleState',
            'availability_domains': 'availabilityDomains',
            'security_mode': 'securityMode'
        }

        self._id = None
        self._display_name = None
        self._compartment_id = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._software_version = None
        self._total_storage_gb = None
        self._lifecycle_state = None
        self._availability_domains = None
        self._security_mode = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this OpensearchClusterSummary.
        The OCID of the cluster.


        :return: The id of this OpensearchClusterSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this OpensearchClusterSummary.
        The OCID of the cluster.


        :param id: The id of this OpensearchClusterSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        Gets the display_name of this OpensearchClusterSummary.
        The name of the cluster. Avoid entering confidential information.


        :return: The display_name of this OpensearchClusterSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this OpensearchClusterSummary.
        The name of the cluster. Avoid entering confidential information.


        :param display_name: The display_name of this OpensearchClusterSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this OpensearchClusterSummary.
        The OCID for the compartment where the cluster is located.


        :return: The compartment_id of this OpensearchClusterSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this OpensearchClusterSummary.
        The OCID for the compartment where the cluster is located.


        :param compartment_id: The compartment_id of this OpensearchClusterSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def time_created(self):
        """
        Gets the time_created of this OpensearchClusterSummary.
        The date and time the cluster was created. Format defined
        by `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this OpensearchClusterSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this OpensearchClusterSummary.
        The date and time the cluster was created. Format defined
        by `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this OpensearchClusterSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this OpensearchClusterSummary.
        The date and time the cluster was updated. Format defined
        by `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_updated of this OpensearchClusterSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this OpensearchClusterSummary.
        The date and time the cluster was updated. Format defined
        by `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :param time_updated: The time_updated of this OpensearchClusterSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this OpensearchClusterSummary.
        Additional information about the current lifecycle state of the cluster.


        :return: The lifecycle_details of this OpensearchClusterSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this OpensearchClusterSummary.
        Additional information about the current lifecycle state of the cluster.


        :param lifecycle_details: The lifecycle_details of this OpensearchClusterSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this OpensearchClusterSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this OpensearchClusterSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this OpensearchClusterSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this OpensearchClusterSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this OpensearchClusterSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this OpensearchClusterSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this OpensearchClusterSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this OpensearchClusterSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this OpensearchClusterSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this OpensearchClusterSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this OpensearchClusterSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this OpensearchClusterSummary.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    @property
    def software_version(self):
        """
        **[Required]** Gets the software_version of this OpensearchClusterSummary.
        The software version the cluster is running.


        :return: The software_version of this OpensearchClusterSummary.
        :rtype: str
        """
        return self._software_version

    @software_version.setter
    def software_version(self, software_version):
        """
        Sets the software_version of this OpensearchClusterSummary.
        The software version the cluster is running.


        :param software_version: The software_version of this OpensearchClusterSummary.
        :type: str
        """
        self._software_version = software_version

    @property
    def total_storage_gb(self):
        """
        **[Required]** Gets the total_storage_gb of this OpensearchClusterSummary.
        The total amount of storage in GB, for the cluster.


        :return: The total_storage_gb of this OpensearchClusterSummary.
        :rtype: int
        """
        return self._total_storage_gb

    @total_storage_gb.setter
    def total_storage_gb(self, total_storage_gb):
        """
        Sets the total_storage_gb of this OpensearchClusterSummary.
        The total amount of storage in GB, for the cluster.


        :param total_storage_gb: The total_storage_gb of this OpensearchClusterSummary.
        :type: int
        """
        self._total_storage_gb = total_storage_gb

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this OpensearchClusterSummary.
        The current state of the cluster.


        :return: The lifecycle_state of this OpensearchClusterSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this OpensearchClusterSummary.
        The current state of the cluster.


        :param lifecycle_state: The lifecycle_state of this OpensearchClusterSummary.
        :type: str
        """
        self._lifecycle_state = lifecycle_state

    @property
    def availability_domains(self):
        """
        Gets the availability_domains of this OpensearchClusterSummary.
        The availability domains to distribute the cluser nodes across.


        :return: The availability_domains of this OpensearchClusterSummary.
        :rtype: list[str]
        """
        return self._availability_domains

    @availability_domains.setter
    def availability_domains(self, availability_domains):
        """
        Sets the availability_domains of this OpensearchClusterSummary.
        The availability domains to distribute the cluser nodes across.


        :param availability_domains: The availability_domains of this OpensearchClusterSummary.
        :type: list[str]
        """
        self._availability_domains = availability_domains

    @property
    def security_mode(self):
        """
        Gets the security_mode of this OpensearchClusterSummary.
        The security mode of the cluster.

        Allowed values for this property are: "DISABLED", "PERMISSIVE", "ENFORCING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The security_mode of this OpensearchClusterSummary.
        :rtype: str
        """
        return self._security_mode

    @security_mode.setter
    def security_mode(self, security_mode):
        """
        Sets the security_mode of this OpensearchClusterSummary.
        The security mode of the cluster.


        :param security_mode: The security_mode of this OpensearchClusterSummary.
        :type: str
        """
        allowed_values = ["DISABLED", "PERMISSIVE", "ENFORCING"]
        if not value_allowed_none_or_none_sentinel(security_mode, allowed_values):
            security_mode = 'UNKNOWN_ENUM_VALUE'
        self._security_mode = security_mode

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
