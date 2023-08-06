# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RiskScoreAggregation(object):
    """
    Provides the dimensions and their corresponding risk score.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RiskScoreAggregation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param dimensions_map:
            The value to assign to the dimensions_map property of this RiskScoreAggregation.
        :type dimensions_map: dict(str, str)

        :param risk_score:
            The value to assign to the risk_score property of this RiskScoreAggregation.
        :type risk_score: int

        """
        self.swagger_types = {
            'dimensions_map': 'dict(str, str)',
            'risk_score': 'int'
        }

        self.attribute_map = {
            'dimensions_map': 'dimensionsMap',
            'risk_score': 'riskScore'
        }

        self._dimensions_map = None
        self._risk_score = None

    @property
    def dimensions_map(self):
        """
        **[Required]** Gets the dimensions_map of this RiskScoreAggregation.
        The key-value pairs of dimensions and their names.


        :return: The dimensions_map of this RiskScoreAggregation.
        :rtype: dict(str, str)
        """
        return self._dimensions_map

    @dimensions_map.setter
    def dimensions_map(self, dimensions_map):
        """
        Sets the dimensions_map of this RiskScoreAggregation.
        The key-value pairs of dimensions and their names.


        :param dimensions_map: The dimensions_map of this RiskScoreAggregation.
        :type: dict(str, str)
        """
        self._dimensions_map = dimensions_map

    @property
    def risk_score(self):
        """
        **[Required]** Gets the risk_score of this RiskScoreAggregation.
        The risk score with given dimensions


        :return: The risk_score of this RiskScoreAggregation.
        :rtype: int
        """
        return self._risk_score

    @risk_score.setter
    def risk_score(self, risk_score):
        """
        Sets the risk_score of this RiskScoreAggregation.
        The risk score with given dimensions


        :param risk_score: The risk_score of this RiskScoreAggregation.
        :type: int
        """
        self._risk_score = risk_score

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
