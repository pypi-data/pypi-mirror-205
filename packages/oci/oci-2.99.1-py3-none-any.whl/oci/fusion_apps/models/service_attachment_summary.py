# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ServiceAttachmentSummary(object):
    """
    Summary of the ServiceInstance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ServiceAttachmentSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ServiceAttachmentSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ServiceAttachmentSummary.
        :type display_name: str

        :param service_instance_type:
            The value to assign to the service_instance_type property of this ServiceAttachmentSummary.
        :type service_instance_type: str

        :param service_instance_id:
            The value to assign to the service_instance_id property of this ServiceAttachmentSummary.
        :type service_instance_id: str

        :param service_url:
            The value to assign to the service_url property of this ServiceAttachmentSummary.
        :type service_url: str

        :param time_created:
            The value to assign to the time_created property of this ServiceAttachmentSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ServiceAttachmentSummary.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ServiceAttachmentSummary.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ServiceAttachmentSummary.
        :type lifecycle_details: str

        :param is_sku_based:
            The value to assign to the is_sku_based property of this ServiceAttachmentSummary.
        :type is_sku_based: bool

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ServiceAttachmentSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this ServiceAttachmentSummary.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'service_instance_type': 'str',
            'service_instance_id': 'str',
            'service_url': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'is_sku_based': 'bool',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'service_instance_type': 'serviceInstanceType',
            'service_instance_id': 'serviceInstanceId',
            'service_url': 'serviceUrl',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'is_sku_based': 'isSkuBased',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._display_name = None
        self._service_instance_type = None
        self._service_instance_id = None
        self._service_url = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._is_sku_based = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ServiceAttachmentSummary.
        Unique identifier that is immutable on creation


        :return: The id of this ServiceAttachmentSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ServiceAttachmentSummary.
        Unique identifier that is immutable on creation


        :param id: The id of this ServiceAttachmentSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ServiceAttachmentSummary.
        ServiceInstance Identifier, can be renamed


        :return: The display_name of this ServiceAttachmentSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ServiceAttachmentSummary.
        ServiceInstance Identifier, can be renamed


        :param display_name: The display_name of this ServiceAttachmentSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def service_instance_type(self):
        """
        **[Required]** Gets the service_instance_type of this ServiceAttachmentSummary.
        Type of the service.


        :return: The service_instance_type of this ServiceAttachmentSummary.
        :rtype: str
        """
        return self._service_instance_type

    @service_instance_type.setter
    def service_instance_type(self, service_instance_type):
        """
        Sets the service_instance_type of this ServiceAttachmentSummary.
        Type of the service.


        :param service_instance_type: The service_instance_type of this ServiceAttachmentSummary.
        :type: str
        """
        self._service_instance_type = service_instance_type

    @property
    def service_instance_id(self):
        """
        Gets the service_instance_id of this ServiceAttachmentSummary.
        The ID of the service instance created that can be used to identify this on the service control plane


        :return: The service_instance_id of this ServiceAttachmentSummary.
        :rtype: str
        """
        return self._service_instance_id

    @service_instance_id.setter
    def service_instance_id(self, service_instance_id):
        """
        Sets the service_instance_id of this ServiceAttachmentSummary.
        The ID of the service instance created that can be used to identify this on the service control plane


        :param service_instance_id: The service_instance_id of this ServiceAttachmentSummary.
        :type: str
        """
        self._service_instance_id = service_instance_id

    @property
    def service_url(self):
        """
        Gets the service_url of this ServiceAttachmentSummary.
        Service URL of the instance


        :return: The service_url of this ServiceAttachmentSummary.
        :rtype: str
        """
        return self._service_url

    @service_url.setter
    def service_url(self, service_url):
        """
        Sets the service_url of this ServiceAttachmentSummary.
        Service URL of the instance


        :param service_url: The service_url of this ServiceAttachmentSummary.
        :type: str
        """
        self._service_url = service_url

    @property
    def time_created(self):
        """
        Gets the time_created of this ServiceAttachmentSummary.
        The time the service instance was created. An RFC3339 formatted datetime string


        :return: The time_created of this ServiceAttachmentSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ServiceAttachmentSummary.
        The time the service instance was created. An RFC3339 formatted datetime string


        :param time_created: The time_created of this ServiceAttachmentSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this ServiceAttachmentSummary.
        The time the serivce instance was updated. An RFC3339 formatted datetime string


        :return: The time_updated of this ServiceAttachmentSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ServiceAttachmentSummary.
        The time the serivce instance was updated. An RFC3339 formatted datetime string


        :param time_updated: The time_updated of this ServiceAttachmentSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ServiceAttachmentSummary.
        The current state of the ServiceInstance.


        :return: The lifecycle_state of this ServiceAttachmentSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ServiceAttachmentSummary.
        The current state of the ServiceInstance.


        :param lifecycle_state: The lifecycle_state of this ServiceAttachmentSummary.
        :type: str
        """
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ServiceAttachmentSummary.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :return: The lifecycle_details of this ServiceAttachmentSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ServiceAttachmentSummary.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :param lifecycle_details: The lifecycle_details of this ServiceAttachmentSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def is_sku_based(self):
        """
        **[Required]** Gets the is_sku_based of this ServiceAttachmentSummary.
        Whether this service is provisioned due to the customer being subscribed to a specific SKU


        :return: The is_sku_based of this ServiceAttachmentSummary.
        :rtype: bool
        """
        return self._is_sku_based

    @is_sku_based.setter
    def is_sku_based(self, is_sku_based):
        """
        Sets the is_sku_based of this ServiceAttachmentSummary.
        Whether this service is provisioned due to the customer being subscribed to a specific SKU


        :param is_sku_based: The is_sku_based of this ServiceAttachmentSummary.
        :type: bool
        """
        self._is_sku_based = is_sku_based

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this ServiceAttachmentSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this ServiceAttachmentSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this ServiceAttachmentSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this ServiceAttachmentSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this ServiceAttachmentSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this ServiceAttachmentSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this ServiceAttachmentSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this ServiceAttachmentSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
