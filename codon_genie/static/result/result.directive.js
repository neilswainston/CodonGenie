resultApp.directive("resultPanel", function() {
    return {
    	scope: {
    		"results": "&",
    		"toString": "&",
    	},
        templateUrl: "/static/result/result.html"
    };
});