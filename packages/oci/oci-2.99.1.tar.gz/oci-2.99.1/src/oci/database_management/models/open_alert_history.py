# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class OpenAlertHistory(object):
    """
    The open alerts current existing in a storage server.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new OpenAlertHistory object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param alerts:
            The value to assign to the alerts property of this OpenAlertHistory.
        :type alerts: list[oci.database_management.models.OpenAlertSummary]

        """
        self.swagger_types = {
            'alerts': 'list[OpenAlertSummary]'
        }

        self.attribute_map = {
            'alerts': 'alerts'
        }

        self._alerts = None

    @property
    def alerts(self):
        """
        **[Required]** Gets the alerts of this OpenAlertHistory.
        A list of open alerts.


        :return: The alerts of this OpenAlertHistory.
        :rtype: list[oci.database_management.models.OpenAlertSummary]
        """
        return self._alerts

    @alerts.setter
    def alerts(self, alerts):
        """
        Sets the alerts of this OpenAlertHistory.
        A list of open alerts.


        :param alerts: The alerts of this OpenAlertHistory.
        :type: list[oci.database_management.models.OpenAlertSummary]
        """
        self._alerts = alerts

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
