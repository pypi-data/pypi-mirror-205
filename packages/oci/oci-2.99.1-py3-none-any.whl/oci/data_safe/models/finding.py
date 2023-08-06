# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Finding(object):
    """
    The particular finding reported by the security assessment.
    """

    #: A constant which can be used with the severity property of a Finding.
    #: This constant has a value of "HIGH"
    SEVERITY_HIGH = "HIGH"

    #: A constant which can be used with the severity property of a Finding.
    #: This constant has a value of "MEDIUM"
    SEVERITY_MEDIUM = "MEDIUM"

    #: A constant which can be used with the severity property of a Finding.
    #: This constant has a value of "LOW"
    SEVERITY_LOW = "LOW"

    #: A constant which can be used with the severity property of a Finding.
    #: This constant has a value of "EVALUATE"
    SEVERITY_EVALUATE = "EVALUATE"

    #: A constant which can be used with the severity property of a Finding.
    #: This constant has a value of "ADVISORY"
    SEVERITY_ADVISORY = "ADVISORY"

    #: A constant which can be used with the severity property of a Finding.
    #: This constant has a value of "PASS"
    SEVERITY_PASS = "PASS"

    def __init__(self, **kwargs):
        """
        Initializes a new Finding object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this Finding.
        :type key: str

        :param severity:
            The value to assign to the severity property of this Finding.
            Allowed values for this property are: "HIGH", "MEDIUM", "LOW", "EVALUATE", "ADVISORY", "PASS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type severity: str

        :param title:
            The value to assign to the title property of this Finding.
        :type title: str

        :param remarks:
            The value to assign to the remarks property of this Finding.
        :type remarks: str

        :param details:
            The value to assign to the details property of this Finding.
        :type details: object

        :param summary:
            The value to assign to the summary property of this Finding.
        :type summary: str

        :param references:
            The value to assign to the references property of this Finding.
        :type references: oci.data_safe.models.References

        """
        self.swagger_types = {
            'key': 'str',
            'severity': 'str',
            'title': 'str',
            'remarks': 'str',
            'details': 'object',
            'summary': 'str',
            'references': 'References'
        }

        self.attribute_map = {
            'key': 'key',
            'severity': 'severity',
            'title': 'title',
            'remarks': 'remarks',
            'details': 'details',
            'summary': 'summary',
            'references': 'references'
        }

        self._key = None
        self._severity = None
        self._title = None
        self._remarks = None
        self._details = None
        self._summary = None
        self._references = None

    @property
    def key(self):
        """
        Gets the key of this Finding.
        A unique identifier for the finding. This is common for the finding across targets.


        :return: The key of this Finding.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this Finding.
        A unique identifier for the finding. This is common for the finding across targets.


        :param key: The key of this Finding.
        :type: str
        """
        self._key = key

    @property
    def severity(self):
        """
        Gets the severity of this Finding.
        The severity of the finding.

        Allowed values for this property are: "HIGH", "MEDIUM", "LOW", "EVALUATE", "ADVISORY", "PASS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The severity of this Finding.
        :rtype: str
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """
        Sets the severity of this Finding.
        The severity of the finding.


        :param severity: The severity of this Finding.
        :type: str
        """
        allowed_values = ["HIGH", "MEDIUM", "LOW", "EVALUATE", "ADVISORY", "PASS"]
        if not value_allowed_none_or_none_sentinel(severity, allowed_values):
            severity = 'UNKNOWN_ENUM_VALUE'
        self._severity = severity

    @property
    def title(self):
        """
        Gets the title of this Finding.
        The short title for the finding.


        :return: The title of this Finding.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this Finding.
        The short title for the finding.


        :param title: The title of this Finding.
        :type: str
        """
        self._title = title

    @property
    def remarks(self):
        """
        Gets the remarks of this Finding.
        The explanation of the issue in this finding. It explains the reason for the rule and, if a risk is reported, it may also explain the recommended actions for remediation.


        :return: The remarks of this Finding.
        :rtype: str
        """
        return self._remarks

    @remarks.setter
    def remarks(self, remarks):
        """
        Sets the remarks of this Finding.
        The explanation of the issue in this finding. It explains the reason for the rule and, if a risk is reported, it may also explain the recommended actions for remediation.


        :param remarks: The remarks of this Finding.
        :type: str
        """
        self._remarks = remarks

    @property
    def details(self):
        """
        Gets the details of this Finding.
        The details of the finding. Provides detailed information to explain the finding summary, typically results from the assessed database, followed by any recommendations for changes.


        :return: The details of this Finding.
        :rtype: object
        """
        return self._details

    @details.setter
    def details(self, details):
        """
        Sets the details of this Finding.
        The details of the finding. Provides detailed information to explain the finding summary, typically results from the assessed database, followed by any recommendations for changes.


        :param details: The details of this Finding.
        :type: object
        """
        self._details = details

    @property
    def summary(self):
        """
        Gets the summary of this Finding.
        The brief summary of the finding. When the finding is informational, the summary typically reports only the number of data elements that were examined.


        :return: The summary of this Finding.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this Finding.
        The brief summary of the finding. When the finding is informational, the summary typically reports only the number of data elements that were examined.


        :param summary: The summary of this Finding.
        :type: str
        """
        self._summary = summary

    @property
    def references(self):
        """
        Gets the references of this Finding.
        Provides information on whether the finding is related to a CIS Oracle Database Benchmark recommendation, STIG rule, or related to a GDPR Article/Recital.


        :return: The references of this Finding.
        :rtype: oci.data_safe.models.References
        """
        return self._references

    @references.setter
    def references(self, references):
        """
        Sets the references of this Finding.
        Provides information on whether the finding is related to a CIS Oracle Database Benchmark recommendation, STIG rule, or related to a GDPR Article/Recital.


        :param references: The references of this Finding.
        :type: oci.data_safe.models.References
        """
        self._references = references

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
