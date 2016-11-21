resultApp.directive("resultPanel", function() {
    return {
    	scope: {
    		"results": "&",
    	},
        templateUrl: "/static/result/result.html",
        link: function(scope, element, attrs) {
        	scope.toString = function(array) {
            	var len = array.length;
        		var formatted = [array.length];
        		
        		for(var i = 0; i < len; i++) {
        			formatted[i] = array[i][0] + " (" + array[i][1].toFixed(2) + ")";
        		}
        		
        		return formatted.join(", ");
            };
        }
    };
});