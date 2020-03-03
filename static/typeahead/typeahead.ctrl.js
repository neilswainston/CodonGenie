typeaheadApp.controller("typeaheadCtrl", function($http) {
	var self = this;
	self.url = null;
	
	self.getItem = function(val) {
		return $http.get(self.url + val).then(function(resp) {
			return resp.data.map(function(item) {
				return item;
			});
		});
	};
});