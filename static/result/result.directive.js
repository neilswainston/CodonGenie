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
        			formatted[i] = array[i]['codon'] + " (" + array[i]['probability'].toFixed(2) + ")";
        		}
        		
        		return formatted.join(", ");
            };
            
            scope.toCodonString = function(array) {
            	return "[" + array.join("|") + "]";
            };
        }
    };
});