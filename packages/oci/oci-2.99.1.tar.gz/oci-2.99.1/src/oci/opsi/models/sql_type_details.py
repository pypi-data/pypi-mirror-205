# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .related_object_type_details import RelatedObjectTypeDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SqlTypeDetails(RelatedObjectTypeDetails):
    """
    SQL details
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SqlTypeDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.opsi.models.SqlTypeDetails.type` attribute
        of this class is ``SQL`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this SqlTypeDetails.
            Allowed values for this property are: "SCHEMA_OBJECT", "SQL", "DATABASE_PARAMETER"
        :type type: str

        :param sql_id:
            The value to assign to the sql_id property of this SqlTypeDetails.
        :type sql_id: str

        :param sql_text:
            The value to assign to the sql_text property of this SqlTypeDetails.
        :type sql_text: str

        :param is_sql_text_truncated:
            The value to assign to the is_sql_text_truncated property of this SqlTypeDetails.
        :type is_sql_text_truncated: bool

        :param sql_command:
            The value to assign to the sql_command property of this SqlTypeDetails.
        :type sql_command: str

        """
        self.swagger_types = {
            'type': 'str',
            'sql_id': 'str',
            'sql_text': 'str',
            'is_sql_text_truncated': 'bool',
            'sql_command': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'sql_id': 'sqlId',
            'sql_text': 'sqlText',
            'is_sql_text_truncated': 'isSqlTextTruncated',
            'sql_command': 'sqlCommand'
        }

        self._type = None
        self._sql_id = None
        self._sql_text = None
        self._is_sql_text_truncated = None
        self._sql_command = None
        self._type = 'SQL'

    @property
    def sql_id(self):
        """
        **[Required]** Gets the sql_id of this SqlTypeDetails.
        SQL identifier


        :return: The sql_id of this SqlTypeDetails.
        :rtype: str
        """
        return self._sql_id

    @sql_id.setter
    def sql_id(self, sql_id):
        """
        Sets the sql_id of this SqlTypeDetails.
        SQL identifier


        :param sql_id: The sql_id of this SqlTypeDetails.
        :type: str
        """
        self._sql_id = sql_id

    @property
    def sql_text(self):
        """
        **[Required]** Gets the sql_text of this SqlTypeDetails.
        First 3800 characters of the SQL text


        :return: The sql_text of this SqlTypeDetails.
        :rtype: str
        """
        return self._sql_text

    @sql_text.setter
    def sql_text(self, sql_text):
        """
        Sets the sql_text of this SqlTypeDetails.
        First 3800 characters of the SQL text


        :param sql_text: The sql_text of this SqlTypeDetails.
        :type: str
        """
        self._sql_text = sql_text

    @property
    def is_sql_text_truncated(self):
        """
        **[Required]** Gets the is_sql_text_truncated of this SqlTypeDetails.
        SQL identifier


        :return: The is_sql_text_truncated of this SqlTypeDetails.
        :rtype: bool
        """
        return self._is_sql_text_truncated

    @is_sql_text_truncated.setter
    def is_sql_text_truncated(self, is_sql_text_truncated):
        """
        Sets the is_sql_text_truncated of this SqlTypeDetails.
        SQL identifier


        :param is_sql_text_truncated: The is_sql_text_truncated of this SqlTypeDetails.
        :type: bool
        """
        self._is_sql_text_truncated = is_sql_text_truncated

    @property
    def sql_command(self):
        """
        **[Required]** Gets the sql_command of this SqlTypeDetails.
        SQL command name (such as SELECT, INSERT)


        :return: The sql_command of this SqlTypeDetails.
        :rtype: str
        """
        return self._sql_command

    @sql_command.setter
    def sql_command(self, sql_command):
        """
        Sets the sql_command of this SqlTypeDetails.
        SQL command name (such as SELECT, INSERT)


        :param sql_command: The sql_command of this SqlTypeDetails.
        :type: str
        """
        self._sql_command = sql_command

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
