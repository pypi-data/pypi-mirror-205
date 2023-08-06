# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateMediaWorkflowJobDetails(object):
    """
    Information to run the MediaWorkflow.
    """

    #: A constant which can be used with the workflow_identifier_type property of a CreateMediaWorkflowJobDetails.
    #: This constant has a value of "ID"
    WORKFLOW_IDENTIFIER_TYPE_ID = "ID"

    #: A constant which can be used with the workflow_identifier_type property of a CreateMediaWorkflowJobDetails.
    #: This constant has a value of "NAME"
    WORKFLOW_IDENTIFIER_TYPE_NAME = "NAME"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateMediaWorkflowJobDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.media_services.models.CreateMediaWorkflowJobByNameDetails`
        * :class:`~oci.media_services.models.CreateMediaWorkflowJobByIdDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param workflow_identifier_type:
            The value to assign to the workflow_identifier_type property of this CreateMediaWorkflowJobDetails.
            Allowed values for this property are: "ID", "NAME"
        :type workflow_identifier_type: str

        :param media_workflow_configuration_ids:
            The value to assign to the media_workflow_configuration_ids property of this CreateMediaWorkflowJobDetails.
        :type media_workflow_configuration_ids: list[str]

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateMediaWorkflowJobDetails.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateMediaWorkflowJobDetails.
        :type display_name: str

        :param parameters:
            The value to assign to the parameters property of this CreateMediaWorkflowJobDetails.
        :type parameters: dict(str, object)

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateMediaWorkflowJobDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateMediaWorkflowJobDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'workflow_identifier_type': 'str',
            'media_workflow_configuration_ids': 'list[str]',
            'compartment_id': 'str',
            'display_name': 'str',
            'parameters': 'dict(str, object)',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'workflow_identifier_type': 'workflowIdentifierType',
            'media_workflow_configuration_ids': 'mediaWorkflowConfigurationIds',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'parameters': 'parameters',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._workflow_identifier_type = None
        self._media_workflow_configuration_ids = None
        self._compartment_id = None
        self._display_name = None
        self._parameters = None
        self._freeform_tags = None
        self._defined_tags = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['workflowIdentifierType']

        if type == 'NAME':
            return 'CreateMediaWorkflowJobByNameDetails'

        if type == 'ID':
            return 'CreateMediaWorkflowJobByIdDetails'
        else:
            return 'CreateMediaWorkflowJobDetails'

    @property
    def workflow_identifier_type(self):
        """
        **[Required]** Gets the workflow_identifier_type of this CreateMediaWorkflowJobDetails.
        Discriminate identification of a workflow by name versus a workflow by ID.

        Allowed values for this property are: "ID", "NAME"


        :return: The workflow_identifier_type of this CreateMediaWorkflowJobDetails.
        :rtype: str
        """
        return self._workflow_identifier_type

    @workflow_identifier_type.setter
    def workflow_identifier_type(self, workflow_identifier_type):
        """
        Sets the workflow_identifier_type of this CreateMediaWorkflowJobDetails.
        Discriminate identification of a workflow by name versus a workflow by ID.


        :param workflow_identifier_type: The workflow_identifier_type of this CreateMediaWorkflowJobDetails.
        :type: str
        """
        allowed_values = ["ID", "NAME"]
        if not value_allowed_none_or_none_sentinel(workflow_identifier_type, allowed_values):
            raise ValueError(
                "Invalid value for `workflow_identifier_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._workflow_identifier_type = workflow_identifier_type

    @property
    def media_workflow_configuration_ids(self):
        """
        Gets the media_workflow_configuration_ids of this CreateMediaWorkflowJobDetails.
        Configurations to be applied to this run of the workflow.


        :return: The media_workflow_configuration_ids of this CreateMediaWorkflowJobDetails.
        :rtype: list[str]
        """
        return self._media_workflow_configuration_ids

    @media_workflow_configuration_ids.setter
    def media_workflow_configuration_ids(self, media_workflow_configuration_ids):
        """
        Sets the media_workflow_configuration_ids of this CreateMediaWorkflowJobDetails.
        Configurations to be applied to this run of the workflow.


        :param media_workflow_configuration_ids: The media_workflow_configuration_ids of this CreateMediaWorkflowJobDetails.
        :type: list[str]
        """
        self._media_workflow_configuration_ids = media_workflow_configuration_ids

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateMediaWorkflowJobDetails.
        ID of the compartment in which the job should be created.


        :return: The compartment_id of this CreateMediaWorkflowJobDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateMediaWorkflowJobDetails.
        ID of the compartment in which the job should be created.


        :param compartment_id: The compartment_id of this CreateMediaWorkflowJobDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateMediaWorkflowJobDetails.
        Name of the Media Workflow Job. Does not have to be unique. Avoid entering confidential information.


        :return: The display_name of this CreateMediaWorkflowJobDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateMediaWorkflowJobDetails.
        Name of the Media Workflow Job. Does not have to be unique. Avoid entering confidential information.


        :param display_name: The display_name of this CreateMediaWorkflowJobDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def parameters(self):
        """
        Gets the parameters of this CreateMediaWorkflowJobDetails.
        Parameters that override parameters specified in MediaWorkflowTaskDeclarations, the MediaWorkflow,
        the MediaWorkflow's MediaWorkflowConfigurations and the MediaWorkflowConfigurations of this
        MediaWorkflowJob. The parameters are given as JSON. The top level and 2nd level elements must be
        JSON objects (vs arrays, scalars, etc). The top level keys refer to a task's key and the 2nd level
        keys refer to a parameter's name.


        :return: The parameters of this CreateMediaWorkflowJobDetails.
        :rtype: dict(str, object)
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this CreateMediaWorkflowJobDetails.
        Parameters that override parameters specified in MediaWorkflowTaskDeclarations, the MediaWorkflow,
        the MediaWorkflow's MediaWorkflowConfigurations and the MediaWorkflowConfigurations of this
        MediaWorkflowJob. The parameters are given as JSON. The top level and 2nd level elements must be
        JSON objects (vs arrays, scalars, etc). The top level keys refer to a task's key and the 2nd level
        keys refer to a parameter's name.


        :param parameters: The parameters of this CreateMediaWorkflowJobDetails.
        :type: dict(str, object)
        """
        self._parameters = parameters

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateMediaWorkflowJobDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateMediaWorkflowJobDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateMediaWorkflowJobDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateMediaWorkflowJobDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateMediaWorkflowJobDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateMediaWorkflowJobDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateMediaWorkflowJobDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateMediaWorkflowJobDetails.
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
