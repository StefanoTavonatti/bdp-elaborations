# SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import absolute_import, annotations

import logging
from typing import List

from common.cache.common import TrafficManagerClass
from common.connector.common import ODHBaseConnector
from common.data_model.validation import ValidationMeasure, ValidationMeasureCollection, ValidationEntry
from common.manager.traffic_station import TrafficStationManager
from common.data_model.common import DataType, MeasureCollection
from common.model.model import GenericModel
from validator.model.validation_model import ValidationModel

logger = logging.getLogger("pollution_v2.validator.manager.validation")


class ValidationManager(TrafficStationManager):
    """
    Manager in charge of executing validation.
    """

    def _get_manager_code(self) -> str:
        return TrafficManagerClass.VALIDATION.name

    def _get_model(self) -> GenericModel:
        return ValidationModel()

    def get_data_collector(self) -> ODHBaseConnector:
        return self._connector_collector.validation

    def get_date_reference_collector(self) -> ODHBaseConnector:
        return self._connector_collector.traffic

    def _get_data_types(self) -> List[DataType]:
        return ValidationMeasure.get_data_types()

    def _build_from_entries(self, input_entries: List[ValidationEntry]) -> MeasureCollection:
        return ValidationMeasureCollection.build_from_validation_entries(input_entries, self._provenance)