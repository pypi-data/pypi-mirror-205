# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DetectLanguageSentimentsResult(object):
    """
    Result of sentiments detect call.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DetectLanguageSentimentsResult object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param aspects:
            The value to assign to the aspects property of this DetectLanguageSentimentsResult.
        :type aspects: list[oci.ai_language.models.SentimentAspect]

        """
        self.swagger_types = {
            'aspects': 'list[SentimentAspect]'
        }

        self.attribute_map = {
            'aspects': 'aspects'
        }

        self._aspects = None

    @property
    def aspects(self):
        """
        **[Required]** Gets the aspects of this DetectLanguageSentimentsResult.
        List of detected aspects.


        :return: The aspects of this DetectLanguageSentimentsResult.
        :rtype: list[oci.ai_language.models.SentimentAspect]
        """
        return self._aspects

    @aspects.setter
    def aspects(self, aspects):
        """
        Sets the aspects of this DetectLanguageSentimentsResult.
        List of detected aspects.


        :param aspects: The aspects of this DetectLanguageSentimentsResult.
        :type: list[oci.ai_language.models.SentimentAspect]
        """
        self._aspects = aspects

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
