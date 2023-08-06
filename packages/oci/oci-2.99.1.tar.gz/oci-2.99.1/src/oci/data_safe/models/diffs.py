# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Diffs(object):
    """
    Results of the comparison of an item between two security assessments.
    """

    #: A constant which can be used with the severity property of a Diffs.
    #: This constant has a value of "HIGH"
    SEVERITY_HIGH = "HIGH"

    #: A constant which can be used with the severity property of a Diffs.
    #: This constant has a value of "MEDIUM"
    SEVERITY_MEDIUM = "MEDIUM"

    #: A constant which can be used with the severity property of a Diffs.
    #: This constant has a value of "LOW"
    SEVERITY_LOW = "LOW"

    #: A constant which can be used with the severity property of a Diffs.
    #: This constant has a value of "EVALUATE"
    SEVERITY_EVALUATE = "EVALUATE"

    #: A constant which can be used with the severity property of a Diffs.
    #: This constant has a value of "ADVISORY"
    SEVERITY_ADVISORY = "ADVISORY"

    #: A constant which can be used with the severity property of a Diffs.
    #: This constant has a value of "PASS"
    SEVERITY_PASS = "PASS"

    def __init__(self, **kwargs):
        """
        Initializes a new Diffs object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param current:
            The value to assign to the current property of this Diffs.
        :type current: oci.data_safe.models.Finding

        :param baseline:
            The value to assign to the baseline property of this Diffs.
        :type baseline: oci.data_safe.models.Finding

        :param removed_items:
            The value to assign to the removed_items property of this Diffs.
        :type removed_items: list[str]

        :param added_items:
            The value to assign to the added_items property of this Diffs.
        :type added_items: list[str]

        :param modified_items:
            The value to assign to the modified_items property of this Diffs.
        :type modified_items: list[str]

        :param severity:
            The value to assign to the severity property of this Diffs.
            Allowed values for this property are: "HIGH", "MEDIUM", "LOW", "EVALUATE", "ADVISORY", "PASS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type severity: str

        """
        self.swagger_types = {
            'current': 'Finding',
            'baseline': 'Finding',
            'removed_items': 'list[str]',
            'added_items': 'list[str]',
            'modified_items': 'list[str]',
            'severity': 'str'
        }

        self.attribute_map = {
            'current': 'current',
            'baseline': 'baseline',
            'removed_items': 'removedItems',
            'added_items': 'addedItems',
            'modified_items': 'modifiedItems',
            'severity': 'severity'
        }

        self._current = None
        self._baseline = None
        self._removed_items = None
        self._added_items = None
        self._modified_items = None
        self._severity = None

    @property
    def current(self):
        """
        Gets the current of this Diffs.

        :return: The current of this Diffs.
        :rtype: oci.data_safe.models.Finding
        """
        return self._current

    @current.setter
    def current(self, current):
        """
        Sets the current of this Diffs.

        :param current: The current of this Diffs.
        :type: oci.data_safe.models.Finding
        """
        self._current = current

    @property
    def baseline(self):
        """
        Gets the baseline of this Diffs.

        :return: The baseline of this Diffs.
        :rtype: oci.data_safe.models.Finding
        """
        return self._baseline

    @baseline.setter
    def baseline(self, baseline):
        """
        Sets the baseline of this Diffs.

        :param baseline: The baseline of this Diffs.
        :type: oci.data_safe.models.Finding
        """
        self._baseline = baseline

    @property
    def removed_items(self):
        """
        Gets the removed_items of this Diffs.
        This array identifies the items that are present in the baseline, but are missing from the current assessment.


        :return: The removed_items of this Diffs.
        :rtype: list[str]
        """
        return self._removed_items

    @removed_items.setter
    def removed_items(self, removed_items):
        """
        Sets the removed_items of this Diffs.
        This array identifies the items that are present in the baseline, but are missing from the current assessment.


        :param removed_items: The removed_items of this Diffs.
        :type: list[str]
        """
        self._removed_items = removed_items

    @property
    def added_items(self):
        """
        Gets the added_items of this Diffs.
        This array identifies the items that are present in the current assessment, but are missing from the baseline.


        :return: The added_items of this Diffs.
        :rtype: list[str]
        """
        return self._added_items

    @added_items.setter
    def added_items(self, added_items):
        """
        Sets the added_items of this Diffs.
        This array identifies the items that are present in the current assessment, but are missing from the baseline.


        :param added_items: The added_items of this Diffs.
        :type: list[str]
        """
        self._added_items = added_items

    @property
    def modified_items(self):
        """
        Gets the modified_items of this Diffs.
        This array contains the items that are present in both the current assessment and the baseline, but are different in the two assessments.


        :return: The modified_items of this Diffs.
        :rtype: list[str]
        """
        return self._modified_items

    @modified_items.setter
    def modified_items(self, modified_items):
        """
        Sets the modified_items of this Diffs.
        This array contains the items that are present in both the current assessment and the baseline, but are different in the two assessments.


        :param modified_items: The modified_items of this Diffs.
        :type: list[str]
        """
        self._modified_items = modified_items

    @property
    def severity(self):
        """
        Gets the severity of this Diffs.
        The severity of this diff.

        Allowed values for this property are: "HIGH", "MEDIUM", "LOW", "EVALUATE", "ADVISORY", "PASS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The severity of this Diffs.
        :rtype: str
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """
        Sets the severity of this Diffs.
        The severity of this diff.


        :param severity: The severity of this Diffs.
        :type: str
        """
        allowed_values = ["HIGH", "MEDIUM", "LOW", "EVALUATE", "ADVISORY", "PASS"]
        if not value_allowed_none_or_none_sentinel(severity, allowed_values):
            severity = 'UNKNOWN_ENUM_VALUE'
        self._severity = severity

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
