# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PdbMetrics(object):
    """
    The summary of Pluggable Databases (PDBs) and their resource usage metrics, within a specific Container Database (CDB).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PdbMetrics object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param database_usage_metrics:
            The value to assign to the database_usage_metrics property of this PdbMetrics.
        :type database_usage_metrics: list[oci.database_management.models.DatabaseUsageMetrics]

        """
        self.swagger_types = {
            'database_usage_metrics': 'list[DatabaseUsageMetrics]'
        }

        self.attribute_map = {
            'database_usage_metrics': 'databaseUsageMetrics'
        }

        self._database_usage_metrics = None

    @property
    def database_usage_metrics(self):
        """
        **[Required]** Gets the database_usage_metrics of this PdbMetrics.
        A summary of PDBs and their resource usage metrics such as CPU, User I/O, and Storage, within a specific CDB.


        :return: The database_usage_metrics of this PdbMetrics.
        :rtype: list[oci.database_management.models.DatabaseUsageMetrics]
        """
        return self._database_usage_metrics

    @database_usage_metrics.setter
    def database_usage_metrics(self, database_usage_metrics):
        """
        Sets the database_usage_metrics of this PdbMetrics.
        A summary of PDBs and their resource usage metrics such as CPU, User I/O, and Storage, within a specific CDB.


        :param database_usage_metrics: The database_usage_metrics of this PdbMetrics.
        :type: list[oci.database_management.models.DatabaseUsageMetrics]
        """
        self._database_usage_metrics = database_usage_metrics

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
