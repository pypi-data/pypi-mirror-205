# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AudioFormatDetails(object):
    """
    Audio format details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AudioFormatDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param format:
            The value to assign to the format property of this AudioFormatDetails.
        :type format: str

        :param number_of_channels:
            The value to assign to the number_of_channels property of this AudioFormatDetails.
        :type number_of_channels: int

        :param encoding:
            The value to assign to the encoding property of this AudioFormatDetails.
        :type encoding: str

        :param sample_rate_in_hz:
            The value to assign to the sample_rate_in_hz property of this AudioFormatDetails.
        :type sample_rate_in_hz: int

        """
        self.swagger_types = {
            'format': 'str',
            'number_of_channels': 'int',
            'encoding': 'str',
            'sample_rate_in_hz': 'int'
        }

        self.attribute_map = {
            'format': 'format',
            'number_of_channels': 'numberOfChannels',
            'encoding': 'encoding',
            'sample_rate_in_hz': 'sampleRateInHz'
        }

        self._format = None
        self._number_of_channels = None
        self._encoding = None
        self._sample_rate_in_hz = None

    @property
    def format(self):
        """
        Gets the format of this AudioFormatDetails.
        Input file format. Example - WAV.


        :return: The format of this AudioFormatDetails.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """
        Sets the format of this AudioFormatDetails.
        Input file format. Example - WAV.


        :param format: The format of this AudioFormatDetails.
        :type: str
        """
        self._format = format

    @property
    def number_of_channels(self):
        """
        Gets the number_of_channels of this AudioFormatDetails.
        Input file number of channels.


        :return: The number_of_channels of this AudioFormatDetails.
        :rtype: int
        """
        return self._number_of_channels

    @number_of_channels.setter
    def number_of_channels(self, number_of_channels):
        """
        Sets the number_of_channels of this AudioFormatDetails.
        Input file number of channels.


        :param number_of_channels: The number_of_channels of this AudioFormatDetails.
        :type: int
        """
        self._number_of_channels = number_of_channels

    @property
    def encoding(self):
        """
        Gets the encoding of this AudioFormatDetails.
        Input file encoding. Example - PCM.


        :return: The encoding of this AudioFormatDetails.
        :rtype: str
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        """
        Sets the encoding of this AudioFormatDetails.
        Input file encoding. Example - PCM.


        :param encoding: The encoding of this AudioFormatDetails.
        :type: str
        """
        self._encoding = encoding

    @property
    def sample_rate_in_hz(self):
        """
        Gets the sample_rate_in_hz of this AudioFormatDetails.
        Input file sampleRate. Example - 16000


        :return: The sample_rate_in_hz of this AudioFormatDetails.
        :rtype: int
        """
        return self._sample_rate_in_hz

    @sample_rate_in_hz.setter
    def sample_rate_in_hz(self, sample_rate_in_hz):
        """
        Sets the sample_rate_in_hz of this AudioFormatDetails.
        Input file sampleRate. Example - 16000


        :param sample_rate_in_hz: The sample_rate_in_hz of this AudioFormatDetails.
        :type: int
        """
        self._sample_rate_in_hz = sample_rate_in_hz

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
