# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .traffic_rule_target_details import TrafficRuleTargetDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VirtualDeploymentTrafficRuleTargetDetails(TrafficRuleTargetDetails):
    """
    Traffic router target for a virtual service version.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VirtualDeploymentTrafficRuleTargetDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.service_mesh.models.VirtualDeploymentTrafficRuleTargetDetails.type` attribute
        of this class is ``VIRTUAL_DEPLOYMENT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this VirtualDeploymentTrafficRuleTargetDetails.
            Allowed values for this property are: "VIRTUAL_DEPLOYMENT", "VIRTUAL_SERVICE"
        :type type: str

        :param virtual_deployment_id:
            The value to assign to the virtual_deployment_id property of this VirtualDeploymentTrafficRuleTargetDetails.
        :type virtual_deployment_id: str

        :param port:
            The value to assign to the port property of this VirtualDeploymentTrafficRuleTargetDetails.
        :type port: int

        :param weight:
            The value to assign to the weight property of this VirtualDeploymentTrafficRuleTargetDetails.
        :type weight: int

        """
        self.swagger_types = {
            'type': 'str',
            'virtual_deployment_id': 'str',
            'port': 'int',
            'weight': 'int'
        }

        self.attribute_map = {
            'type': 'type',
            'virtual_deployment_id': 'virtualDeploymentId',
            'port': 'port',
            'weight': 'weight'
        }

        self._type = None
        self._virtual_deployment_id = None
        self._port = None
        self._weight = None
        self._type = 'VIRTUAL_DEPLOYMENT'

    @property
    def virtual_deployment_id(self):
        """
        **[Required]** Gets the virtual_deployment_id of this VirtualDeploymentTrafficRuleTargetDetails.
        The OCID of the virtual deployment where the request will be routed.


        :return: The virtual_deployment_id of this VirtualDeploymentTrafficRuleTargetDetails.
        :rtype: str
        """
        return self._virtual_deployment_id

    @virtual_deployment_id.setter
    def virtual_deployment_id(self, virtual_deployment_id):
        """
        Sets the virtual_deployment_id of this VirtualDeploymentTrafficRuleTargetDetails.
        The OCID of the virtual deployment where the request will be routed.


        :param virtual_deployment_id: The virtual_deployment_id of this VirtualDeploymentTrafficRuleTargetDetails.
        :type: str
        """
        self._virtual_deployment_id = virtual_deployment_id

    @property
    def port(self):
        """
        Gets the port of this VirtualDeploymentTrafficRuleTargetDetails.
        Port on virtual deployment to target.
        If port is missing, the rule will target all ports on the virtual deployment.


        :return: The port of this VirtualDeploymentTrafficRuleTargetDetails.
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port of this VirtualDeploymentTrafficRuleTargetDetails.
        Port on virtual deployment to target.
        If port is missing, the rule will target all ports on the virtual deployment.


        :param port: The port of this VirtualDeploymentTrafficRuleTargetDetails.
        :type: int
        """
        self._port = port

    @property
    def weight(self):
        """
        **[Required]** Gets the weight of this VirtualDeploymentTrafficRuleTargetDetails.
        Weight of traffic target.


        :return: The weight of this VirtualDeploymentTrafficRuleTargetDetails.
        :rtype: int
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """
        Sets the weight of this VirtualDeploymentTrafficRuleTargetDetails.
        Weight of traffic target.


        :param weight: The weight of this VirtualDeploymentTrafficRuleTargetDetails.
        :type: int
        """
        self._weight = weight

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
