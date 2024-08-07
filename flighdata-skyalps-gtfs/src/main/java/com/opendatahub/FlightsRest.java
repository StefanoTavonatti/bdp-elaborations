// SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>
//
// SPDX-License-Identifier: AGPL-3.0-or-later

package com.opendatahub;

import java.util.Arrays;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.client.RestTemplate;

import com.opendatahub.dto.Flights;

@Service
public class FlightsRest {
	@Value("${odh.base.url}")
	private String baseUrl; 

	private final String GET_FLIGHTS = "/v2/flat,node/Flight?limit=-1&where=sactive.eq.true";
	private final Logger LOG = LoggerFactory.getLogger(FlightsRest.class);

	@RequestMapping(value = "/getFlights", method = RequestMethod.POST)
	@ResponseBody
	public Flights getFlights(RestTemplate restTemplate) throws Exception {
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.APPLICATION_JSON);
		headers.setAccept(Arrays.asList(MediaType.ALL)); /* Collections.singletonList(MediaType.APPLICATION_JSON) */

		String url = baseUrl + GET_FLIGHTS;
		ResponseEntity<Flights> response = restTemplate.getForEntity(url, Flights.class);
		LOG.debug(response.getBody().toString());

		if (response.getStatusCode() == HttpStatus.OK) {
			LOG.info("Request Successful {}", url);
			return response.getBody();
		} else {
			throw new Exception("Request failed with status code " + response.getStatusCode());
		}
	}
}
