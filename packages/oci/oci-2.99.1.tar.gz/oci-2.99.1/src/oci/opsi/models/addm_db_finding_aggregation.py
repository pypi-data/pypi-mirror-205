# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddmDbFindingAggregation(object):
    """
    Summarizes a specific ADDM finding
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddmDbFindingAggregation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this AddmDbFindingAggregation.
        :type id: str

        :param finding_id:
            The value to assign to the finding_id property of this AddmDbFindingAggregation.
        :type finding_id: str

        :param category_name:
            The value to assign to the category_name property of this AddmDbFindingAggregation.
        :type category_name: str

        :param category_display_name:
            The value to assign to the category_display_name property of this AddmDbFindingAggregation.
        :type category_display_name: str

        :param name:
            The value to assign to the name property of this AddmDbFindingAggregation.
        :type name: str

        :param message:
            The value to assign to the message property of this AddmDbFindingAggregation.
        :type message: str

        :param impact_overall_percent:
            The value to assign to the impact_overall_percent property of this AddmDbFindingAggregation.
        :type impact_overall_percent: float

        :param impact_max_percent:
            The value to assign to the impact_max_percent property of this AddmDbFindingAggregation.
        :type impact_max_percent: float

        :param impact_avg_active_sessions:
            The value to assign to the impact_avg_active_sessions property of this AddmDbFindingAggregation.
        :type impact_avg_active_sessions: float

        :param frequency_count:
            The value to assign to the frequency_count property of this AddmDbFindingAggregation.
        :type frequency_count: int

        :param recommendation_count:
            The value to assign to the recommendation_count property of this AddmDbFindingAggregation.
        :type recommendation_count: int

        """
        self.swagger_types = {
            'id': 'str',
            'finding_id': 'str',
            'category_name': 'str',
            'category_display_name': 'str',
            'name': 'str',
            'message': 'str',
            'impact_overall_percent': 'float',
            'impact_max_percent': 'float',
            'impact_avg_active_sessions': 'float',
            'frequency_count': 'int',
            'recommendation_count': 'int'
        }

        self.attribute_map = {
            'id': 'id',
            'finding_id': 'findingId',
            'category_name': 'categoryName',
            'category_display_name': 'categoryDisplayName',
            'name': 'name',
            'message': 'message',
            'impact_overall_percent': 'impactOverallPercent',
            'impact_max_percent': 'impactMaxPercent',
            'impact_avg_active_sessions': 'impactAvgActiveSessions',
            'frequency_count': 'frequencyCount',
            'recommendation_count': 'recommendationCount'
        }

        self._id = None
        self._finding_id = None
        self._category_name = None
        self._category_display_name = None
        self._name = None
        self._message = None
        self._impact_overall_percent = None
        self._impact_max_percent = None
        self._impact_avg_active_sessions = None
        self._frequency_count = None
        self._recommendation_count = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this AddmDbFindingAggregation.
        The `OCID`__ of the Database insight.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this AddmDbFindingAggregation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AddmDbFindingAggregation.
        The `OCID`__ of the Database insight.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this AddmDbFindingAggregation.
        :type: str
        """
        self._id = id

    @property
    def finding_id(self):
        """
        **[Required]** Gets the finding_id of this AddmDbFindingAggregation.
        Unique finding id


        :return: The finding_id of this AddmDbFindingAggregation.
        :rtype: str
        """
        return self._finding_id

    @finding_id.setter
    def finding_id(self, finding_id):
        """
        Sets the finding_id of this AddmDbFindingAggregation.
        Unique finding id


        :param finding_id: The finding_id of this AddmDbFindingAggregation.
        :type: str
        """
        self._finding_id = finding_id

    @property
    def category_name(self):
        """
        **[Required]** Gets the category_name of this AddmDbFindingAggregation.
        Category name


        :return: The category_name of this AddmDbFindingAggregation.
        :rtype: str
        """
        return self._category_name

    @category_name.setter
    def category_name(self, category_name):
        """
        Sets the category_name of this AddmDbFindingAggregation.
        Category name


        :param category_name: The category_name of this AddmDbFindingAggregation.
        :type: str
        """
        self._category_name = category_name

    @property
    def category_display_name(self):
        """
        **[Required]** Gets the category_display_name of this AddmDbFindingAggregation.
        Category display name


        :return: The category_display_name of this AddmDbFindingAggregation.
        :rtype: str
        """
        return self._category_display_name

    @category_display_name.setter
    def category_display_name(self, category_display_name):
        """
        Sets the category_display_name of this AddmDbFindingAggregation.
        Category display name


        :param category_display_name: The category_display_name of this AddmDbFindingAggregation.
        :type: str
        """
        self._category_display_name = category_display_name

    @property
    def name(self):
        """
        **[Required]** Gets the name of this AddmDbFindingAggregation.
        Finding name


        :return: The name of this AddmDbFindingAggregation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AddmDbFindingAggregation.
        Finding name


        :param name: The name of this AddmDbFindingAggregation.
        :type: str
        """
        self._name = name

    @property
    def message(self):
        """
        **[Required]** Gets the message of this AddmDbFindingAggregation.
        Finding message


        :return: The message of this AddmDbFindingAggregation.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this AddmDbFindingAggregation.
        Finding message


        :param message: The message of this AddmDbFindingAggregation.
        :type: str
        """
        self._message = message

    @property
    def impact_overall_percent(self):
        """
        **[Required]** Gets the impact_overall_percent of this AddmDbFindingAggregation.
        Overall impact in terms of percentage of total activity


        :return: The impact_overall_percent of this AddmDbFindingAggregation.
        :rtype: float
        """
        return self._impact_overall_percent

    @impact_overall_percent.setter
    def impact_overall_percent(self, impact_overall_percent):
        """
        Sets the impact_overall_percent of this AddmDbFindingAggregation.
        Overall impact in terms of percentage of total activity


        :param impact_overall_percent: The impact_overall_percent of this AddmDbFindingAggregation.
        :type: float
        """
        self._impact_overall_percent = impact_overall_percent

    @property
    def impact_max_percent(self):
        """
        **[Required]** Gets the impact_max_percent of this AddmDbFindingAggregation.
        Maximum impact in terms of percentage of total activity


        :return: The impact_max_percent of this AddmDbFindingAggregation.
        :rtype: float
        """
        return self._impact_max_percent

    @impact_max_percent.setter
    def impact_max_percent(self, impact_max_percent):
        """
        Sets the impact_max_percent of this AddmDbFindingAggregation.
        Maximum impact in terms of percentage of total activity


        :param impact_max_percent: The impact_max_percent of this AddmDbFindingAggregation.
        :type: float
        """
        self._impact_max_percent = impact_max_percent

    @property
    def impact_avg_active_sessions(self):
        """
        Gets the impact_avg_active_sessions of this AddmDbFindingAggregation.
        Impact in terms of average active sessions


        :return: The impact_avg_active_sessions of this AddmDbFindingAggregation.
        :rtype: float
        """
        return self._impact_avg_active_sessions

    @impact_avg_active_sessions.setter
    def impact_avg_active_sessions(self, impact_avg_active_sessions):
        """
        Sets the impact_avg_active_sessions of this AddmDbFindingAggregation.
        Impact in terms of average active sessions


        :param impact_avg_active_sessions: The impact_avg_active_sessions of this AddmDbFindingAggregation.
        :type: float
        """
        self._impact_avg_active_sessions = impact_avg_active_sessions

    @property
    def frequency_count(self):
        """
        **[Required]** Gets the frequency_count of this AddmDbFindingAggregation.
        Number of occurrences for this finding


        :return: The frequency_count of this AddmDbFindingAggregation.
        :rtype: int
        """
        return self._frequency_count

    @frequency_count.setter
    def frequency_count(self, frequency_count):
        """
        Sets the frequency_count of this AddmDbFindingAggregation.
        Number of occurrences for this finding


        :param frequency_count: The frequency_count of this AddmDbFindingAggregation.
        :type: int
        """
        self._frequency_count = frequency_count

    @property
    def recommendation_count(self):
        """
        **[Required]** Gets the recommendation_count of this AddmDbFindingAggregation.
        Number of recommendations for this finding


        :return: The recommendation_count of this AddmDbFindingAggregation.
        :rtype: int
        """
        return self._recommendation_count

    @recommendation_count.setter
    def recommendation_count(self, recommendation_count):
        """
        Sets the recommendation_count of this AddmDbFindingAggregation.
        Number of recommendations for this finding


        :param recommendation_count: The recommendation_count of this AddmDbFindingAggregation.
        :type: int
        """
        self._recommendation_count = recommendation_count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
