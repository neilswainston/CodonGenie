codonGenieApp.controller("codonGenieCtrl", ["$scope", "$http", "$log", "ErrorService", function($scope, $http, $log, ErrorService) {
	var self = this;
	self.isCalculating = false;
	self.query = {};
	self.aa_pattern = "[qwertyipasdfghklcvnmQWERTYIPASDFGHKLCVNM]*";
	self.codons = null;
	
	self.submit = function() {
		self.isCalculating = true;
		self.codons = null;
		self.query.aminoAcids = self.query.aminoAcids.toUpperCase();
		
		$http.post("/codons/", self.query).then(
				function(resp) {
					self.codons = resp.data;
					self.isCalculating = false;
				},
				function(errResp) {
					$log.error(errResp.data.message);
					ErrorService.open(errResp.data.message);
					self.isCalculating = false;
				});
	};
	
	self.getCodonString = function(codon) {
		return "[" + codon.join("][") + "]";
	};
	
	self.toString = function(array) {
		var len = array.length;
		var formatted = [array.length];
		
		for(var i = 0; i < len; i++) {
			formatted[i] = array[i][0] + " (" + array[i][1].toFixed(2) + ")";
		}
		
		return formatted.join(", ");
	};
	
	$scope.$watch(function() {
		return self.query;
	},               
	function(values) {
		self.codons = null;
	}, true);
}]);