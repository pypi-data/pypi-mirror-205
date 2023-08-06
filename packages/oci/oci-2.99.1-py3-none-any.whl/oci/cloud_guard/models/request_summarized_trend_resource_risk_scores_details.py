# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RequestSummarizedTrendResourceRiskScoresDetails(object):
    """
    ResourceRiskScores filter.
    """

    #: A constant which can be used with the filter property of a RequestSummarizedTrendResourceRiskScoresDetails.
    #: This constant has a value of "PROBLEM_ID"
    FILTER_PROBLEM_ID = "PROBLEM_ID"

    #: A constant which can be used with the filter property of a RequestSummarizedTrendResourceRiskScoresDetails.
    #: This constant has a value of "RESOURCE_PROFILE_ID"
    FILTER_RESOURCE_PROFILE_ID = "RESOURCE_PROFILE_ID"

    def __init__(self, **kwargs):
        """
        Initializes a new RequestSummarizedTrendResourceRiskScoresDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param filter:
            The value to assign to the filter property of this RequestSummarizedTrendResourceRiskScoresDetails.
            Allowed values for this property are: "PROBLEM_ID", "RESOURCE_PROFILE_ID"
        :type filter: str

        :param filter_id:
            The value to assign to the filter_id property of this RequestSummarizedTrendResourceRiskScoresDetails.
        :type filter_id: str

        """
        self.swagger_types = {
            'filter': 'str',
            'filter_id': 'str'
        }

        self.attribute_map = {
            'filter': 'filter',
            'filter_id': 'filterId'
        }

        self._filter = None
        self._filter_id = None

    @property
    def filter(self):
        """
        **[Required]** Gets the filter of this RequestSummarizedTrendResourceRiskScoresDetails.
        The filter type.

        Allowed values for this property are: "PROBLEM_ID", "RESOURCE_PROFILE_ID"


        :return: The filter of this RequestSummarizedTrendResourceRiskScoresDetails.
        :rtype: str
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """
        Sets the filter of this RequestSummarizedTrendResourceRiskScoresDetails.
        The filter type.


        :param filter: The filter of this RequestSummarizedTrendResourceRiskScoresDetails.
        :type: str
        """
        allowed_values = ["PROBLEM_ID", "RESOURCE_PROFILE_ID"]
        if not value_allowed_none_or_none_sentinel(filter, allowed_values):
            raise ValueError(
                "Invalid value for `filter`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._filter = filter

    @property
    def filter_id(self):
        """
        **[Required]** Gets the filter_id of this RequestSummarizedTrendResourceRiskScoresDetails.
        Id to be passed in to filter the risk scores.


        :return: The filter_id of this RequestSummarizedTrendResourceRiskScoresDetails.
        :rtype: str
        """
        return self._filter_id

    @filter_id.setter
    def filter_id(self, filter_id):
        """
        Sets the filter_id of this RequestSummarizedTrendResourceRiskScoresDetails.
        Id to be passed in to filter the risk scores.


        :param filter_id: The filter_id of this RequestSummarizedTrendResourceRiskScoresDetails.
        :type: str
        """
        self._filter_id = filter_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
