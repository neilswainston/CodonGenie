resultApp.directive("resultPanel", function() {
    return {
    	scope: {
    		"results": "&",
    	},
        templateUrl: "/static/result/result.html"
    };
});