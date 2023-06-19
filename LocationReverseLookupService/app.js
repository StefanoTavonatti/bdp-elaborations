// SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>
//
// SPDX-License-Identifier: AGPL-3.0-or-later

const endpointUrl = process.env.odhEndpoint;
const stationsUrl = endpointUrl+"/stationsWithoutMunicipality";
const sendUrl = endpointUrl+"/patchStations";
const logger = require('winston');
logger.level='info';
const osmReverseLookupUrl = "http://nominatim.openstreetmap.org/reverse";
var request = require("request")
exports.handler = (event, context, callback) => {
    var data = init();
    callback(null, data);
};
exports.getInputData = function(){
	return new Promise(function(resolve,reject){
		request.get({
			url: stationsUrl,
		    	json: true
		}, function (error, response, body) {
			logger.debug(body);
    			if (!error && response.statusCode === 200)
				      resolve(body);
		    	else
				      reject(error);
		});
	});
}
var getTownNameByCoordinate = function(longitude,latitude){
	return new Promise(function(resolve, reject){
		if (!longitude || !latitude)
			reject("required request parameters not provided");
		request.get({
    			url: osmReverseLookupUrl,
			headers:{
				referer:'NOI-Techpark'
			},
		    	json: true,
			qs:{
				format: "jsonv2",
				lon: longitude,
				lat: latitude
			}
		}, function (error, response, body) {
	 		if (!error && response.statusCode === 200)
				resolve(body);
	    		else
				reject(error);
		});

	});
}
var send = function(mappings){
	request.post({
		url:sendUrl,
		json:true,
		body:mappings
	},function(error,response,body){
		if (!error && response.statusCode === 200)
			logger.debug("Data sent");
	    	else
			logger.debug("post failed with error" + error);
	});
}
function init(){
	exports.getInputData().then(function(stations){
    var totalLength = stations.length;
    logger.info("Retrieved " + totalLength + " objects");
    logger.info("Start to retrieve municipality of objects");
		var objWithCoordinates = [];
		recursiveRetrival();
		function recursiveRetrival(){
      logger.info("Found "+ (totalLength-stations.length+1) +" of " + totalLength);
			if (stations.length === 0)
				return ;
			var station = stations.pop();
			getTownNameByCoordinate(station.longitude, station.latitude)
			.then(function(jR){
				var address = jR.address;
        if (address){
						logger.info("About to send an object");
				    send([{municipality:address.city||address.town||address.village||address.hamlet,id:station.id,"_t":"it.bz.idm.bdp.dto.StationDto",stationType:station.stationType}]);
				}
        else {
            logger.info("Could not get address info of object with id" + station.id);
        }
			}).then(function(){
				setTimeout(recursiveRetrival,1000);
			}).catch(function(err){console.log(err);setTimeout(recursiveRetrival,1000)});
		}
	}).catch(err => console.log(err));
}


init();
