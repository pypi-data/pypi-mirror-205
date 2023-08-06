# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RuleFinding(object):
    """
    The summary of the Optimizer Statistics Advisor findings and recommendations.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RuleFinding object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param message:
            The value to assign to the message property of this RuleFinding.
        :type message: str

        :param details:
            The value to assign to the details property of this RuleFinding.
        :type details: list[oci.database_management.models.FindingSchemaOrOperation]

        :param recommendations:
            The value to assign to the recommendations property of this RuleFinding.
        :type recommendations: list[oci.database_management.models.Recommendation]

        """
        self.swagger_types = {
            'message': 'str',
            'details': 'list[FindingSchemaOrOperation]',
            'recommendations': 'list[Recommendation]'
        }

        self.attribute_map = {
            'message': 'message',
            'details': 'details',
            'recommendations': 'recommendations'
        }

        self._message = None
        self._details = None
        self._recommendations = None

    @property
    def message(self):
        """
        **[Required]** Gets the message of this RuleFinding.
        A high-level overview of the findings of the Optimizer Statistics Advisor.


        :return: The message of this RuleFinding.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this RuleFinding.
        A high-level overview of the findings of the Optimizer Statistics Advisor.


        :param message: The message of this RuleFinding.
        :type: str
        """
        self._message = message

    @property
    def details(self):
        """
        **[Required]** Gets the details of this RuleFinding.
        The details of the schema or operation.


        :return: The details of this RuleFinding.
        :rtype: list[oci.database_management.models.FindingSchemaOrOperation]
        """
        return self._details

    @details.setter
    def details(self, details):
        """
        Sets the details of this RuleFinding.
        The details of the schema or operation.


        :param details: The details of this RuleFinding.
        :type: list[oci.database_management.models.FindingSchemaOrOperation]
        """
        self._details = details

    @property
    def recommendations(self):
        """
        **[Required]** Gets the recommendations of this RuleFinding.
        The list of recommendations.


        :return: The recommendations of this RuleFinding.
        :rtype: list[oci.database_management.models.Recommendation]
        """
        return self._recommendations

    @recommendations.setter
    def recommendations(self, recommendations):
        """
        Sets the recommendations of this RuleFinding.
        The list of recommendations.


        :param recommendations: The recommendations of this RuleFinding.
        :type: list[oci.database_management.models.Recommendation]
        """
        self._recommendations = recommendations

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
