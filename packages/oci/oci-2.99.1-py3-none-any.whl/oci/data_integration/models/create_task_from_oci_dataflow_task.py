# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_task_details import CreateTaskDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateTaskFromOCIDataflowTask(CreateTaskDetails):
    """
    The information about the OCI Dataflow task.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateTaskFromOCIDataflowTask object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.CreateTaskFromOCIDataflowTask.model_type` attribute
        of this class is ``OCI_DATAFLOW_TASK`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this CreateTaskFromOCIDataflowTask.
            Allowed values for this property are: "INTEGRATION_TASK", "DATA_LOADER_TASK", "PIPELINE_TASK", "SQL_TASK", "OCI_DATAFLOW_TASK", "REST_TASK"
        :type model_type: str

        :param key:
            The value to assign to the key property of this CreateTaskFromOCIDataflowTask.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this CreateTaskFromOCIDataflowTask.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this CreateTaskFromOCIDataflowTask.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param name:
            The value to assign to the name property of this CreateTaskFromOCIDataflowTask.
        :type name: str

        :param description:
            The value to assign to the description property of this CreateTaskFromOCIDataflowTask.
        :type description: str

        :param object_status:
            The value to assign to the object_status property of this CreateTaskFromOCIDataflowTask.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this CreateTaskFromOCIDataflowTask.
        :type identifier: str

        :param input_ports:
            The value to assign to the input_ports property of this CreateTaskFromOCIDataflowTask.
        :type input_ports: list[oci.data_integration.models.InputPort]

        :param output_ports:
            The value to assign to the output_ports property of this CreateTaskFromOCIDataflowTask.
        :type output_ports: list[oci.data_integration.models.OutputPort]

        :param parameters:
            The value to assign to the parameters property of this CreateTaskFromOCIDataflowTask.
        :type parameters: list[oci.data_integration.models.Parameter]

        :param op_config_values:
            The value to assign to the op_config_values property of this CreateTaskFromOCIDataflowTask.
        :type op_config_values: oci.data_integration.models.ConfigValues

        :param config_provider_delegate:
            The value to assign to the config_provider_delegate property of this CreateTaskFromOCIDataflowTask.
        :type config_provider_delegate: oci.data_integration.models.CreateConfigProvider

        :param registry_metadata:
            The value to assign to the registry_metadata property of this CreateTaskFromOCIDataflowTask.
        :type registry_metadata: oci.data_integration.models.RegistryMetadata

        :param dataflow_application:
            The value to assign to the dataflow_application property of this CreateTaskFromOCIDataflowTask.
        :type dataflow_application: oci.data_integration.models.DataflowApplication

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'description': 'str',
            'object_status': 'int',
            'identifier': 'str',
            'input_ports': 'list[InputPort]',
            'output_ports': 'list[OutputPort]',
            'parameters': 'list[Parameter]',
            'op_config_values': 'ConfigValues',
            'config_provider_delegate': 'CreateConfigProvider',
            'registry_metadata': 'RegistryMetadata',
            'dataflow_application': 'DataflowApplication'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'description': 'description',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'input_ports': 'inputPorts',
            'output_ports': 'outputPorts',
            'parameters': 'parameters',
            'op_config_values': 'opConfigValues',
            'config_provider_delegate': 'configProviderDelegate',
            'registry_metadata': 'registryMetadata',
            'dataflow_application': 'dataflowApplication'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._description = None
        self._object_status = None
        self._identifier = None
        self._input_ports = None
        self._output_ports = None
        self._parameters = None
        self._op_config_values = None
        self._config_provider_delegate = None
        self._registry_metadata = None
        self._dataflow_application = None
        self._model_type = 'OCI_DATAFLOW_TASK'

    @property
    def dataflow_application(self):
        """
        Gets the dataflow_application of this CreateTaskFromOCIDataflowTask.

        :return: The dataflow_application of this CreateTaskFromOCIDataflowTask.
        :rtype: oci.data_integration.models.DataflowApplication
        """
        return self._dataflow_application

    @dataflow_application.setter
    def dataflow_application(self, dataflow_application):
        """
        Sets the dataflow_application of this CreateTaskFromOCIDataflowTask.

        :param dataflow_application: The dataflow_application of this CreateTaskFromOCIDataflowTask.
        :type: oci.data_integration.models.DataflowApplication
        """
        self._dataflow_application = dataflow_application

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
