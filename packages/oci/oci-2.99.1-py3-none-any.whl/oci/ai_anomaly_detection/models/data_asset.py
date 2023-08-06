# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DataAsset(object):
    """
    Description of DataAsset.
    """

    #: A constant which can be used with the lifecycle_state property of a DataAsset.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DataAsset.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    def __init__(self, **kwargs):
        """
        Initializes a new DataAsset object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DataAsset.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DataAsset.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this DataAsset.
        :type display_name: str

        :param description:
            The value to assign to the description property of this DataAsset.
        :type description: str

        :param time_created:
            The value to assign to the time_created property of this DataAsset.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this DataAsset.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DataAsset.
            Allowed values for this property are: "ACTIVE", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param project_id:
            The value to assign to the project_id property of this DataAsset.
        :type project_id: str

        :param data_source_details:
            The value to assign to the data_source_details property of this DataAsset.
        :type data_source_details: oci.ai_anomaly_detection.models.DataSourceDetails

        :param private_endpoint_id:
            The value to assign to the private_endpoint_id property of this DataAsset.
        :type private_endpoint_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DataAsset.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this DataAsset.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this DataAsset.
        :type system_tags: dict(str, object)

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'project_id': 'str',
            'data_source_details': 'DataSourceDetails',
            'private_endpoint_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, object)'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'project_id': 'projectId',
            'data_source_details': 'dataSourceDetails',
            'private_endpoint_id': 'privateEndpointId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._description = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._project_id = None
        self._data_source_details = None
        self._private_endpoint_id = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DataAsset.
        The Unique Oracle ID (OCID) that is immutable on creation.


        :return: The id of this DataAsset.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DataAsset.
        The Unique Oracle ID (OCID) that is immutable on creation.


        :param id: The id of this DataAsset.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DataAsset.
        The OCID of the compartment containing the DataAsset.


        :return: The compartment_id of this DataAsset.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DataAsset.
        The OCID of the compartment containing the DataAsset.


        :param compartment_id: The compartment_id of this DataAsset.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this DataAsset.
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.


        :return: The display_name of this DataAsset.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DataAsset.
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.


        :param display_name: The display_name of this DataAsset.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this DataAsset.
        A short description of the data asset.


        :return: The description of this DataAsset.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this DataAsset.
        A short description of the data asset.


        :param description: The description of this DataAsset.
        :type: str
        """
        self._description = description

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this DataAsset.
        The time the the DataAsset was created. An RFC3339 formatted datetime string


        :return: The time_created of this DataAsset.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this DataAsset.
        The time the the DataAsset was created. An RFC3339 formatted datetime string


        :param time_created: The time_created of this DataAsset.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this DataAsset.
        The time the the DataAsset was updated. An RFC3339 formatted datetime string


        :return: The time_updated of this DataAsset.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this DataAsset.
        The time the the DataAsset was updated. An RFC3339 formatted datetime string


        :param time_updated: The time_updated of this DataAsset.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this DataAsset.
        The lifecycle state of the Data Asset.

        Allowed values for this property are: "ACTIVE", "DELETED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this DataAsset.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DataAsset.
        The lifecycle state of the Data Asset.


        :param lifecycle_state: The lifecycle_state of this DataAsset.
        :type: str
        """
        allowed_values = ["ACTIVE", "DELETED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def project_id(self):
        """
        **[Required]** Gets the project_id of this DataAsset.
        The Unique project id which is created at project creation that is immutable on creation.


        :return: The project_id of this DataAsset.
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """
        Sets the project_id of this DataAsset.
        The Unique project id which is created at project creation that is immutable on creation.


        :param project_id: The project_id of this DataAsset.
        :type: str
        """
        self._project_id = project_id

    @property
    def data_source_details(self):
        """
        **[Required]** Gets the data_source_details of this DataAsset.

        :return: The data_source_details of this DataAsset.
        :rtype: oci.ai_anomaly_detection.models.DataSourceDetails
        """
        return self._data_source_details

    @data_source_details.setter
    def data_source_details(self, data_source_details):
        """
        Sets the data_source_details of this DataAsset.

        :param data_source_details: The data_source_details of this DataAsset.
        :type: oci.ai_anomaly_detection.models.DataSourceDetails
        """
        self._data_source_details = data_source_details

    @property
    def private_endpoint_id(self):
        """
        Gets the private_endpoint_id of this DataAsset.
        OCID of Private Endpoint.


        :return: The private_endpoint_id of this DataAsset.
        :rtype: str
        """
        return self._private_endpoint_id

    @private_endpoint_id.setter
    def private_endpoint_id(self, private_endpoint_id):
        """
        Sets the private_endpoint_id of this DataAsset.
        OCID of Private Endpoint.


        :param private_endpoint_id: The private_endpoint_id of this DataAsset.
        :type: str
        """
        self._private_endpoint_id = private_endpoint_id

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this DataAsset.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this DataAsset.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this DataAsset.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this DataAsset.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this DataAsset.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this DataAsset.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this DataAsset.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this DataAsset.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this DataAsset.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{ \"orcl-cloud\": { \"free-tier-retained\": \"true\" } }`


        :return: The system_tags of this DataAsset.
        :rtype: dict(str, object)
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this DataAsset.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{ \"orcl-cloud\": { \"free-tier-retained\": \"true\" } }`


        :param system_tags: The system_tags of this DataAsset.
        :type: dict(str, object)
        """
        self._system_tags = system_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
