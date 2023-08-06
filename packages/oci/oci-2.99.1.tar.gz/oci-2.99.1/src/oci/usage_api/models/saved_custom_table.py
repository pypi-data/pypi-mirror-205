# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SavedCustomTable(object):
    """
    The custom table for Cost Analysis UI rendering.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SavedCustomTable object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this SavedCustomTable.
        :type display_name: str

        :param row_group_by:
            The value to assign to the row_group_by property of this SavedCustomTable.
        :type row_group_by: list[str]

        :param column_group_by:
            The value to assign to the column_group_by property of this SavedCustomTable.
        :type column_group_by: list[str]

        :param group_by_tag:
            The value to assign to the group_by_tag property of this SavedCustomTable.
        :type group_by_tag: list[oci.usage_api.models.Tag]

        :param compartment_depth:
            The value to assign to the compartment_depth property of this SavedCustomTable.
        :type compartment_depth: float

        :param version:
            The value to assign to the version property of this SavedCustomTable.
        :type version: float

        """
        self.swagger_types = {
            'display_name': 'str',
            'row_group_by': 'list[str]',
            'column_group_by': 'list[str]',
            'group_by_tag': 'list[Tag]',
            'compartment_depth': 'float',
            'version': 'float'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'row_group_by': 'rowGroupBy',
            'column_group_by': 'columnGroupBy',
            'group_by_tag': 'groupByTag',
            'compartment_depth': 'compartmentDepth',
            'version': 'version'
        }

        self._display_name = None
        self._row_group_by = None
        self._column_group_by = None
        self._group_by_tag = None
        self._compartment_depth = None
        self._version = None

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this SavedCustomTable.
        The name of the custom table.


        :return: The display_name of this SavedCustomTable.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this SavedCustomTable.
        The name of the custom table.


        :param display_name: The display_name of this SavedCustomTable.
        :type: str
        """
        self._display_name = display_name

    @property
    def row_group_by(self):
        """
        Gets the row_group_by of this SavedCustomTable.
        The row groupBy key list.
        example:
          `[\"tagNamespace\", \"tagKey\", \"tagValue\", \"service\", \"skuName\", \"skuPartNumber\", \"unit\",
            \"compartmentName\", \"compartmentPath\", \"compartmentId\", \"platform\", \"region\", \"logicalAd\",
            \"resourceId\", \"tenantId\", \"tenantName\"]`


        :return: The row_group_by of this SavedCustomTable.
        :rtype: list[str]
        """
        return self._row_group_by

    @row_group_by.setter
    def row_group_by(self, row_group_by):
        """
        Sets the row_group_by of this SavedCustomTable.
        The row groupBy key list.
        example:
          `[\"tagNamespace\", \"tagKey\", \"tagValue\", \"service\", \"skuName\", \"skuPartNumber\", \"unit\",
            \"compartmentName\", \"compartmentPath\", \"compartmentId\", \"platform\", \"region\", \"logicalAd\",
            \"resourceId\", \"tenantId\", \"tenantName\"]`


        :param row_group_by: The row_group_by of this SavedCustomTable.
        :type: list[str]
        """
        self._row_group_by = row_group_by

    @property
    def column_group_by(self):
        """
        Gets the column_group_by of this SavedCustomTable.
        The column groupBy key list.
        example:
          `[\"tagNamespace\", \"tagKey\", \"tagValue\", \"service\", \"skuName\", \"skuPartNumber\", \"unit\",
            \"compartmentName\", \"compartmentPath\", \"compartmentId\", \"platform\", \"region\", \"logicalAd\",
            \"resourceId\", \"tenantId\", \"tenantName\"]`


        :return: The column_group_by of this SavedCustomTable.
        :rtype: list[str]
        """
        return self._column_group_by

    @column_group_by.setter
    def column_group_by(self, column_group_by):
        """
        Sets the column_group_by of this SavedCustomTable.
        The column groupBy key list.
        example:
          `[\"tagNamespace\", \"tagKey\", \"tagValue\", \"service\", \"skuName\", \"skuPartNumber\", \"unit\",
            \"compartmentName\", \"compartmentPath\", \"compartmentId\", \"platform\", \"region\", \"logicalAd\",
            \"resourceId\", \"tenantId\", \"tenantName\"]`


        :param column_group_by: The column_group_by of this SavedCustomTable.
        :type: list[str]
        """
        self._column_group_by = column_group_by

    @property
    def group_by_tag(self):
        """
        Gets the group_by_tag of this SavedCustomTable.
        GroupBy a specific tagKey. Provide the tagNamespace and tagKey in the tag object. Only one tag in the list is supported.
        For example:
          `[{\"namespace\":\"oracle\", \"key\":\"createdBy\"]`


        :return: The group_by_tag of this SavedCustomTable.
        :rtype: list[oci.usage_api.models.Tag]
        """
        return self._group_by_tag

    @group_by_tag.setter
    def group_by_tag(self, group_by_tag):
        """
        Sets the group_by_tag of this SavedCustomTable.
        GroupBy a specific tagKey. Provide the tagNamespace and tagKey in the tag object. Only one tag in the list is supported.
        For example:
          `[{\"namespace\":\"oracle\", \"key\":\"createdBy\"]`


        :param group_by_tag: The group_by_tag of this SavedCustomTable.
        :type: list[oci.usage_api.models.Tag]
        """
        self._group_by_tag = group_by_tag

    @property
    def compartment_depth(self):
        """
        Gets the compartment_depth of this SavedCustomTable.
        The compartment depth level.


        :return: The compartment_depth of this SavedCustomTable.
        :rtype: float
        """
        return self._compartment_depth

    @compartment_depth.setter
    def compartment_depth(self, compartment_depth):
        """
        Sets the compartment_depth of this SavedCustomTable.
        The compartment depth level.


        :param compartment_depth: The compartment_depth of this SavedCustomTable.
        :type: float
        """
        self._compartment_depth = compartment_depth

    @property
    def version(self):
        """
        Gets the version of this SavedCustomTable.
        The version of the custom table.


        :return: The version of this SavedCustomTable.
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this SavedCustomTable.
        The version of the custom table.


        :param version: The version of this SavedCustomTable.
        :type: float
        """
        self._version = version

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
