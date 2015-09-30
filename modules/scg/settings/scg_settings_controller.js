window[appName].controller('scg_settings_controller',function($scope,$state,$http,$window){
	
	$scope.innerAccordion = {};
	
	$scope.innerAccordion.activeSection = 'email';
	
	$scope.navigateAccordion = function(sectionName) {
		
		$scope.innerAccordion.activeSection = sectionName;
		
	}
	
	  
	
	console.log("am inside");

});
