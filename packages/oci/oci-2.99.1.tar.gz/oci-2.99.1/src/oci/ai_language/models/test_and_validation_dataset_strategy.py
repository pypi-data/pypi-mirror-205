# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .test_strategy import TestStrategy
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TestAndValidationDatasetStrategy(TestStrategy):
    """
    This information will be used capture training, testing and validation dataset.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new TestAndValidationDatasetStrategy object with values from keyword arguments. The default value of the :py:attr:`~oci.ai_language.models.TestAndValidationDatasetStrategy.strategy_type` attribute
        of this class is ``TEST_AND_VALIDATION_DATASET`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param strategy_type:
            The value to assign to the strategy_type property of this TestAndValidationDatasetStrategy.
            Allowed values for this property are: "TEST_AND_VALIDATION_DATASET"
        :type strategy_type: str

        :param testing_dataset:
            The value to assign to the testing_dataset property of this TestAndValidationDatasetStrategy.
        :type testing_dataset: oci.ai_language.models.DatasetDetails

        :param validation_dataset:
            The value to assign to the validation_dataset property of this TestAndValidationDatasetStrategy.
        :type validation_dataset: oci.ai_language.models.DatasetDetails

        """
        self.swagger_types = {
            'strategy_type': 'str',
            'testing_dataset': 'DatasetDetails',
            'validation_dataset': 'DatasetDetails'
        }

        self.attribute_map = {
            'strategy_type': 'strategyType',
            'testing_dataset': 'testingDataset',
            'validation_dataset': 'validationDataset'
        }

        self._strategy_type = None
        self._testing_dataset = None
        self._validation_dataset = None
        self._strategy_type = 'TEST_AND_VALIDATION_DATASET'

    @property
    def testing_dataset(self):
        """
        **[Required]** Gets the testing_dataset of this TestAndValidationDatasetStrategy.

        :return: The testing_dataset of this TestAndValidationDatasetStrategy.
        :rtype: oci.ai_language.models.DatasetDetails
        """
        return self._testing_dataset

    @testing_dataset.setter
    def testing_dataset(self, testing_dataset):
        """
        Sets the testing_dataset of this TestAndValidationDatasetStrategy.

        :param testing_dataset: The testing_dataset of this TestAndValidationDatasetStrategy.
        :type: oci.ai_language.models.DatasetDetails
        """
        self._testing_dataset = testing_dataset

    @property
    def validation_dataset(self):
        """
        Gets the validation_dataset of this TestAndValidationDatasetStrategy.

        :return: The validation_dataset of this TestAndValidationDatasetStrategy.
        :rtype: oci.ai_language.models.DatasetDetails
        """
        return self._validation_dataset

    @validation_dataset.setter
    def validation_dataset(self, validation_dataset):
        """
        Sets the validation_dataset of this TestAndValidationDatasetStrategy.

        :param validation_dataset: The validation_dataset of this TestAndValidationDatasetStrategy.
        :type: oci.ai_language.models.DatasetDetails
        """
        self._validation_dataset = validation_dataset

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
