# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SearchLogsDetails(object):
    """
    Search request object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SearchLogsDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_start:
            The value to assign to the time_start property of this SearchLogsDetails.
        :type time_start: datetime

        :param time_end:
            The value to assign to the time_end property of this SearchLogsDetails.
        :type time_end: datetime

        :param search_query:
            The value to assign to the search_query property of this SearchLogsDetails.
        :type search_query: str

        :param is_return_field_info:
            The value to assign to the is_return_field_info property of this SearchLogsDetails.
        :type is_return_field_info: bool

        """
        self.swagger_types = {
            'time_start': 'datetime',
            'time_end': 'datetime',
            'search_query': 'str',
            'is_return_field_info': 'bool'
        }

        self.attribute_map = {
            'time_start': 'timeStart',
            'time_end': 'timeEnd',
            'search_query': 'searchQuery',
            'is_return_field_info': 'isReturnFieldInfo'
        }

        self._time_start = None
        self._time_end = None
        self._search_query = None
        self._is_return_field_info = None

    @property
    def time_start(self):
        """
        **[Required]** Gets the time_start of this SearchLogsDetails.
        Start filter log's date and time, in the format defined by RFC3339.


        :return: The time_start of this SearchLogsDetails.
        :rtype: datetime
        """
        return self._time_start

    @time_start.setter
    def time_start(self, time_start):
        """
        Sets the time_start of this SearchLogsDetails.
        Start filter log's date and time, in the format defined by RFC3339.


        :param time_start: The time_start of this SearchLogsDetails.
        :type: datetime
        """
        self._time_start = time_start

    @property
    def time_end(self):
        """
        **[Required]** Gets the time_end of this SearchLogsDetails.
        End filter log's date and time, in the format defined by RFC3339.


        :return: The time_end of this SearchLogsDetails.
        :rtype: datetime
        """
        return self._time_end

    @time_end.setter
    def time_end(self, time_end):
        """
        Sets the time_end of this SearchLogsDetails.
        End filter log's date and time, in the format defined by RFC3339.


        :param time_end: The time_end of this SearchLogsDetails.
        :type: datetime
        """
        self._time_end = time_end

    @property
    def search_query(self):
        """
        **[Required]** Gets the search_query of this SearchLogsDetails.
        Query corresponding to the search operation. This query is parsed and validated before execution and
        should follow the specification. For more information on the query language specification, see
        `Logging Query Language Specification`__.

        __ https://docs.cloud.oracle.com/Content/Logging/Reference/query_language_specification.htm


        :return: The search_query of this SearchLogsDetails.
        :rtype: str
        """
        return self._search_query

    @search_query.setter
    def search_query(self, search_query):
        """
        Sets the search_query of this SearchLogsDetails.
        Query corresponding to the search operation. This query is parsed and validated before execution and
        should follow the specification. For more information on the query language specification, see
        `Logging Query Language Specification`__.

        __ https://docs.cloud.oracle.com/Content/Logging/Reference/query_language_specification.htm


        :param search_query: The search_query of this SearchLogsDetails.
        :type: str
        """
        self._search_query = search_query

    @property
    def is_return_field_info(self):
        """
        Gets the is_return_field_info of this SearchLogsDetails.
        Whether to return field schema information for the log stream specified in searchQuery.


        :return: The is_return_field_info of this SearchLogsDetails.
        :rtype: bool
        """
        return self._is_return_field_info

    @is_return_field_info.setter
    def is_return_field_info(self, is_return_field_info):
        """
        Sets the is_return_field_info of this SearchLogsDetails.
        Whether to return field schema information for the log stream specified in searchQuery.


        :param is_return_field_info: The is_return_field_info of this SearchLogsDetails.
        :type: bool
        """
        self._is_return_field_info = is_return_field_info

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
