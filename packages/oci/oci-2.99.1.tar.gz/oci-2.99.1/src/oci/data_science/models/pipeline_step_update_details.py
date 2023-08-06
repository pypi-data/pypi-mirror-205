# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PipelineStepUpdateDetails(object):
    """
    The details of the step to update.
    """

    #: A constant which can be used with the step_type property of a PipelineStepUpdateDetails.
    #: This constant has a value of "ML_JOB"
    STEP_TYPE_ML_JOB = "ML_JOB"

    #: A constant which can be used with the step_type property of a PipelineStepUpdateDetails.
    #: This constant has a value of "CUSTOM_SCRIPT"
    STEP_TYPE_CUSTOM_SCRIPT = "CUSTOM_SCRIPT"

    def __init__(self, **kwargs):
        """
        Initializes a new PipelineStepUpdateDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.data_science.models.PipelineMLJobStepUpdateDetails`
        * :class:`~oci.data_science.models.PipelineCustomScriptStepUpdateDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param step_type:
            The value to assign to the step_type property of this PipelineStepUpdateDetails.
            Allowed values for this property are: "ML_JOB", "CUSTOM_SCRIPT"
        :type step_type: str

        :param step_name:
            The value to assign to the step_name property of this PipelineStepUpdateDetails.
        :type step_name: str

        :param description:
            The value to assign to the description property of this PipelineStepUpdateDetails.
        :type description: str

        :param step_configuration_details:
            The value to assign to the step_configuration_details property of this PipelineStepUpdateDetails.
        :type step_configuration_details: oci.data_science.models.PipelineStepConfigurationDetails

        """
        self.swagger_types = {
            'step_type': 'str',
            'step_name': 'str',
            'description': 'str',
            'step_configuration_details': 'PipelineStepConfigurationDetails'
        }

        self.attribute_map = {
            'step_type': 'stepType',
            'step_name': 'stepName',
            'description': 'description',
            'step_configuration_details': 'stepConfigurationDetails'
        }

        self._step_type = None
        self._step_name = None
        self._description = None
        self._step_configuration_details = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['stepType']

        if type == 'ML_JOB':
            return 'PipelineMLJobStepUpdateDetails'

        if type == 'CUSTOM_SCRIPT':
            return 'PipelineCustomScriptStepUpdateDetails'
        else:
            return 'PipelineStepUpdateDetails'

    @property
    def step_type(self):
        """
        **[Required]** Gets the step_type of this PipelineStepUpdateDetails.
        The type of step.

        Allowed values for this property are: "ML_JOB", "CUSTOM_SCRIPT"


        :return: The step_type of this PipelineStepUpdateDetails.
        :rtype: str
        """
        return self._step_type

    @step_type.setter
    def step_type(self, step_type):
        """
        Sets the step_type of this PipelineStepUpdateDetails.
        The type of step.


        :param step_type: The step_type of this PipelineStepUpdateDetails.
        :type: str
        """
        allowed_values = ["ML_JOB", "CUSTOM_SCRIPT"]
        if not value_allowed_none_or_none_sentinel(step_type, allowed_values):
            raise ValueError(
                "Invalid value for `step_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._step_type = step_type

    @property
    def step_name(self):
        """
        **[Required]** Gets the step_name of this PipelineStepUpdateDetails.
        The name of the step.


        :return: The step_name of this PipelineStepUpdateDetails.
        :rtype: str
        """
        return self._step_name

    @step_name.setter
    def step_name(self, step_name):
        """
        Sets the step_name of this PipelineStepUpdateDetails.
        The name of the step.


        :param step_name: The step_name of this PipelineStepUpdateDetails.
        :type: str
        """
        self._step_name = step_name

    @property
    def description(self):
        """
        Gets the description of this PipelineStepUpdateDetails.
        A short description of the step.


        :return: The description of this PipelineStepUpdateDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PipelineStepUpdateDetails.
        A short description of the step.


        :param description: The description of this PipelineStepUpdateDetails.
        :type: str
        """
        self._description = description

    @property
    def step_configuration_details(self):
        """
        Gets the step_configuration_details of this PipelineStepUpdateDetails.

        :return: The step_configuration_details of this PipelineStepUpdateDetails.
        :rtype: oci.data_science.models.PipelineStepConfigurationDetails
        """
        return self._step_configuration_details

    @step_configuration_details.setter
    def step_configuration_details(self, step_configuration_details):
        """
        Sets the step_configuration_details of this PipelineStepUpdateDetails.

        :param step_configuration_details: The step_configuration_details of this PipelineStepUpdateDetails.
        :type: oci.data_science.models.PipelineStepConfigurationDetails
        """
        self._step_configuration_details = step_configuration_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
