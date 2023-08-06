# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class EntityTagCollection(object):
    """
    Results of an entity tags listing. Entity tags allow assciation of business terms with entities.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new EntityTagCollection object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param count:
            The value to assign to the count property of this EntityTagCollection.
        :type count: int

        :param items:
            The value to assign to the items property of this EntityTagCollection.
        :type items: list[oci.data_catalog.models.EntityTagSummary]

        """
        self.swagger_types = {
            'count': 'int',
            'items': 'list[EntityTagSummary]'
        }

        self.attribute_map = {
            'count': 'count',
            'items': 'items'
        }

        self._count = None
        self._items = None

    @property
    def count(self):
        """
        Gets the count of this EntityTagCollection.
        Total number of items returned.


        :return: The count of this EntityTagCollection.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """
        Sets the count of this EntityTagCollection.
        Total number of items returned.


        :param count: The count of this EntityTagCollection.
        :type: int
        """
        self._count = count

    @property
    def items(self):
        """
        **[Required]** Gets the items of this EntityTagCollection.
        Collection of entity tags.


        :return: The items of this EntityTagCollection.
        :rtype: list[oci.data_catalog.models.EntityTagSummary]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this EntityTagCollection.
        Collection of entity tags.


        :param items: The items of this EntityTagCollection.
        :type: list[oci.data_catalog.models.EntityTagSummary]
        """
        self._items = items

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
