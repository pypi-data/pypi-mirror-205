# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DetectedLanguage(object):
    """
    Attributes to the detected language. Contains Language Name , Code, and Confidence Score.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DetectedLanguage object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this DetectedLanguage.
        :type name: str

        :param code:
            The value to assign to the code property of this DetectedLanguage.
        :type code: str

        :param score:
            The value to assign to the score property of this DetectedLanguage.
        :type score: float

        """
        self.swagger_types = {
            'name': 'str',
            'code': 'str',
            'score': 'float'
        }

        self.attribute_map = {
            'name': 'name',
            'code': 'code',
            'score': 'score'
        }

        self._name = None
        self._code = None
        self._score = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this DetectedLanguage.
        Full language name.
        Example: `English, Hindi, and so on`


        :return: The name of this DetectedLanguage.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DetectedLanguage.
        Full language name.
        Example: `English, Hindi, and so on`


        :param name: The name of this DetectedLanguage.
        :type: str
        """
        self._name = name

    @property
    def code(self):
        """
        **[Required]** Gets the code of this DetectedLanguage.
        Detected language code as per `ISO 639-1`__ standard.
        Example: `en, fr, hi etc`.

        __ https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes


        :return: The code of this DetectedLanguage.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this DetectedLanguage.
        Detected language code as per `ISO 639-1`__ standard.
        Example: `en, fr, hi etc`.

        __ https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes


        :param code: The code of this DetectedLanguage.
        :type: str
        """
        self._code = code

    @property
    def score(self):
        """
        **[Required]** Gets the score of this DetectedLanguage.
        Score or confidence of detected language code.
        Example: `0.9999856066867399`


        :return: The score of this DetectedLanguage.
        :rtype: float
        """
        return self._score

    @score.setter
    def score(self, score):
        """
        Sets the score of this DetectedLanguage.
        Score or confidence of detected language code.
        Example: `0.9999856066867399`


        :param score: The score of this DetectedLanguage.
        :type: float
        """
        self._score = score

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
