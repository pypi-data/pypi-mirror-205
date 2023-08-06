# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .dr_plan_user_defined_step import DrPlanUserDefinedStep
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RunObjectStoreScriptUserDefinedStep(DrPlanUserDefinedStep):
    """
    Run Object Store Script step details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RunObjectStoreScriptUserDefinedStep object with values from keyword arguments. The default value of the :py:attr:`~oci.disaster_recovery.models.RunObjectStoreScriptUserDefinedStep.step_type` attribute
        of this class is ``RUN_OBJECTSTORE_SCRIPT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param step_type:
            The value to assign to the step_type property of this RunObjectStoreScriptUserDefinedStep.
            Allowed values for this property are: "RUN_OBJECTSTORE_SCRIPT_PRECHECK", "RUN_LOCAL_SCRIPT_PRECHECK", "INVOKE_FUNCTION_PRECHECK", "RUN_OBJECTSTORE_SCRIPT", "RUN_LOCAL_SCRIPT", "INVOKE_FUNCTION"
        :type step_type: str

        :param run_on_instance_id:
            The value to assign to the run_on_instance_id property of this RunObjectStoreScriptUserDefinedStep.
        :type run_on_instance_id: str

        :param run_on_instance_region:
            The value to assign to the run_on_instance_region property of this RunObjectStoreScriptUserDefinedStep.
        :type run_on_instance_region: str

        :param object_storage_script_location:
            The value to assign to the object_storage_script_location property of this RunObjectStoreScriptUserDefinedStep.
        :type object_storage_script_location: oci.disaster_recovery.models.ObjectStorageScriptLocation

        """
        self.swagger_types = {
            'step_type': 'str',
            'run_on_instance_id': 'str',
            'run_on_instance_region': 'str',
            'object_storage_script_location': 'ObjectStorageScriptLocation'
        }

        self.attribute_map = {
            'step_type': 'stepType',
            'run_on_instance_id': 'runOnInstanceId',
            'run_on_instance_region': 'runOnInstanceRegion',
            'object_storage_script_location': 'objectStorageScriptLocation'
        }

        self._step_type = None
        self._run_on_instance_id = None
        self._run_on_instance_region = None
        self._object_storage_script_location = None
        self._step_type = 'RUN_OBJECTSTORE_SCRIPT'

    @property
    def run_on_instance_id(self):
        """
        Gets the run_on_instance_id of this RunObjectStoreScriptUserDefinedStep.
        The OCID of the instance where this script or command should be executed.

        Example: `ocid1.instance.oc1.phx.exampleocid1`


        :return: The run_on_instance_id of this RunObjectStoreScriptUserDefinedStep.
        :rtype: str
        """
        return self._run_on_instance_id

    @run_on_instance_id.setter
    def run_on_instance_id(self, run_on_instance_id):
        """
        Sets the run_on_instance_id of this RunObjectStoreScriptUserDefinedStep.
        The OCID of the instance where this script or command should be executed.

        Example: `ocid1.instance.oc1.phx.exampleocid1`


        :param run_on_instance_id: The run_on_instance_id of this RunObjectStoreScriptUserDefinedStep.
        :type: str
        """
        self._run_on_instance_id = run_on_instance_id

    @property
    def run_on_instance_region(self):
        """
        Gets the run_on_instance_region of this RunObjectStoreScriptUserDefinedStep.
        The region of the instance where this script or command should be executed.

        Example: `us-phoenix-1`


        :return: The run_on_instance_region of this RunObjectStoreScriptUserDefinedStep.
        :rtype: str
        """
        return self._run_on_instance_region

    @run_on_instance_region.setter
    def run_on_instance_region(self, run_on_instance_region):
        """
        Sets the run_on_instance_region of this RunObjectStoreScriptUserDefinedStep.
        The region of the instance where this script or command should be executed.

        Example: `us-phoenix-1`


        :param run_on_instance_region: The run_on_instance_region of this RunObjectStoreScriptUserDefinedStep.
        :type: str
        """
        self._run_on_instance_region = run_on_instance_region

    @property
    def object_storage_script_location(self):
        """
        Gets the object_storage_script_location of this RunObjectStoreScriptUserDefinedStep.

        :return: The object_storage_script_location of this RunObjectStoreScriptUserDefinedStep.
        :rtype: oci.disaster_recovery.models.ObjectStorageScriptLocation
        """
        return self._object_storage_script_location

    @object_storage_script_location.setter
    def object_storage_script_location(self, object_storage_script_location):
        """
        Sets the object_storage_script_location of this RunObjectStoreScriptUserDefinedStep.

        :param object_storage_script_location: The object_storage_script_location of this RunObjectStoreScriptUserDefinedStep.
        :type: oci.disaster_recovery.models.ObjectStorageScriptLocation
        """
        self._object_storage_script_location = object_storage_script_location

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
