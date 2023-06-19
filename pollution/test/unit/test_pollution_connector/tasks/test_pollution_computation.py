# SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import absolute_import, annotations

import datetime
from unittest import TestCase
from unittest.mock import patch, Mock

from pollution_connector.data_model.common import Provenance, DataType
from pollution_connector.data_model.pollution import PollutionMeasure
from pollution_connector.settings import DEFAULT_TIMEZONE
from pollution_connector.tasks.pollution_computation import PollutionComputationManager
from test.unit.test_pollution_connector.connector.mock_collector import MockConnectorCollector
from test.unit.test_pollution_connector.data_model.generator import Generator


class TestPollutionComputationManager(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.station = Generator.generate_traffic_station(code="A22:678:1")
        self.station1 = Generator.generate_traffic_station()
        self.traffic_measure = Generator.generate_traffic_measure(station=self.station)
        self.traffic_measure1 = Generator.generate_traffic_measure(station=self.station1)
        self.mock_connector_collector = MockConnectorCollector.build()
        self.pollution_computation_manager = PollutionComputationManager(self.mock_connector_collector, Provenance("id", "lineage", "name", "version"))

    def test_run_computation_and_upload_results(self):
        with patch("pollution_connector.tasks.pollution_computation.PollutionComputationManager._get_station_list") as station_list_mock:
            station_list_mock.return_value = [self.station]
            with patch("pollution_connector.tasks.pollution_computation.PollutionComputationManager._get_latest_pollution_measure") as latest_pollution_measure_mock:
                latest_pollution_measure_mock.return_value = None
                with patch("pollution_connector.tasks.pollution_computation.PollutionComputationManager._upload_pollution_data") as upload_pollution_data_mock:
                    upload_pollution_data_mock.return_value = None
                    valid_time = datetime.datetime.now()
                    traffic_measure = Generator.generate_traffic_measure(station=self.station, valid_time=valid_time, data_type=DataType(name="Average Speed Buses", description="", data_type="Mean", unit="km/h", metadata={}))
                    traffic_measure1 = Generator.generate_traffic_measure(station=self.station, valid_time=valid_time, data_type=DataType(name="Nr. Buses", description="", data_type="Mean", unit="", metadata={}))
                    self.mock_connector_collector.traffic.get_measures = Mock(return_value=[traffic_measure1, traffic_measure])
                    self.pollution_computation_manager.run_computation_and_upload_results(min_from_date=datetime.datetime(2020, 1, 1),
                                                                                          max_to_date=datetime.datetime(2020, 1, 2))
                    station_list_mock.assert_called_once()
                    latest_pollution_measure_mock.assert_called_once_with(self.station)
                    upload_pollution_data_mock.assert_called_once()
                    self.mock_connector_collector.traffic.get_measures.assert_called_once_with(from_date=DEFAULT_TIMEZONE.localize(datetime.datetime(2020, 1, 1)), to_date=DEFAULT_TIMEZONE.localize(datetime.datetime(2020, 1, 2)), station=self.station)

    def test_run_computation_and_upload_results_with_measure(self):
        with patch("pollution_connector.tasks.pollution_computation.PollutionComputationManager._get_station_list") as station_list_mock:
            station_list_mock.return_value = [self.station]
            with patch("pollution_connector.tasks.pollution_computation.PollutionComputationManager._get_latest_pollution_measure") as latest_pollution_measure_mock:
                latest_pollution_measure_mock.return_value = PollutionMeasure(station=self.station,
                                                                              data_type=self.traffic_measure.data_type,
                                                                              provenance=self.traffic_measure.provenance,
                                                                              valid_time=DEFAULT_TIMEZONE.localize(datetime.datetime(2020, 1, 1, hour=1, minute=1)),
                                                                              transaction_time=DEFAULT_TIMEZONE.localize(datetime.datetime(2020, 1, 1, hour=1, minute=1)),
                                                                              value=3,
                                                                              period=self.traffic_measure.period)
                with patch("pollution_connector.tasks.pollution_computation.PollutionComputationManager._upload_pollution_data") as upload_pollution_data_mock:
                    upload_pollution_data_mock.return_value = None
                    valid_time = datetime.datetime.now()
                    traffic_measure = Generator.generate_traffic_measure(station=self.station, valid_time=valid_time, data_type=DataType(name="Average Speed Buses", description="", data_type="Mean", unit="km/h", metadata={}))
                    traffic_measure1 = Generator.generate_traffic_measure(station=self.station, valid_time=valid_time, data_type=DataType(name="Nr. Buses", description="", data_type="Mean", unit="", metadata={}))
                    self.mock_connector_collector.traffic.get_measures = Mock(return_value=[traffic_measure1, traffic_measure])
                    self.pollution_computation_manager.run_computation_and_upload_results(min_from_date=datetime.datetime(2020, 1, 1),
                                                                                          max_to_date=datetime.datetime(2020, 1, 2))
                    station_list_mock.assert_called_once()
                    latest_pollution_measure_mock.assert_called_once_with(self.station)
                    upload_pollution_data_mock.assert_called_once()
                    self.mock_connector_collector.traffic.get_measures.assert_called_once_with(from_date=DEFAULT_TIMEZONE.localize(datetime.datetime(2020, 1, 1, hour=1, minute=1)), to_date=DEFAULT_TIMEZONE.localize(datetime.datetime(2020, 1, 2)), station=self.station)
