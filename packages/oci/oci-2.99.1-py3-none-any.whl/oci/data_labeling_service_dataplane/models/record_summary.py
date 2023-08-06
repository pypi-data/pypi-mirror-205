# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RecordSummary(object):
    """
    A record summary is the representation returned in list views.  It is usually a subset of the full record entity and should not contain any potentially sensitive information.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RecordSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this RecordSummary.
        :type id: str

        :param name:
            The value to assign to the name property of this RecordSummary.
        :type name: str

        :param time_created:
            The value to assign to the time_created property of this RecordSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this RecordSummary.
        :type time_updated: datetime

        :param dataset_id:
            The value to assign to the dataset_id property of this RecordSummary.
        :type dataset_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this RecordSummary.
        :type compartment_id: str

        :param is_labeled:
            The value to assign to the is_labeled property of this RecordSummary.
        :type is_labeled: bool

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this RecordSummary.
        :type lifecycle_state: str

        :param record_metadata:
            The value to assign to the record_metadata property of this RecordSummary.
        :type record_metadata: oci.data_labeling_service_dataplane.models.RecordMetadata

        :param freeform_tags:
            The value to assign to the freeform_tags property of this RecordSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this RecordSummary.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'dataset_id': 'str',
            'compartment_id': 'str',
            'is_labeled': 'bool',
            'lifecycle_state': 'str',
            'record_metadata': 'RecordMetadata',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'dataset_id': 'datasetId',
            'compartment_id': 'compartmentId',
            'is_labeled': 'isLabeled',
            'lifecycle_state': 'lifecycleState',
            'record_metadata': 'recordMetadata',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._name = None
        self._time_created = None
        self._time_updated = None
        self._dataset_id = None
        self._compartment_id = None
        self._is_labeled = None
        self._lifecycle_state = None
        self._record_metadata = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this RecordSummary.
        The OCID of the record.


        :return: The id of this RecordSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this RecordSummary.
        The OCID of the record.


        :param id: The id of this RecordSummary.
        :type: str
        """
        self._id = id

    @property
    def name(self):
        """
        **[Required]** Gets the name of this RecordSummary.
        The name is automatically assigned by the service. It is unique and immutable


        :return: The name of this RecordSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this RecordSummary.
        The name is automatically assigned by the service. It is unique and immutable


        :param name: The name of this RecordSummary.
        :type: str
        """
        self._name = name

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this RecordSummary.
        The date and time the resource was created, in the timestamp format defined by RFC3339.


        :return: The time_created of this RecordSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this RecordSummary.
        The date and time the resource was created, in the timestamp format defined by RFC3339.


        :param time_created: The time_created of this RecordSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this RecordSummary.
        The date and time the resource was updated, in the timestamp format defined by RFC3339.


        :return: The time_updated of this RecordSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this RecordSummary.
        The date and time the resource was updated, in the timestamp format defined by RFC3339.


        :param time_updated: The time_updated of this RecordSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def dataset_id(self):
        """
        **[Required]** Gets the dataset_id of this RecordSummary.
        The OCID of the dataset to associate the record with.


        :return: The dataset_id of this RecordSummary.
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """
        Sets the dataset_id of this RecordSummary.
        The OCID of the dataset to associate the record with.


        :param dataset_id: The dataset_id of this RecordSummary.
        :type: str
        """
        self._dataset_id = dataset_id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this RecordSummary.
        The OCID of the compartment for the task.


        :return: The compartment_id of this RecordSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this RecordSummary.
        The OCID of the compartment for the task.


        :param compartment_id: The compartment_id of this RecordSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def is_labeled(self):
        """
        **[Required]** Gets the is_labeled of this RecordSummary.
        Whether or not the record has been labeled and has associated annotations.


        :return: The is_labeled of this RecordSummary.
        :rtype: bool
        """
        return self._is_labeled

    @is_labeled.setter
    def is_labeled(self, is_labeled):
        """
        Sets the is_labeled of this RecordSummary.
        Whether or not the record has been labeled and has associated annotations.


        :param is_labeled: The is_labeled of this RecordSummary.
        :type: bool
        """
        self._is_labeled = is_labeled

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this RecordSummary.
        Describes the lifecycle state.


        :return: The lifecycle_state of this RecordSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this RecordSummary.
        Describes the lifecycle state.


        :param lifecycle_state: The lifecycle_state of this RecordSummary.
        :type: str
        """
        self._lifecycle_state = lifecycle_state

    @property
    def record_metadata(self):
        """
        Gets the record_metadata of this RecordSummary.

        :return: The record_metadata of this RecordSummary.
        :rtype: oci.data_labeling_service_dataplane.models.RecordMetadata
        """
        return self._record_metadata

    @record_metadata.setter
    def record_metadata(self, record_metadata):
        """
        Sets the record_metadata of this RecordSummary.

        :param record_metadata: The record_metadata of this RecordSummary.
        :type: oci.data_labeling_service_dataplane.models.RecordMetadata
        """
        self._record_metadata = record_metadata

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this RecordSummary.
        A simple key-value pair that is applied without any predefined name, type, or scope. It exists for cross-compatibility only.
        For example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this RecordSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this RecordSummary.
        A simple key-value pair that is applied without any predefined name, type, or scope. It exists for cross-compatibility only.
        For example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this RecordSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this RecordSummary.
        The defined tags for this resource. Each key is predefined and scoped to a namespace.
        For example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this RecordSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this RecordSummary.
        The defined tags for this resource. Each key is predefined and scoped to a namespace.
        For example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this RecordSummary.
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
