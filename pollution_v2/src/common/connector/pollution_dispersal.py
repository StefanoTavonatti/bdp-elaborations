# SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import absolute_import, annotations

from typing import Optional, List

from common.connector.common import ODHBaseConnector
from common.data_model import PollutionDispersalMeasure, Station
from common.settings import PERIOD_1HOUR


class PollutionDispersalODHConnector(ODHBaseConnector[PollutionDispersalMeasure, Station]):

    def __init__(self,
                 base_reader_url: str,
                 base_writer_url: str,
                 authentication_url: str,
                 username: Optional[str],
                 password: Optional[str],
                 client_id: Optional[str],
                 client_secret: Optional[str],
                 grant_type: List[str],
                 pagination_size: int,
                 max_post_batch_size: Optional[int],
                 requests_timeout: float,
                 requests_max_retries: int,
                 requests_sleep_time: float,
                 requests_retry_sleep_time: float) -> None:

        self.station_type = "EnvironmentStation"
        measure_types = list(map(str, PollutionDispersalMeasure.get_data_types()))
        period = PERIOD_1HOUR


        super().__init__(base_reader_url,
                         base_writer_url,
                         self.station_type,
                         measure_types,
                         authentication_url,
                         username,
                         password,
                         client_id,
                         client_secret,
                         grant_type,
                         pagination_size,
                         max_post_batch_size,
                         requests_timeout,
                         requests_max_retries,
                         requests_sleep_time,
                         requests_retry_sleep_time,
                         period)

    @staticmethod
    def build_station(raw_station: dict) -> Station:
        return Station.from_odh_repr(raw_station)

    @staticmethod
    def build_measure(raw_measure: dict) -> PollutionDispersalMeasure:
        return PollutionDispersalMeasure.from_odh_repr(raw_measure)
