codonGenieApp.controller("codonGenieCtrl", ["$scope", "$http", "$log", function($scope, $http, $log) {
	var self = this;
	self.isCalculating = false;
	self.aminoAcids = null;
	self.codons = null;
	
	self.getCodons = function() {
		if(self.aminoAcids) {
			self.isCalculating = true;
			$http.get("/codons/" + self.aminoAcids).then(
					function(resp) {
						self.codons = resp.data;
						self.isCalculating = false;
					},
					function(errResp) {
						$log.error(errResp.data.message);
						self.isCalculating = false;
					});
		}
	};
}]);