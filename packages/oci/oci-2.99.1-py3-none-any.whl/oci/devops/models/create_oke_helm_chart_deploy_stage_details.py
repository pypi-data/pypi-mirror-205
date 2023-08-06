# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_deploy_stage_details import CreateDeployStageDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateOkeHelmChartDeployStageDetails(CreateDeployStageDetails):
    """
    Specifies the Helm chart deployment to a Kubernetes cluster stage.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateOkeHelmChartDeployStageDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.devops.models.CreateOkeHelmChartDeployStageDetails.deploy_stage_type` attribute
        of this class is ``OKE_HELM_CHART_DEPLOYMENT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param description:
            The value to assign to the description property of this CreateOkeHelmChartDeployStageDetails.
        :type description: str

        :param display_name:
            The value to assign to the display_name property of this CreateOkeHelmChartDeployStageDetails.
        :type display_name: str

        :param deploy_stage_type:
            The value to assign to the deploy_stage_type property of this CreateOkeHelmChartDeployStageDetails.
        :type deploy_stage_type: str

        :param deploy_pipeline_id:
            The value to assign to the deploy_pipeline_id property of this CreateOkeHelmChartDeployStageDetails.
        :type deploy_pipeline_id: str

        :param deploy_stage_predecessor_collection:
            The value to assign to the deploy_stage_predecessor_collection property of this CreateOkeHelmChartDeployStageDetails.
        :type deploy_stage_predecessor_collection: oci.devops.models.DeployStagePredecessorCollection

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateOkeHelmChartDeployStageDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateOkeHelmChartDeployStageDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param oke_cluster_deploy_environment_id:
            The value to assign to the oke_cluster_deploy_environment_id property of this CreateOkeHelmChartDeployStageDetails.
        :type oke_cluster_deploy_environment_id: str

        :param helm_chart_deploy_artifact_id:
            The value to assign to the helm_chart_deploy_artifact_id property of this CreateOkeHelmChartDeployStageDetails.
        :type helm_chart_deploy_artifact_id: str

        :param values_artifact_ids:
            The value to assign to the values_artifact_ids property of this CreateOkeHelmChartDeployStageDetails.
        :type values_artifact_ids: list[str]

        :param release_name:
            The value to assign to the release_name property of this CreateOkeHelmChartDeployStageDetails.
        :type release_name: str

        :param namespace:
            The value to assign to the namespace property of this CreateOkeHelmChartDeployStageDetails.
        :type namespace: str

        :param timeout_in_seconds:
            The value to assign to the timeout_in_seconds property of this CreateOkeHelmChartDeployStageDetails.
        :type timeout_in_seconds: int

        :param rollback_policy:
            The value to assign to the rollback_policy property of this CreateOkeHelmChartDeployStageDetails.
        :type rollback_policy: oci.devops.models.DeployStageRollbackPolicy

        :param set_values:
            The value to assign to the set_values property of this CreateOkeHelmChartDeployStageDetails.
        :type set_values: oci.devops.models.HelmSetValueCollection

        :param set_string:
            The value to assign to the set_string property of this CreateOkeHelmChartDeployStageDetails.
        :type set_string: oci.devops.models.HelmSetValueCollection

        :param are_hooks_enabled:
            The value to assign to the are_hooks_enabled property of this CreateOkeHelmChartDeployStageDetails.
        :type are_hooks_enabled: bool

        :param should_reuse_values:
            The value to assign to the should_reuse_values property of this CreateOkeHelmChartDeployStageDetails.
        :type should_reuse_values: bool

        :param should_reset_values:
            The value to assign to the should_reset_values property of this CreateOkeHelmChartDeployStageDetails.
        :type should_reset_values: bool

        :param is_force_enabled:
            The value to assign to the is_force_enabled property of this CreateOkeHelmChartDeployStageDetails.
        :type is_force_enabled: bool

        :param should_cleanup_on_fail:
            The value to assign to the should_cleanup_on_fail property of this CreateOkeHelmChartDeployStageDetails.
        :type should_cleanup_on_fail: bool

        :param max_history:
            The value to assign to the max_history property of this CreateOkeHelmChartDeployStageDetails.
        :type max_history: int

        :param should_skip_crds:
            The value to assign to the should_skip_crds property of this CreateOkeHelmChartDeployStageDetails.
        :type should_skip_crds: bool

        :param should_skip_render_subchart_notes:
            The value to assign to the should_skip_render_subchart_notes property of this CreateOkeHelmChartDeployStageDetails.
        :type should_skip_render_subchart_notes: bool

        :param should_not_wait:
            The value to assign to the should_not_wait property of this CreateOkeHelmChartDeployStageDetails.
        :type should_not_wait: bool

        :param is_debug_enabled:
            The value to assign to the is_debug_enabled property of this CreateOkeHelmChartDeployStageDetails.
        :type is_debug_enabled: bool

        """
        self.swagger_types = {
            'description': 'str',
            'display_name': 'str',
            'deploy_stage_type': 'str',
            'deploy_pipeline_id': 'str',
            'deploy_stage_predecessor_collection': 'DeployStagePredecessorCollection',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'oke_cluster_deploy_environment_id': 'str',
            'helm_chart_deploy_artifact_id': 'str',
            'values_artifact_ids': 'list[str]',
            'release_name': 'str',
            'namespace': 'str',
            'timeout_in_seconds': 'int',
            'rollback_policy': 'DeployStageRollbackPolicy',
            'set_values': 'HelmSetValueCollection',
            'set_string': 'HelmSetValueCollection',
            'are_hooks_enabled': 'bool',
            'should_reuse_values': 'bool',
            'should_reset_values': 'bool',
            'is_force_enabled': 'bool',
            'should_cleanup_on_fail': 'bool',
            'max_history': 'int',
            'should_skip_crds': 'bool',
            'should_skip_render_subchart_notes': 'bool',
            'should_not_wait': 'bool',
            'is_debug_enabled': 'bool'
        }

        self.attribute_map = {
            'description': 'description',
            'display_name': 'displayName',
            'deploy_stage_type': 'deployStageType',
            'deploy_pipeline_id': 'deployPipelineId',
            'deploy_stage_predecessor_collection': 'deployStagePredecessorCollection',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'oke_cluster_deploy_environment_id': 'okeClusterDeployEnvironmentId',
            'helm_chart_deploy_artifact_id': 'helmChartDeployArtifactId',
            'values_artifact_ids': 'valuesArtifactIds',
            'release_name': 'releaseName',
            'namespace': 'namespace',
            'timeout_in_seconds': 'timeoutInSeconds',
            'rollback_policy': 'rollbackPolicy',
            'set_values': 'setValues',
            'set_string': 'setString',
            'are_hooks_enabled': 'areHooksEnabled',
            'should_reuse_values': 'shouldReuseValues',
            'should_reset_values': 'shouldResetValues',
            'is_force_enabled': 'isForceEnabled',
            'should_cleanup_on_fail': 'shouldCleanupOnFail',
            'max_history': 'maxHistory',
            'should_skip_crds': 'shouldSkipCrds',
            'should_skip_render_subchart_notes': 'shouldSkipRenderSubchartNotes',
            'should_not_wait': 'shouldNotWait',
            'is_debug_enabled': 'isDebugEnabled'
        }

        self._description = None
        self._display_name = None
        self._deploy_stage_type = None
        self._deploy_pipeline_id = None
        self._deploy_stage_predecessor_collection = None
        self._freeform_tags = None
        self._defined_tags = None
        self._oke_cluster_deploy_environment_id = None
        self._helm_chart_deploy_artifact_id = None
        self._values_artifact_ids = None
        self._release_name = None
        self._namespace = None
        self._timeout_in_seconds = None
        self._rollback_policy = None
        self._set_values = None
        self._set_string = None
        self._are_hooks_enabled = None
        self._should_reuse_values = None
        self._should_reset_values = None
        self._is_force_enabled = None
        self._should_cleanup_on_fail = None
        self._max_history = None
        self._should_skip_crds = None
        self._should_skip_render_subchart_notes = None
        self._should_not_wait = None
        self._is_debug_enabled = None
        self._deploy_stage_type = 'OKE_HELM_CHART_DEPLOYMENT'

    @property
    def oke_cluster_deploy_environment_id(self):
        """
        **[Required]** Gets the oke_cluster_deploy_environment_id of this CreateOkeHelmChartDeployStageDetails.
        Kubernetes cluster environment OCID for deployment.


        :return: The oke_cluster_deploy_environment_id of this CreateOkeHelmChartDeployStageDetails.
        :rtype: str
        """
        return self._oke_cluster_deploy_environment_id

    @oke_cluster_deploy_environment_id.setter
    def oke_cluster_deploy_environment_id(self, oke_cluster_deploy_environment_id):
        """
        Sets the oke_cluster_deploy_environment_id of this CreateOkeHelmChartDeployStageDetails.
        Kubernetes cluster environment OCID for deployment.


        :param oke_cluster_deploy_environment_id: The oke_cluster_deploy_environment_id of this CreateOkeHelmChartDeployStageDetails.
        :type: str
        """
        self._oke_cluster_deploy_environment_id = oke_cluster_deploy_environment_id

    @property
    def helm_chart_deploy_artifact_id(self):
        """
        **[Required]** Gets the helm_chart_deploy_artifact_id of this CreateOkeHelmChartDeployStageDetails.
        Helm chart artifact OCID.


        :return: The helm_chart_deploy_artifact_id of this CreateOkeHelmChartDeployStageDetails.
        :rtype: str
        """
        return self._helm_chart_deploy_artifact_id

    @helm_chart_deploy_artifact_id.setter
    def helm_chart_deploy_artifact_id(self, helm_chart_deploy_artifact_id):
        """
        Sets the helm_chart_deploy_artifact_id of this CreateOkeHelmChartDeployStageDetails.
        Helm chart artifact OCID.


        :param helm_chart_deploy_artifact_id: The helm_chart_deploy_artifact_id of this CreateOkeHelmChartDeployStageDetails.
        :type: str
        """
        self._helm_chart_deploy_artifact_id = helm_chart_deploy_artifact_id

    @property
    def values_artifact_ids(self):
        """
        Gets the values_artifact_ids of this CreateOkeHelmChartDeployStageDetails.
        List of values.yaml file artifact OCIDs.


        :return: The values_artifact_ids of this CreateOkeHelmChartDeployStageDetails.
        :rtype: list[str]
        """
        return self._values_artifact_ids

    @values_artifact_ids.setter
    def values_artifact_ids(self, values_artifact_ids):
        """
        Sets the values_artifact_ids of this CreateOkeHelmChartDeployStageDetails.
        List of values.yaml file artifact OCIDs.


        :param values_artifact_ids: The values_artifact_ids of this CreateOkeHelmChartDeployStageDetails.
        :type: list[str]
        """
        self._values_artifact_ids = values_artifact_ids

    @property
    def release_name(self):
        """
        **[Required]** Gets the release_name of this CreateOkeHelmChartDeployStageDetails.
        Default name of the chart instance. Must be unique within a Kubernetes namespace.


        :return: The release_name of this CreateOkeHelmChartDeployStageDetails.
        :rtype: str
        """
        return self._release_name

    @release_name.setter
    def release_name(self, release_name):
        """
        Sets the release_name of this CreateOkeHelmChartDeployStageDetails.
        Default name of the chart instance. Must be unique within a Kubernetes namespace.


        :param release_name: The release_name of this CreateOkeHelmChartDeployStageDetails.
        :type: str
        """
        self._release_name = release_name

    @property
    def namespace(self):
        """
        Gets the namespace of this CreateOkeHelmChartDeployStageDetails.
        Default namespace to be used for Kubernetes deployment when not specified in the manifest.


        :return: The namespace of this CreateOkeHelmChartDeployStageDetails.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """
        Sets the namespace of this CreateOkeHelmChartDeployStageDetails.
        Default namespace to be used for Kubernetes deployment when not specified in the manifest.


        :param namespace: The namespace of this CreateOkeHelmChartDeployStageDetails.
        :type: str
        """
        self._namespace = namespace

    @property
    def timeout_in_seconds(self):
        """
        Gets the timeout_in_seconds of this CreateOkeHelmChartDeployStageDetails.
        Time to wait for execution of a helm stage. Defaults to 300 seconds.


        :return: The timeout_in_seconds of this CreateOkeHelmChartDeployStageDetails.
        :rtype: int
        """
        return self._timeout_in_seconds

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, timeout_in_seconds):
        """
        Sets the timeout_in_seconds of this CreateOkeHelmChartDeployStageDetails.
        Time to wait for execution of a helm stage. Defaults to 300 seconds.


        :param timeout_in_seconds: The timeout_in_seconds of this CreateOkeHelmChartDeployStageDetails.
        :type: int
        """
        self._timeout_in_seconds = timeout_in_seconds

    @property
    def rollback_policy(self):
        """
        Gets the rollback_policy of this CreateOkeHelmChartDeployStageDetails.

        :return: The rollback_policy of this CreateOkeHelmChartDeployStageDetails.
        :rtype: oci.devops.models.DeployStageRollbackPolicy
        """
        return self._rollback_policy

    @rollback_policy.setter
    def rollback_policy(self, rollback_policy):
        """
        Sets the rollback_policy of this CreateOkeHelmChartDeployStageDetails.

        :param rollback_policy: The rollback_policy of this CreateOkeHelmChartDeployStageDetails.
        :type: oci.devops.models.DeployStageRollbackPolicy
        """
        self._rollback_policy = rollback_policy

    @property
    def set_values(self):
        """
        Gets the set_values of this CreateOkeHelmChartDeployStageDetails.

        :return: The set_values of this CreateOkeHelmChartDeployStageDetails.
        :rtype: oci.devops.models.HelmSetValueCollection
        """
        return self._set_values

    @set_values.setter
    def set_values(self, set_values):
        """
        Sets the set_values of this CreateOkeHelmChartDeployStageDetails.

        :param set_values: The set_values of this CreateOkeHelmChartDeployStageDetails.
        :type: oci.devops.models.HelmSetValueCollection
        """
        self._set_values = set_values

    @property
    def set_string(self):
        """
        Gets the set_string of this CreateOkeHelmChartDeployStageDetails.

        :return: The set_string of this CreateOkeHelmChartDeployStageDetails.
        :rtype: oci.devops.models.HelmSetValueCollection
        """
        return self._set_string

    @set_string.setter
    def set_string(self, set_string):
        """
        Sets the set_string of this CreateOkeHelmChartDeployStageDetails.

        :param set_string: The set_string of this CreateOkeHelmChartDeployStageDetails.
        :type: oci.devops.models.HelmSetValueCollection
        """
        self._set_string = set_string

    @property
    def are_hooks_enabled(self):
        """
        Gets the are_hooks_enabled of this CreateOkeHelmChartDeployStageDetails.
        Disable pre/post upgrade hooks. Set to false by default.


        :return: The are_hooks_enabled of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._are_hooks_enabled

    @are_hooks_enabled.setter
    def are_hooks_enabled(self, are_hooks_enabled):
        """
        Sets the are_hooks_enabled of this CreateOkeHelmChartDeployStageDetails.
        Disable pre/post upgrade hooks. Set to false by default.


        :param are_hooks_enabled: The are_hooks_enabled of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._are_hooks_enabled = are_hooks_enabled

    @property
    def should_reuse_values(self):
        """
        Gets the should_reuse_values of this CreateOkeHelmChartDeployStageDetails.
        During upgrade, reuse the values of the last release and merge overrides from the command line. Set to false by default.


        :return: The should_reuse_values of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._should_reuse_values

    @should_reuse_values.setter
    def should_reuse_values(self, should_reuse_values):
        """
        Sets the should_reuse_values of this CreateOkeHelmChartDeployStageDetails.
        During upgrade, reuse the values of the last release and merge overrides from the command line. Set to false by default.


        :param should_reuse_values: The should_reuse_values of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._should_reuse_values = should_reuse_values

    @property
    def should_reset_values(self):
        """
        Gets the should_reset_values of this CreateOkeHelmChartDeployStageDetails.
        During upgrade, reset the values to the ones built into the chart. It overrides shouldReuseValues. Set to false by default.


        :return: The should_reset_values of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._should_reset_values

    @should_reset_values.setter
    def should_reset_values(self, should_reset_values):
        """
        Sets the should_reset_values of this CreateOkeHelmChartDeployStageDetails.
        During upgrade, reset the values to the ones built into the chart. It overrides shouldReuseValues. Set to false by default.


        :param should_reset_values: The should_reset_values of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._should_reset_values = should_reset_values

    @property
    def is_force_enabled(self):
        """
        Gets the is_force_enabled of this CreateOkeHelmChartDeployStageDetails.
        Force resource update through delete; or if required, recreate. Set to false by default.


        :return: The is_force_enabled of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._is_force_enabled

    @is_force_enabled.setter
    def is_force_enabled(self, is_force_enabled):
        """
        Sets the is_force_enabled of this CreateOkeHelmChartDeployStageDetails.
        Force resource update through delete; or if required, recreate. Set to false by default.


        :param is_force_enabled: The is_force_enabled of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._is_force_enabled = is_force_enabled

    @property
    def should_cleanup_on_fail(self):
        """
        Gets the should_cleanup_on_fail of this CreateOkeHelmChartDeployStageDetails.
        Allow deletion of new resources created during when an upgrade fails. Set to false by default.


        :return: The should_cleanup_on_fail of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._should_cleanup_on_fail

    @should_cleanup_on_fail.setter
    def should_cleanup_on_fail(self, should_cleanup_on_fail):
        """
        Sets the should_cleanup_on_fail of this CreateOkeHelmChartDeployStageDetails.
        Allow deletion of new resources created during when an upgrade fails. Set to false by default.


        :param should_cleanup_on_fail: The should_cleanup_on_fail of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._should_cleanup_on_fail = should_cleanup_on_fail

    @property
    def max_history(self):
        """
        Gets the max_history of this CreateOkeHelmChartDeployStageDetails.
        Limit the maximum number of revisions saved per release. Use 0 for no limit. Set to 10 by default


        :return: The max_history of this CreateOkeHelmChartDeployStageDetails.
        :rtype: int
        """
        return self._max_history

    @max_history.setter
    def max_history(self, max_history):
        """
        Sets the max_history of this CreateOkeHelmChartDeployStageDetails.
        Limit the maximum number of revisions saved per release. Use 0 for no limit. Set to 10 by default


        :param max_history: The max_history of this CreateOkeHelmChartDeployStageDetails.
        :type: int
        """
        self._max_history = max_history

    @property
    def should_skip_crds(self):
        """
        Gets the should_skip_crds of this CreateOkeHelmChartDeployStageDetails.
        If set, no CRDs are installed. By default, CRDs are installed only if they are not present already. Set to false by default.


        :return: The should_skip_crds of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._should_skip_crds

    @should_skip_crds.setter
    def should_skip_crds(self, should_skip_crds):
        """
        Sets the should_skip_crds of this CreateOkeHelmChartDeployStageDetails.
        If set, no CRDs are installed. By default, CRDs are installed only if they are not present already. Set to false by default.


        :param should_skip_crds: The should_skip_crds of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._should_skip_crds = should_skip_crds

    @property
    def should_skip_render_subchart_notes(self):
        """
        Gets the should_skip_render_subchart_notes of this CreateOkeHelmChartDeployStageDetails.
        If set, renders subchart notes along with the parent. Set to false by default.


        :return: The should_skip_render_subchart_notes of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._should_skip_render_subchart_notes

    @should_skip_render_subchart_notes.setter
    def should_skip_render_subchart_notes(self, should_skip_render_subchart_notes):
        """
        Sets the should_skip_render_subchart_notes of this CreateOkeHelmChartDeployStageDetails.
        If set, renders subchart notes along with the parent. Set to false by default.


        :param should_skip_render_subchart_notes: The should_skip_render_subchart_notes of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._should_skip_render_subchart_notes = should_skip_render_subchart_notes

    @property
    def should_not_wait(self):
        """
        Gets the should_not_wait of this CreateOkeHelmChartDeployStageDetails.
        Does not wait until all the resources are in a ready state to mark the release as successful if set to true. Set to false by default.


        :return: The should_not_wait of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._should_not_wait

    @should_not_wait.setter
    def should_not_wait(self, should_not_wait):
        """
        Sets the should_not_wait of this CreateOkeHelmChartDeployStageDetails.
        Does not wait until all the resources are in a ready state to mark the release as successful if set to true. Set to false by default.


        :param should_not_wait: The should_not_wait of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._should_not_wait = should_not_wait

    @property
    def is_debug_enabled(self):
        """
        Gets the is_debug_enabled of this CreateOkeHelmChartDeployStageDetails.
        Enables helm --debug option to stream output to tf stdout. Set to false by default.


        :return: The is_debug_enabled of this CreateOkeHelmChartDeployStageDetails.
        :rtype: bool
        """
        return self._is_debug_enabled

    @is_debug_enabled.setter
    def is_debug_enabled(self, is_debug_enabled):
        """
        Sets the is_debug_enabled of this CreateOkeHelmChartDeployStageDetails.
        Enables helm --debug option to stream output to tf stdout. Set to false by default.


        :param is_debug_enabled: The is_debug_enabled of this CreateOkeHelmChartDeployStageDetails.
        :type: bool
        """
        self._is_debug_enabled = is_debug_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
