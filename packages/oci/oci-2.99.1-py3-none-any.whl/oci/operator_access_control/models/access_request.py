# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AccessRequest(object):
    """
    An Oracle operator raises access request when they need access to any infrastructure resource governed by Operator Access Control.
    The access request identifies the target resource and the set of operator actions. Access request handling depends upon the Operator Control
    that governs the target resource, and the set of operator actions listed for approval in the access request. If all of the operator actions
    listed in the access request are in the pre-approved list in the Operator Control that governs the target resource, then the access request is
    automatically approved. If not, then the access request requires explicit approval from the approver group specified by the Operator Control governing the target resource.

    You can approve or reject an access request. You can also revoke the approval of an already approved access request. While creating an access request,
    the operator specifies the duration of access. You have the option to approve the entire duration or reduce or even increase the time duration.
    An operator can also request for an extension. The approval for such an extension is processed the same way the original access request was processed.
    """

    #: A constant which can be used with the resource_type property of a AccessRequest.
    #: This constant has a value of "EXACC"
    RESOURCE_TYPE_EXACC = "EXACC"

    #: A constant which can be used with the resource_type property of a AccessRequest.
    #: This constant has a value of "EXADATAINFRASTRUCTURE"
    RESOURCE_TYPE_EXADATAINFRASTRUCTURE = "EXADATAINFRASTRUCTURE"

    #: A constant which can be used with the resource_type property of a AccessRequest.
    #: This constant has a value of "AUTONOMOUSVMCLUSTER"
    RESOURCE_TYPE_AUTONOMOUSVMCLUSTER = "AUTONOMOUSVMCLUSTER"

    #: A constant which can be used with the resource_type property of a AccessRequest.
    #: This constant has a value of "CLOUDAUTONOMOUSVMCLUSTER"
    RESOURCE_TYPE_CLOUDAUTONOMOUSVMCLUSTER = "CLOUDAUTONOMOUSVMCLUSTER"

    #: A constant which can be used with the severity property of a AccessRequest.
    #: This constant has a value of "S1"
    SEVERITY_S1 = "S1"

    #: A constant which can be used with the severity property of a AccessRequest.
    #: This constant has a value of "S2"
    SEVERITY_S2 = "S2"

    #: A constant which can be used with the severity property of a AccessRequest.
    #: This constant has a value of "S3"
    SEVERITY_S3 = "S3"

    #: A constant which can be used with the severity property of a AccessRequest.
    #: This constant has a value of "S4"
    SEVERITY_S4 = "S4"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "CREATED"
    LIFECYCLE_STATE_CREATED = "CREATED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "APPROVALWAITING"
    LIFECYCLE_STATE_APPROVALWAITING = "APPROVALWAITING"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "PREAPPROVED"
    LIFECYCLE_STATE_PREAPPROVED = "PREAPPROVED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "APPROVED"
    LIFECYCLE_STATE_APPROVED = "APPROVED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "MOREINFO"
    LIFECYCLE_STATE_MOREINFO = "MOREINFO"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "REJECTED"
    LIFECYCLE_STATE_REJECTED = "REJECTED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "DEPLOYED"
    LIFECYCLE_STATE_DEPLOYED = "DEPLOYED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "DEPLOYFAILED"
    LIFECYCLE_STATE_DEPLOYFAILED = "DEPLOYFAILED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "UNDEPLOYED"
    LIFECYCLE_STATE_UNDEPLOYED = "UNDEPLOYED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "UNDEPLOYFAILED"
    LIFECYCLE_STATE_UNDEPLOYFAILED = "UNDEPLOYFAILED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "CLOSEFAILED"
    LIFECYCLE_STATE_CLOSEFAILED = "CLOSEFAILED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "REVOKEFAILED"
    LIFECYCLE_STATE_REVOKEFAILED = "REVOKEFAILED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "EXPIRYFAILED"
    LIFECYCLE_STATE_EXPIRYFAILED = "EXPIRYFAILED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "REVOKING"
    LIFECYCLE_STATE_REVOKING = "REVOKING"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "REVOKED"
    LIFECYCLE_STATE_REVOKED = "REVOKED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "EXTENDING"
    LIFECYCLE_STATE_EXTENDING = "EXTENDING"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "EXTENDED"
    LIFECYCLE_STATE_EXTENDED = "EXTENDED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "EXTENSIONREJECTED"
    LIFECYCLE_STATE_EXTENSIONREJECTED = "EXTENSIONREJECTED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "COMPLETING"
    LIFECYCLE_STATE_COMPLETING = "COMPLETING"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "COMPLETED"
    LIFECYCLE_STATE_COMPLETED = "COMPLETED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "EXPIRED"
    LIFECYCLE_STATE_EXPIRED = "EXPIRED"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "APPROVEDFORFUTURE"
    LIFECYCLE_STATE_APPROVEDFORFUTURE = "APPROVEDFORFUTURE"

    #: A constant which can be used with the lifecycle_state property of a AccessRequest.
    #: This constant has a value of "INREVIEW"
    LIFECYCLE_STATE_INREVIEW = "INREVIEW"

    def __init__(self, **kwargs):
        """
        Initializes a new AccessRequest object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this AccessRequest.
        :type id: str

        :param request_id:
            The value to assign to the request_id property of this AccessRequest.
        :type request_id: str

        :param access_reason_summary:
            The value to assign to the access_reason_summary property of this AccessRequest.
        :type access_reason_summary: str

        :param operator_id:
            The value to assign to the operator_id property of this AccessRequest.
        :type operator_id: str

        :param resource_id:
            The value to assign to the resource_id property of this AccessRequest.
        :type resource_id: str

        :param resource_name:
            The value to assign to the resource_name property of this AccessRequest.
        :type resource_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this AccessRequest.
        :type compartment_id: str

        :param resource_type:
            The value to assign to the resource_type property of this AccessRequest.
            Allowed values for this property are: "EXACC", "EXADATAINFRASTRUCTURE", "AUTONOMOUSVMCLUSTER", "CLOUDAUTONOMOUSVMCLUSTER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type resource_type: str

        :param action_requests_list:
            The value to assign to the action_requests_list property of this AccessRequest.
        :type action_requests_list: list[str]

        :param reason:
            The value to assign to the reason property of this AccessRequest.
        :type reason: str

        :param severity:
            The value to assign to the severity property of this AccessRequest.
            Allowed values for this property are: "S1", "S2", "S3", "S4", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type severity: str

        :param duration:
            The value to assign to the duration property of this AccessRequest.
        :type duration: int

        :param extend_duration:
            The value to assign to the extend_duration property of this AccessRequest.
        :type extend_duration: int

        :param workflow_id:
            The value to assign to the workflow_id property of this AccessRequest.
        :type workflow_id: list[str]

        :param is_auto_approved:
            The value to assign to the is_auto_approved property of this AccessRequest.
        :type is_auto_approved: bool

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this AccessRequest.
            Allowed values for this property are: "CREATED", "APPROVALWAITING", "PREAPPROVED", "APPROVED", "MOREINFO", "REJECTED", "DEPLOYED", "DEPLOYFAILED", "UNDEPLOYED", "UNDEPLOYFAILED", "CLOSEFAILED", "REVOKEFAILED", "EXPIRYFAILED", "REVOKING", "REVOKED", "EXTENDING", "EXTENDED", "EXTENSIONREJECTED", "COMPLETING", "COMPLETED", "EXPIRED", "APPROVEDFORFUTURE", "INREVIEW", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this AccessRequest.
        :type lifecycle_details: str

        :param time_of_creation:
            The value to assign to the time_of_creation property of this AccessRequest.
        :type time_of_creation: datetime

        :param time_of_modification:
            The value to assign to the time_of_modification property of this AccessRequest.
        :type time_of_modification: datetime

        :param time_of_user_creation:
            The value to assign to the time_of_user_creation property of this AccessRequest.
        :type time_of_user_creation: datetime

        :param user_id:
            The value to assign to the user_id property of this AccessRequest.
        :type user_id: str

        :param approver_comment:
            The value to assign to the approver_comment property of this AccessRequest.
        :type approver_comment: str

        :param closure_comment:
            The value to assign to the closure_comment property of this AccessRequest.
        :type closure_comment: str

        :param opctl_id:
            The value to assign to the opctl_id property of this AccessRequest.
        :type opctl_id: str

        :param opctl_name:
            The value to assign to the opctl_name property of this AccessRequest.
        :type opctl_name: str

        :param system_message:
            The value to assign to the system_message property of this AccessRequest.
        :type system_message: str

        :param opctl_additional_message:
            The value to assign to the opctl_additional_message property of this AccessRequest.
        :type opctl_additional_message: str

        :param audit_type:
            The value to assign to the audit_type property of this AccessRequest.
        :type audit_type: list[str]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this AccessRequest.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this AccessRequest.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'request_id': 'str',
            'access_reason_summary': 'str',
            'operator_id': 'str',
            'resource_id': 'str',
            'resource_name': 'str',
            'compartment_id': 'str',
            'resource_type': 'str',
            'action_requests_list': 'list[str]',
            'reason': 'str',
            'severity': 'str',
            'duration': 'int',
            'extend_duration': 'int',
            'workflow_id': 'list[str]',
            'is_auto_approved': 'bool',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_of_creation': 'datetime',
            'time_of_modification': 'datetime',
            'time_of_user_creation': 'datetime',
            'user_id': 'str',
            'approver_comment': 'str',
            'closure_comment': 'str',
            'opctl_id': 'str',
            'opctl_name': 'str',
            'system_message': 'str',
            'opctl_additional_message': 'str',
            'audit_type': 'list[str]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'request_id': 'requestId',
            'access_reason_summary': 'accessReasonSummary',
            'operator_id': 'operatorId',
            'resource_id': 'resourceId',
            'resource_name': 'resourceName',
            'compartment_id': 'compartmentId',
            'resource_type': 'resourceType',
            'action_requests_list': 'actionRequestsList',
            'reason': 'reason',
            'severity': 'severity',
            'duration': 'duration',
            'extend_duration': 'extendDuration',
            'workflow_id': 'workflowId',
            'is_auto_approved': 'isAutoApproved',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_of_creation': 'timeOfCreation',
            'time_of_modification': 'timeOfModification',
            'time_of_user_creation': 'timeOfUserCreation',
            'user_id': 'userId',
            'approver_comment': 'approverComment',
            'closure_comment': 'closureComment',
            'opctl_id': 'opctlId',
            'opctl_name': 'opctlName',
            'system_message': 'systemMessage',
            'opctl_additional_message': 'opctlAdditionalMessage',
            'audit_type': 'auditType',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._request_id = None
        self._access_reason_summary = None
        self._operator_id = None
        self._resource_id = None
        self._resource_name = None
        self._compartment_id = None
        self._resource_type = None
        self._action_requests_list = None
        self._reason = None
        self._severity = None
        self._duration = None
        self._extend_duration = None
        self._workflow_id = None
        self._is_auto_approved = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_of_creation = None
        self._time_of_modification = None
        self._time_of_user_creation = None
        self._user_id = None
        self._approver_comment = None
        self._closure_comment = None
        self._opctl_id = None
        self._opctl_name = None
        self._system_message = None
        self._opctl_additional_message = None
        self._audit_type = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this AccessRequest.
        The OCID of the access request.


        :return: The id of this AccessRequest.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AccessRequest.
        The OCID of the access request.


        :param id: The id of this AccessRequest.
        :type: str
        """
        self._id = id

    @property
    def request_id(self):
        """
        Gets the request_id of this AccessRequest.
        This is an automatic identifier generated by the system which is easier for human comprehension.


        :return: The request_id of this AccessRequest.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this AccessRequest.
        This is an automatic identifier generated by the system which is easier for human comprehension.


        :param request_id: The request_id of this AccessRequest.
        :type: str
        """
        self._request_id = request_id

    @property
    def access_reason_summary(self):
        """
        **[Required]** Gets the access_reason_summary of this AccessRequest.
        Summary comment by the operator creating the access request.


        :return: The access_reason_summary of this AccessRequest.
        :rtype: str
        """
        return self._access_reason_summary

    @access_reason_summary.setter
    def access_reason_summary(self, access_reason_summary):
        """
        Sets the access_reason_summary of this AccessRequest.
        Summary comment by the operator creating the access request.


        :param access_reason_summary: The access_reason_summary of this AccessRequest.
        :type: str
        """
        self._access_reason_summary = access_reason_summary

    @property
    def operator_id(self):
        """
        Gets the operator_id of this AccessRequest.
        A unique identifier associated with the operator who raised the request. This identifier can not be used directly to identify the operator.
        You need to provide this identifier if you would like Oracle to provide additional information about the operator action within Oracle tenancy.


        :return: The operator_id of this AccessRequest.
        :rtype: str
        """
        return self._operator_id

    @operator_id.setter
    def operator_id(self, operator_id):
        """
        Sets the operator_id of this AccessRequest.
        A unique identifier associated with the operator who raised the request. This identifier can not be used directly to identify the operator.
        You need to provide this identifier if you would like Oracle to provide additional information about the operator action within Oracle tenancy.


        :param operator_id: The operator_id of this AccessRequest.
        :type: str
        """
        self._operator_id = operator_id

    @property
    def resource_id(self):
        """
        **[Required]** Gets the resource_id of this AccessRequest.
        The OCID of the target resource associated with the access request. The operator raises an access request to get approval to
        access the target resource.


        :return: The resource_id of this AccessRequest.
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """
        Sets the resource_id of this AccessRequest.
        The OCID of the target resource associated with the access request. The operator raises an access request to get approval to
        access the target resource.


        :param resource_id: The resource_id of this AccessRequest.
        :type: str
        """
        self._resource_id = resource_id

    @property
    def resource_name(self):
        """
        Gets the resource_name of this AccessRequest.
        The name of the target resource.


        :return: The resource_name of this AccessRequest.
        :rtype: str
        """
        return self._resource_name

    @resource_name.setter
    def resource_name(self, resource_name):
        """
        Sets the resource_name of this AccessRequest.
        The name of the target resource.


        :param resource_name: The resource_name of this AccessRequest.
        :type: str
        """
        self._resource_name = resource_name

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this AccessRequest.
        The OCID of the compartment that contains the access request.


        :return: The compartment_id of this AccessRequest.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this AccessRequest.
        The OCID of the compartment that contains the access request.


        :param compartment_id: The compartment_id of this AccessRequest.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def resource_type(self):
        """
        Gets the resource_type of this AccessRequest.
        resourceType for which the AccessRequest is applicable

        Allowed values for this property are: "EXACC", "EXADATAINFRASTRUCTURE", "AUTONOMOUSVMCLUSTER", "CLOUDAUTONOMOUSVMCLUSTER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The resource_type of this AccessRequest.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """
        Sets the resource_type of this AccessRequest.
        resourceType for which the AccessRequest is applicable


        :param resource_type: The resource_type of this AccessRequest.
        :type: str
        """
        allowed_values = ["EXACC", "EXADATAINFRASTRUCTURE", "AUTONOMOUSVMCLUSTER", "CLOUDAUTONOMOUSVMCLUSTER"]
        if not value_allowed_none_or_none_sentinel(resource_type, allowed_values):
            resource_type = 'UNKNOWN_ENUM_VALUE'
        self._resource_type = resource_type

    @property
    def action_requests_list(self):
        """
        Gets the action_requests_list of this AccessRequest.
        List of operator actions for which approval is sought by the operator user.


        :return: The action_requests_list of this AccessRequest.
        :rtype: list[str]
        """
        return self._action_requests_list

    @action_requests_list.setter
    def action_requests_list(self, action_requests_list):
        """
        Sets the action_requests_list of this AccessRequest.
        List of operator actions for which approval is sought by the operator user.


        :param action_requests_list: The action_requests_list of this AccessRequest.
        :type: list[str]
        """
        self._action_requests_list = action_requests_list

    @property
    def reason(self):
        """
        Gets the reason of this AccessRequest.
        Summary reason for which the operator is requesting access on the target resource.


        :return: The reason of this AccessRequest.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this AccessRequest.
        Summary reason for which the operator is requesting access on the target resource.


        :param reason: The reason of this AccessRequest.
        :type: str
        """
        self._reason = reason

    @property
    def severity(self):
        """
        Gets the severity of this AccessRequest.
        Priority assigned to the access request by the operator

        Allowed values for this property are: "S1", "S2", "S3", "S4", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The severity of this AccessRequest.
        :rtype: str
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """
        Sets the severity of this AccessRequest.
        Priority assigned to the access request by the operator


        :param severity: The severity of this AccessRequest.
        :type: str
        """
        allowed_values = ["S1", "S2", "S3", "S4"]
        if not value_allowed_none_or_none_sentinel(severity, allowed_values):
            severity = 'UNKNOWN_ENUM_VALUE'
        self._severity = severity

    @property
    def duration(self):
        """
        Gets the duration of this AccessRequest.
        Duration in hours for which access is sought on the target resource.


        :return: The duration of this AccessRequest.
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this AccessRequest.
        Duration in hours for which access is sought on the target resource.


        :param duration: The duration of this AccessRequest.
        :type: int
        """
        self._duration = duration

    @property
    def extend_duration(self):
        """
        Gets the extend_duration of this AccessRequest.
        Duration in hours for which extension access is sought on the target resource.


        :return: The extend_duration of this AccessRequest.
        :rtype: int
        """
        return self._extend_duration

    @extend_duration.setter
    def extend_duration(self, extend_duration):
        """
        Sets the extend_duration of this AccessRequest.
        Duration in hours for which extension access is sought on the target resource.


        :param extend_duration: The extend_duration of this AccessRequest.
        :type: int
        """
        self._extend_duration = extend_duration

    @property
    def workflow_id(self):
        """
        Gets the workflow_id of this AccessRequest.
        The OCID of the workflow associated with the access request. This is needed if you want to contact Oracle Support for a stuck access request
        or for an access request that encounters an internal error.


        :return: The workflow_id of this AccessRequest.
        :rtype: list[str]
        """
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        """
        Sets the workflow_id of this AccessRequest.
        The OCID of the workflow associated with the access request. This is needed if you want to contact Oracle Support for a stuck access request
        or for an access request that encounters an internal error.


        :param workflow_id: The workflow_id of this AccessRequest.
        :type: list[str]
        """
        self._workflow_id = workflow_id

    @property
    def is_auto_approved(self):
        """
        Gets the is_auto_approved of this AccessRequest.
        Whether the access request was automatically approved.


        :return: The is_auto_approved of this AccessRequest.
        :rtype: bool
        """
        return self._is_auto_approved

    @is_auto_approved.setter
    def is_auto_approved(self, is_auto_approved):
        """
        Sets the is_auto_approved of this AccessRequest.
        Whether the access request was automatically approved.


        :param is_auto_approved: The is_auto_approved of this AccessRequest.
        :type: bool
        """
        self._is_auto_approved = is_auto_approved

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this AccessRequest.
        The current state of the AccessRequest.

        Allowed values for this property are: "CREATED", "APPROVALWAITING", "PREAPPROVED", "APPROVED", "MOREINFO", "REJECTED", "DEPLOYED", "DEPLOYFAILED", "UNDEPLOYED", "UNDEPLOYFAILED", "CLOSEFAILED", "REVOKEFAILED", "EXPIRYFAILED", "REVOKING", "REVOKED", "EXTENDING", "EXTENDED", "EXTENSIONREJECTED", "COMPLETING", "COMPLETED", "EXPIRED", "APPROVEDFORFUTURE", "INREVIEW", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this AccessRequest.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this AccessRequest.
        The current state of the AccessRequest.


        :param lifecycle_state: The lifecycle_state of this AccessRequest.
        :type: str
        """
        allowed_values = ["CREATED", "APPROVALWAITING", "PREAPPROVED", "APPROVED", "MOREINFO", "REJECTED", "DEPLOYED", "DEPLOYFAILED", "UNDEPLOYED", "UNDEPLOYFAILED", "CLOSEFAILED", "REVOKEFAILED", "EXPIRYFAILED", "REVOKING", "REVOKED", "EXTENDING", "EXTENDED", "EXTENSIONREJECTED", "COMPLETING", "COMPLETED", "EXPIRED", "APPROVEDFORFUTURE", "INREVIEW"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this AccessRequest.
        more in detail about the lifeCycleState.


        :return: The lifecycle_details of this AccessRequest.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this AccessRequest.
        more in detail about the lifeCycleState.


        :param lifecycle_details: The lifecycle_details of this AccessRequest.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_of_creation(self):
        """
        Gets the time_of_creation of this AccessRequest.
        Time when the access request was created in `RFC 3339`__timestamp format. Example: '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_of_creation of this AccessRequest.
        :rtype: datetime
        """
        return self._time_of_creation

    @time_of_creation.setter
    def time_of_creation(self, time_of_creation):
        """
        Sets the time_of_creation of this AccessRequest.
        Time when the access request was created in `RFC 3339`__timestamp format. Example: '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :param time_of_creation: The time_of_creation of this AccessRequest.
        :type: datetime
        """
        self._time_of_creation = time_of_creation

    @property
    def time_of_modification(self):
        """
        Gets the time_of_modification of this AccessRequest.
        Time when the access request was last modified in `RFC 3339`__timestamp format. Example: '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_of_modification of this AccessRequest.
        :rtype: datetime
        """
        return self._time_of_modification

    @time_of_modification.setter
    def time_of_modification(self, time_of_modification):
        """
        Sets the time_of_modification of this AccessRequest.
        Time when the access request was last modified in `RFC 3339`__timestamp format. Example: '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :param time_of_modification: The time_of_modification of this AccessRequest.
        :type: datetime
        """
        self._time_of_modification = time_of_modification

    @property
    def time_of_user_creation(self):
        """
        Gets the time_of_user_creation of this AccessRequest.
        The time when access request is scheduled to be approved in `RFC 3339`__ timestamp format.Example: '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_of_user_creation of this AccessRequest.
        :rtype: datetime
        """
        return self._time_of_user_creation

    @time_of_user_creation.setter
    def time_of_user_creation(self, time_of_user_creation):
        """
        Sets the time_of_user_creation of this AccessRequest.
        The time when access request is scheduled to be approved in `RFC 3339`__ timestamp format.Example: '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :param time_of_user_creation: The time_of_user_creation of this AccessRequest.
        :type: datetime
        """
        self._time_of_user_creation = time_of_user_creation

    @property
    def user_id(self):
        """
        Gets the user_id of this AccessRequest.
        The OCID of the user that last modified the access request.


        :return: The user_id of this AccessRequest.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this AccessRequest.
        The OCID of the user that last modified the access request.


        :param user_id: The user_id of this AccessRequest.
        :type: str
        """
        self._user_id = user_id

    @property
    def approver_comment(self):
        """
        Gets the approver_comment of this AccessRequest.
        The last recent Comment entered by the approver of the request.


        :return: The approver_comment of this AccessRequest.
        :rtype: str
        """
        return self._approver_comment

    @approver_comment.setter
    def approver_comment(self, approver_comment):
        """
        Sets the approver_comment of this AccessRequest.
        The last recent Comment entered by the approver of the request.


        :param approver_comment: The approver_comment of this AccessRequest.
        :type: str
        """
        self._approver_comment = approver_comment

    @property
    def closure_comment(self):
        """
        Gets the closure_comment of this AccessRequest.
        The comment entered by the operator while closing the request.


        :return: The closure_comment of this AccessRequest.
        :rtype: str
        """
        return self._closure_comment

    @closure_comment.setter
    def closure_comment(self, closure_comment):
        """
        Sets the closure_comment of this AccessRequest.
        The comment entered by the operator while closing the request.


        :param closure_comment: The closure_comment of this AccessRequest.
        :type: str
        """
        self._closure_comment = closure_comment

    @property
    def opctl_id(self):
        """
        Gets the opctl_id of this AccessRequest.
        The OCID of the operator control governing the target resource.


        :return: The opctl_id of this AccessRequest.
        :rtype: str
        """
        return self._opctl_id

    @opctl_id.setter
    def opctl_id(self, opctl_id):
        """
        Sets the opctl_id of this AccessRequest.
        The OCID of the operator control governing the target resource.


        :param opctl_id: The opctl_id of this AccessRequest.
        :type: str
        """
        self._opctl_id = opctl_id

    @property
    def opctl_name(self):
        """
        Gets the opctl_name of this AccessRequest.
        Name of the Operator control governing the target resource.


        :return: The opctl_name of this AccessRequest.
        :rtype: str
        """
        return self._opctl_name

    @opctl_name.setter
    def opctl_name(self, opctl_name):
        """
        Sets the opctl_name of this AccessRequest.
        Name of the Operator control governing the target resource.


        :param opctl_name: The opctl_name of this AccessRequest.
        :type: str
        """
        self._opctl_name = opctl_name

    @property
    def system_message(self):
        """
        Gets the system_message of this AccessRequest.
        System message that will be displayed to the operator at login to the target resource.


        :return: The system_message of this AccessRequest.
        :rtype: str
        """
        return self._system_message

    @system_message.setter
    def system_message(self, system_message):
        """
        Sets the system_message of this AccessRequest.
        System message that will be displayed to the operator at login to the target resource.


        :param system_message: The system_message of this AccessRequest.
        :type: str
        """
        self._system_message = system_message

    @property
    def opctl_additional_message(self):
        """
        Gets the opctl_additional_message of this AccessRequest.
        Additional message specific to the access request that can be specified by the approver at the time of approval.


        :return: The opctl_additional_message of this AccessRequest.
        :rtype: str
        """
        return self._opctl_additional_message

    @opctl_additional_message.setter
    def opctl_additional_message(self, opctl_additional_message):
        """
        Sets the opctl_additional_message of this AccessRequest.
        Additional message specific to the access request that can be specified by the approver at the time of approval.


        :param opctl_additional_message: The opctl_additional_message of this AccessRequest.
        :type: str
        """
        self._opctl_additional_message = opctl_additional_message

    @property
    def audit_type(self):
        """
        Gets the audit_type of this AccessRequest.
        Specifies the type of auditing to be enabled. There are two levels of auditing: command-level and keystroke-level.
        By default, auditing is enabled at the command level i.e., each command issued by the operator is audited. When keystroke-level is chosen,
        in addition to command level logging, key strokes are also logged.


        :return: The audit_type of this AccessRequest.
        :rtype: list[str]
        """
        return self._audit_type

    @audit_type.setter
    def audit_type(self, audit_type):
        """
        Sets the audit_type of this AccessRequest.
        Specifies the type of auditing to be enabled. There are two levels of auditing: command-level and keystroke-level.
        By default, auditing is enabled at the command level i.e., each command issued by the operator is audited. When keystroke-level is chosen,
        in addition to command level logging, key strokes are also logged.


        :param audit_type: The audit_type of this AccessRequest.
        :type: list[str]
        """
        self._audit_type = audit_type

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this AccessRequest.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.


        :return: The freeform_tags of this AccessRequest.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this AccessRequest.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.


        :param freeform_tags: The freeform_tags of this AccessRequest.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this AccessRequest.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.


        :return: The defined_tags of this AccessRequest.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this AccessRequest.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.


        :param defined_tags: The defined_tags of this AccessRequest.
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
