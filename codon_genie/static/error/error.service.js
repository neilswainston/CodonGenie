errorApp.factory("ErrorService", ["$uibModal", function($uibModal) {
	var obj = {};

	obj.open = function(error) {
		$uibModal.open({
			animation: true,
			ariaLabelledBy: 'modal-title',
			ariaDescribedBy: 'modal-body',
			templateUrl: '/static/error/errorContent.html',
			controller: 'errorInstanceCtrl',
			controllerAs: 'errorCtrl',
			resolve: {
				error: function() {
					return error;
				}
			}
		});
	};
	
	return obj;
}]);