# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateDetectAnomalyJobDetails(object):
    """
    Base class for the DetectAnomalies async call. It contains the identifier that is
    used for deciding what type of request this is.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateDetectAnomalyJobDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateDetectAnomalyJobDetails.
        :type compartment_id: str

        :param description:
            The value to assign to the description property of this CreateDetectAnomalyJobDetails.
        :type description: str

        :param display_name:
            The value to assign to the display_name property of this CreateDetectAnomalyJobDetails.
        :type display_name: str

        :param model_id:
            The value to assign to the model_id property of this CreateDetectAnomalyJobDetails.
        :type model_id: str

        :param sensitivity:
            The value to assign to the sensitivity property of this CreateDetectAnomalyJobDetails.
        :type sensitivity: float

        :param are_all_estimates_required:
            The value to assign to the are_all_estimates_required property of this CreateDetectAnomalyJobDetails.
        :type are_all_estimates_required: bool

        :param input_details:
            The value to assign to the input_details property of this CreateDetectAnomalyJobDetails.
        :type input_details: oci.ai_anomaly_detection.models.InputDetails

        :param output_details:
            The value to assign to the output_details property of this CreateDetectAnomalyJobDetails.
        :type output_details: oci.ai_anomaly_detection.models.OutputDetails

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'description': 'str',
            'display_name': 'str',
            'model_id': 'str',
            'sensitivity': 'float',
            'are_all_estimates_required': 'bool',
            'input_details': 'InputDetails',
            'output_details': 'OutputDetails'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'description': 'description',
            'display_name': 'displayName',
            'model_id': 'modelId',
            'sensitivity': 'sensitivity',
            'are_all_estimates_required': 'areAllEstimatesRequired',
            'input_details': 'inputDetails',
            'output_details': 'outputDetails'
        }

        self._compartment_id = None
        self._description = None
        self._display_name = None
        self._model_id = None
        self._sensitivity = None
        self._are_all_estimates_required = None
        self._input_details = None
        self._output_details = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateDetectAnomalyJobDetails.
        The OCID of the compartment that starts the job.


        :return: The compartment_id of this CreateDetectAnomalyJobDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateDetectAnomalyJobDetails.
        The OCID of the compartment that starts the job.


        :param compartment_id: The compartment_id of this CreateDetectAnomalyJobDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def description(self):
        """
        Gets the description of this CreateDetectAnomalyJobDetails.
        A short description of the detect anomaly job.


        :return: The description of this CreateDetectAnomalyJobDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateDetectAnomalyJobDetails.
        A short description of the detect anomaly job.


        :param description: The description of this CreateDetectAnomalyJobDetails.
        :type: str
        """
        self._description = description

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateDetectAnomalyJobDetails.
        Detect anomaly job display name.


        :return: The display_name of this CreateDetectAnomalyJobDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateDetectAnomalyJobDetails.
        Detect anomaly job display name.


        :param display_name: The display_name of this CreateDetectAnomalyJobDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def model_id(self):
        """
        **[Required]** Gets the model_id of this CreateDetectAnomalyJobDetails.
        The OCID of the trained model.


        :return: The model_id of this CreateDetectAnomalyJobDetails.
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """
        Sets the model_id of this CreateDetectAnomalyJobDetails.
        The OCID of the trained model.


        :param model_id: The model_id of this CreateDetectAnomalyJobDetails.
        :type: str
        """
        self._model_id = model_id

    @property
    def sensitivity(self):
        """
        Gets the sensitivity of this CreateDetectAnomalyJobDetails.
        The value that customer can adjust to control the sensitivity of anomaly detection


        :return: The sensitivity of this CreateDetectAnomalyJobDetails.
        :rtype: float
        """
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, sensitivity):
        """
        Sets the sensitivity of this CreateDetectAnomalyJobDetails.
        The value that customer can adjust to control the sensitivity of anomaly detection


        :param sensitivity: The sensitivity of this CreateDetectAnomalyJobDetails.
        :type: float
        """
        self._sensitivity = sensitivity

    @property
    def are_all_estimates_required(self):
        """
        Gets the are_all_estimates_required of this CreateDetectAnomalyJobDetails.
        Flag to enable the service to return estimates for all data points rather than just the anomalous data points.


        :return: The are_all_estimates_required of this CreateDetectAnomalyJobDetails.
        :rtype: bool
        """
        return self._are_all_estimates_required

    @are_all_estimates_required.setter
    def are_all_estimates_required(self, are_all_estimates_required):
        """
        Sets the are_all_estimates_required of this CreateDetectAnomalyJobDetails.
        Flag to enable the service to return estimates for all data points rather than just the anomalous data points.


        :param are_all_estimates_required: The are_all_estimates_required of this CreateDetectAnomalyJobDetails.
        :type: bool
        """
        self._are_all_estimates_required = are_all_estimates_required

    @property
    def input_details(self):
        """
        **[Required]** Gets the input_details of this CreateDetectAnomalyJobDetails.

        :return: The input_details of this CreateDetectAnomalyJobDetails.
        :rtype: oci.ai_anomaly_detection.models.InputDetails
        """
        return self._input_details

    @input_details.setter
    def input_details(self, input_details):
        """
        Sets the input_details of this CreateDetectAnomalyJobDetails.

        :param input_details: The input_details of this CreateDetectAnomalyJobDetails.
        :type: oci.ai_anomaly_detection.models.InputDetails
        """
        self._input_details = input_details

    @property
    def output_details(self):
        """
        **[Required]** Gets the output_details of this CreateDetectAnomalyJobDetails.

        :return: The output_details of this CreateDetectAnomalyJobDetails.
        :rtype: oci.ai_anomaly_detection.models.OutputDetails
        """
        return self._output_details

    @output_details.setter
    def output_details(self, output_details):
        """
        Sets the output_details of this CreateDetectAnomalyJobDetails.

        :param output_details: The output_details of this CreateDetectAnomalyJobDetails.
        :type: oci.ai_anomaly_detection.models.OutputDetails
        """
        self._output_details = output_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
