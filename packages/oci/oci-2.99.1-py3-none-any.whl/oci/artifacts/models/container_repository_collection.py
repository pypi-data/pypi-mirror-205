# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ContainerRepositoryCollection(object):
    """
    List of container repository results.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ContainerRepositoryCollection object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param layer_count:
            The value to assign to the layer_count property of this ContainerRepositoryCollection.
        :type layer_count: int

        :param layers_size_in_bytes:
            The value to assign to the layers_size_in_bytes property of this ContainerRepositoryCollection.
        :type layers_size_in_bytes: int

        :param image_count:
            The value to assign to the image_count property of this ContainerRepositoryCollection.
        :type image_count: int

        :param items:
            The value to assign to the items property of this ContainerRepositoryCollection.
        :type items: list[oci.artifacts.models.ContainerRepositorySummary]

        :param remaining_items_count:
            The value to assign to the remaining_items_count property of this ContainerRepositoryCollection.
        :type remaining_items_count: int

        :param repository_count:
            The value to assign to the repository_count property of this ContainerRepositoryCollection.
        :type repository_count: int

        """
        self.swagger_types = {
            'layer_count': 'int',
            'layers_size_in_bytes': 'int',
            'image_count': 'int',
            'items': 'list[ContainerRepositorySummary]',
            'remaining_items_count': 'int',
            'repository_count': 'int'
        }

        self.attribute_map = {
            'layer_count': 'layerCount',
            'layers_size_in_bytes': 'layersSizeInBytes',
            'image_count': 'imageCount',
            'items': 'items',
            'remaining_items_count': 'remainingItemsCount',
            'repository_count': 'repositoryCount'
        }

        self._layer_count = None
        self._layers_size_in_bytes = None
        self._image_count = None
        self._items = None
        self._remaining_items_count = None
        self._repository_count = None

    @property
    def layer_count(self):
        """
        **[Required]** Gets the layer_count of this ContainerRepositoryCollection.
        Total number of layers.


        :return: The layer_count of this ContainerRepositoryCollection.
        :rtype: int
        """
        return self._layer_count

    @layer_count.setter
    def layer_count(self, layer_count):
        """
        Sets the layer_count of this ContainerRepositoryCollection.
        Total number of layers.


        :param layer_count: The layer_count of this ContainerRepositoryCollection.
        :type: int
        """
        self._layer_count = layer_count

    @property
    def layers_size_in_bytes(self):
        """
        **[Required]** Gets the layers_size_in_bytes of this ContainerRepositoryCollection.
        Total storage in bytes consumed by layers.


        :return: The layers_size_in_bytes of this ContainerRepositoryCollection.
        :rtype: int
        """
        return self._layers_size_in_bytes

    @layers_size_in_bytes.setter
    def layers_size_in_bytes(self, layers_size_in_bytes):
        """
        Sets the layers_size_in_bytes of this ContainerRepositoryCollection.
        Total storage in bytes consumed by layers.


        :param layers_size_in_bytes: The layers_size_in_bytes of this ContainerRepositoryCollection.
        :type: int
        """
        self._layers_size_in_bytes = layers_size_in_bytes

    @property
    def image_count(self):
        """
        **[Required]** Gets the image_count of this ContainerRepositoryCollection.
        Total number of images.


        :return: The image_count of this ContainerRepositoryCollection.
        :rtype: int
        """
        return self._image_count

    @image_count.setter
    def image_count(self, image_count):
        """
        Sets the image_count of this ContainerRepositoryCollection.
        Total number of images.


        :param image_count: The image_count of this ContainerRepositoryCollection.
        :type: int
        """
        self._image_count = image_count

    @property
    def items(self):
        """
        **[Required]** Gets the items of this ContainerRepositoryCollection.
        Collection of container repositories.


        :return: The items of this ContainerRepositoryCollection.
        :rtype: list[oci.artifacts.models.ContainerRepositorySummary]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this ContainerRepositoryCollection.
        Collection of container repositories.


        :param items: The items of this ContainerRepositoryCollection.
        :type: list[oci.artifacts.models.ContainerRepositorySummary]
        """
        self._items = items

    @property
    def remaining_items_count(self):
        """
        **[Required]** Gets the remaining_items_count of this ContainerRepositoryCollection.
        Estimated number of remaining results.


        :return: The remaining_items_count of this ContainerRepositoryCollection.
        :rtype: int
        """
        return self._remaining_items_count

    @remaining_items_count.setter
    def remaining_items_count(self, remaining_items_count):
        """
        Sets the remaining_items_count of this ContainerRepositoryCollection.
        Estimated number of remaining results.


        :param remaining_items_count: The remaining_items_count of this ContainerRepositoryCollection.
        :type: int
        """
        self._remaining_items_count = remaining_items_count

    @property
    def repository_count(self):
        """
        **[Required]** Gets the repository_count of this ContainerRepositoryCollection.
        Total number of repositories.


        :return: The repository_count of this ContainerRepositoryCollection.
        :rtype: int
        """
        return self._repository_count

    @repository_count.setter
    def repository_count(self, repository_count):
        """
        Sets the repository_count of this ContainerRepositoryCollection.
        Total number of repositories.


        :param repository_count: The repository_count of this ContainerRepositoryCollection.
        :type: int
        """
        self._repository_count = repository_count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
