// SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>
//
// SPDX-License-Identifier: AGPL-3.0-or-later

package it.bz.odh.elaborations.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

import it.bz.idm.bdp.dto.DataMapDto;
import it.bz.idm.bdp.dto.ProvenanceDto;
import it.bz.idm.bdp.dto.RecordDtoImpl;
import it.bz.idm.bdp.json.NonBlockingJSONPusher;

@Lazy
@Component
public class ODHWriterClient extends NonBlockingJSONPusher{

	@Value(value="${stationtype}")
	private String stationtype;


	@Value("${provenance_name}")
	private String provenanceName;
	@Value("${provenance_version}")
	private String provenanceVersion;
	
    @Value("${origin}")
    private String origin;

	@Override
	public String initIntegreenTypology() {
		return stationtype;
	}

	@Override
	public ProvenanceDto defineProvenance() {
		return new ProvenanceDto(null, provenanceName, provenanceVersion, origin);
	}

	@Override
	public <T> DataMapDto<RecordDtoImpl> mapData(T arg0) {
		// TODO Auto-generated method stub
		return null;
	}
}
