# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SourceMappingResponse(object):
    """
    Response object containing match status and parsed representation of log data.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SourceMappingResponse object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param parsed_response:
            The value to assign to the parsed_response property of this SourceMappingResponse.
        :type parsed_response: list[oci.log_analytics.models.ParsedContent]

        """
        self.swagger_types = {
            'parsed_response': 'list[ParsedContent]'
        }

        self.attribute_map = {
            'parsed_response': 'parsedResponse'
        }

        self._parsed_response = None

    @property
    def parsed_response(self):
        """
        **[Required]** Gets the parsed_response of this SourceMappingResponse.
        Parsed representation of the log file.


        :return: The parsed_response of this SourceMappingResponse.
        :rtype: list[oci.log_analytics.models.ParsedContent]
        """
        return self._parsed_response

    @parsed_response.setter
    def parsed_response(self, parsed_response):
        """
        Sets the parsed_response of this SourceMappingResponse.
        Parsed representation of the log file.


        :param parsed_response: The parsed_response of this SourceMappingResponse.
        :type: list[oci.log_analytics.models.ParsedContent]
        """
        self._parsed_response = parsed_response

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
