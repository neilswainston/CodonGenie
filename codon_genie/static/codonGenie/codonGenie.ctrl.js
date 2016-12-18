codonGenieApp.controller("codonGenieCtrl", ["$scope", "$http", "$log", "ErrorService", function($scope, $http, $log, ErrorService) {
	var self = this;
	self.isCalculating = false;
	self.query = {"mode": "aminoAcids", "aminoAcids": [], "codon": ""};
	self.codon_pattern = "[acgtmrwsykvhdbnACGTMRWSYKVHDBN]{3}";
	
	var results = null;
	
	self.toggle = function(aminoAcid) {
		if(self.query.aminoAcids.includes(aminoAcid)) {
			for(var i = self.query.aminoAcids.length - 1; i >= 0; i--) {
			    if(self.query.aminoAcids[i] === aminoAcid) {
			    	self.query.aminoAcids.splice(i, 1);
			    }
			}
		}
		else {
			self.query.aminoAcids.push(aminoAcid)
		}
	}
	
	self.submit = function() {
		results = null;
		
		if(self.query["organism"]) {
			self.isCalculating = true;
			var params = null;
			
			if(self.query.mode == "aminoAcids") {
				if(self.query.aminoAcids.length) {
					params = {"aminoAcids": self.query.aminoAcids.join(""),
						"organism": self.query["organism"]["id"]}
				}
			}
			else {
				if(self.query.codon && self.query.codon.length == 3) {
					params = {"codon": self.query.codon,
						"organism": self.query["organism"]["id"]}
				}
			}
			
			if(params) {
				$http.get("codons", {params: params}).then(
						function(resp) {
							results = resp.data;
							self.isCalculating = false;
						},
						function(errResp) {
							$log.error(errResp.data.message);
							ErrorService.open(errResp.data.message);
							self.isCalculating = false;
						});
			}
			else {
				self.isCalculating = false;
			}
		}
	};
	
	self.results = function() {
		return results;
	};
	
	$scope.$watch(function() {
		return self.query;
	},               
	function(values) {
		self.submit();
	}, true);
}]);