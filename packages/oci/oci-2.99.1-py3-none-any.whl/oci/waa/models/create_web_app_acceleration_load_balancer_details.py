# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_web_app_acceleration_details import CreateWebAppAccelerationDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateWebAppAccelerationLoadBalancerDetails(CreateWebAppAccelerationDetails):
    """
    The information about new WebAppAccelerationLoadBalancer.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateWebAppAccelerationLoadBalancerDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.waa.models.CreateWebAppAccelerationLoadBalancerDetails.backend_type` attribute
        of this class is ``LOAD_BALANCER`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this CreateWebAppAccelerationLoadBalancerDetails.
        :type display_name: str

        :param backend_type:
            The value to assign to the backend_type property of this CreateWebAppAccelerationLoadBalancerDetails.
            Allowed values for this property are: "LOAD_BALANCER"
        :type backend_type: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateWebAppAccelerationLoadBalancerDetails.
        :type compartment_id: str

        :param web_app_acceleration_policy_id:
            The value to assign to the web_app_acceleration_policy_id property of this CreateWebAppAccelerationLoadBalancerDetails.
        :type web_app_acceleration_policy_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateWebAppAccelerationLoadBalancerDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateWebAppAccelerationLoadBalancerDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this CreateWebAppAccelerationLoadBalancerDetails.
        :type system_tags: dict(str, dict(str, object))

        :param load_balancer_id:
            The value to assign to the load_balancer_id property of this CreateWebAppAccelerationLoadBalancerDetails.
        :type load_balancer_id: str

        """
        self.swagger_types = {
            'display_name': 'str',
            'backend_type': 'str',
            'compartment_id': 'str',
            'web_app_acceleration_policy_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'load_balancer_id': 'str'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'backend_type': 'backendType',
            'compartment_id': 'compartmentId',
            'web_app_acceleration_policy_id': 'webAppAccelerationPolicyId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'load_balancer_id': 'loadBalancerId'
        }

        self._display_name = None
        self._backend_type = None
        self._compartment_id = None
        self._web_app_acceleration_policy_id = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._load_balancer_id = None
        self._backend_type = 'LOAD_BALANCER'

    @property
    def load_balancer_id(self):
        """
        **[Required]** Gets the load_balancer_id of this CreateWebAppAccelerationLoadBalancerDetails.
        LoadBalancer `OCID`__ to which the WebAppAccelerationPolicy is attached to.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The load_balancer_id of this CreateWebAppAccelerationLoadBalancerDetails.
        :rtype: str
        """
        return self._load_balancer_id

    @load_balancer_id.setter
    def load_balancer_id(self, load_balancer_id):
        """
        Sets the load_balancer_id of this CreateWebAppAccelerationLoadBalancerDetails.
        LoadBalancer `OCID`__ to which the WebAppAccelerationPolicy is attached to.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param load_balancer_id: The load_balancer_id of this CreateWebAppAccelerationLoadBalancerDetails.
        :type: str
        """
        self._load_balancer_id = load_balancer_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
