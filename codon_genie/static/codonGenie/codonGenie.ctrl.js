codonGenieApp.controller("codonGenieCtrl", ["$scope", "$http", "$log", function($scope, $http, $log) {
	var self = this;
	self.isCalculating = false;
	self.query = {};
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
					self.isCalculating = false;
				});
	};
	
	self.getCodonString = function(codon) {
		return "[" + codon.join("][") + "]";
	};
	
	self.toString = function(array) {
		return array.join();
	};
	
	$scope.$watch(function() {
		return self.query;
	},               
	function(values) {
		self.codons = null;
	}, true);
}]);