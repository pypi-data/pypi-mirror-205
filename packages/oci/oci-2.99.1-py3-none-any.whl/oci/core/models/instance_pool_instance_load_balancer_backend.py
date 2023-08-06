# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class InstancePoolInstanceLoadBalancerBackend(object):
    """
    Represents the load balancer Backend that is configured for an instance pool instance.
    """

    #: A constant which can be used with the backend_health_status property of a InstancePoolInstanceLoadBalancerBackend.
    #: This constant has a value of "OK"
    BACKEND_HEALTH_STATUS_OK = "OK"

    #: A constant which can be used with the backend_health_status property of a InstancePoolInstanceLoadBalancerBackend.
    #: This constant has a value of "WARNING"
    BACKEND_HEALTH_STATUS_WARNING = "WARNING"

    #: A constant which can be used with the backend_health_status property of a InstancePoolInstanceLoadBalancerBackend.
    #: This constant has a value of "CRITICAL"
    BACKEND_HEALTH_STATUS_CRITICAL = "CRITICAL"

    #: A constant which can be used with the backend_health_status property of a InstancePoolInstanceLoadBalancerBackend.
    #: This constant has a value of "UNKNOWN"
    BACKEND_HEALTH_STATUS_UNKNOWN = "UNKNOWN"

    def __init__(self, **kwargs):
        """
        Initializes a new InstancePoolInstanceLoadBalancerBackend object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param load_balancer_id:
            The value to assign to the load_balancer_id property of this InstancePoolInstanceLoadBalancerBackend.
        :type load_balancer_id: str

        :param backend_set_name:
            The value to assign to the backend_set_name property of this InstancePoolInstanceLoadBalancerBackend.
        :type backend_set_name: str

        :param backend_name:
            The value to assign to the backend_name property of this InstancePoolInstanceLoadBalancerBackend.
        :type backend_name: str

        :param backend_health_status:
            The value to assign to the backend_health_status property of this InstancePoolInstanceLoadBalancerBackend.
            Allowed values for this property are: "OK", "WARNING", "CRITICAL", "UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type backend_health_status: str

        """
        self.swagger_types = {
            'load_balancer_id': 'str',
            'backend_set_name': 'str',
            'backend_name': 'str',
            'backend_health_status': 'str'
        }

        self.attribute_map = {
            'load_balancer_id': 'loadBalancerId',
            'backend_set_name': 'backendSetName',
            'backend_name': 'backendName',
            'backend_health_status': 'backendHealthStatus'
        }

        self._load_balancer_id = None
        self._backend_set_name = None
        self._backend_name = None
        self._backend_health_status = None

    @property
    def load_balancer_id(self):
        """
        **[Required]** Gets the load_balancer_id of this InstancePoolInstanceLoadBalancerBackend.
        The OCID of the load balancer attached to the instance pool.


        :return: The load_balancer_id of this InstancePoolInstanceLoadBalancerBackend.
        :rtype: str
        """
        return self._load_balancer_id

    @load_balancer_id.setter
    def load_balancer_id(self, load_balancer_id):
        """
        Sets the load_balancer_id of this InstancePoolInstanceLoadBalancerBackend.
        The OCID of the load balancer attached to the instance pool.


        :param load_balancer_id: The load_balancer_id of this InstancePoolInstanceLoadBalancerBackend.
        :type: str
        """
        self._load_balancer_id = load_balancer_id

    @property
    def backend_set_name(self):
        """
        **[Required]** Gets the backend_set_name of this InstancePoolInstanceLoadBalancerBackend.
        The name of the backend set on the load balancer.


        :return: The backend_set_name of this InstancePoolInstanceLoadBalancerBackend.
        :rtype: str
        """
        return self._backend_set_name

    @backend_set_name.setter
    def backend_set_name(self, backend_set_name):
        """
        Sets the backend_set_name of this InstancePoolInstanceLoadBalancerBackend.
        The name of the backend set on the load balancer.


        :param backend_set_name: The backend_set_name of this InstancePoolInstanceLoadBalancerBackend.
        :type: str
        """
        self._backend_set_name = backend_set_name

    @property
    def backend_name(self):
        """
        **[Required]** Gets the backend_name of this InstancePoolInstanceLoadBalancerBackend.
        The name of the backend in the backend set.


        :return: The backend_name of this InstancePoolInstanceLoadBalancerBackend.
        :rtype: str
        """
        return self._backend_name

    @backend_name.setter
    def backend_name(self, backend_name):
        """
        Sets the backend_name of this InstancePoolInstanceLoadBalancerBackend.
        The name of the backend in the backend set.


        :param backend_name: The backend_name of this InstancePoolInstanceLoadBalancerBackend.
        :type: str
        """
        self._backend_name = backend_name

    @property
    def backend_health_status(self):
        """
        **[Required]** Gets the backend_health_status of this InstancePoolInstanceLoadBalancerBackend.
        The health of the backend as observed by the load balancer.

        Allowed values for this property are: "OK", "WARNING", "CRITICAL", "UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The backend_health_status of this InstancePoolInstanceLoadBalancerBackend.
        :rtype: str
        """
        return self._backend_health_status

    @backend_health_status.setter
    def backend_health_status(self, backend_health_status):
        """
        Sets the backend_health_status of this InstancePoolInstanceLoadBalancerBackend.
        The health of the backend as observed by the load balancer.


        :param backend_health_status: The backend_health_status of this InstancePoolInstanceLoadBalancerBackend.
        :type: str
        """
        allowed_values = ["OK", "WARNING", "CRITICAL", "UNKNOWN"]
        if not value_allowed_none_or_none_sentinel(backend_health_status, allowed_values):
            backend_health_status = 'UNKNOWN_ENUM_VALUE'
        self._backend_health_status = backend_health_status

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
