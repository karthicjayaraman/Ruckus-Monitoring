window[appName].filter('highlight', function () {
    return function (text, search, caseSensitive) {
        if (text && (search || angular.isNumber(search))) {
            text = text.toString();
            search = search.toString();
            if (caseSensitive) {
                return text.split(search).join('<span class="ui-match">' + search + '</span>');
            } else {
                return text.replace(new RegExp(search, 'gi'), '<span class="ui-match">$&</span>');
            }
        } else {
            return text;
        }
    };
});


window[appName].controller('scg_dashboard_controller',function($rootScope,$scope,$state,$http,$window,$location,$q,$filter){
	
	$scope.pageChangeHandler = function(num) {
      console.log('meals page changed to ' + num);
  };
  
  
	
	
	$scope.currentPage = 1;
  	
	$scope.pageSize = 10;
    
	
	$scope.polling = {};
	
	$rootScope.closePopup = function() {
		
		$rootScope.showConfirm = false;
		
	}
	
	
	$scope.global_menu = function(id) {
		
		$rootScope.showConfirm = true;
		
	$scope.polling.menu = id;	
		
	}
	
	
	$scope.scg_info_box = false;
	
	$scope.hideBox = function () {
		
		$scope.scg_info_box = false;
		
	}

	$scope.scg_graph = {};
	
	$scope.scg_graph.menu = 'client_devices';
	
	
	$scope.navigate_scg_graph = function(menu_name) {
		
		$scope.scg_graph.menu = menu_name;
		
		if(menu_name=="client_devices") {
			
			//processTheData('get_client_device_data','{}');
		
			HttpRequest('get','get_client_device_data',window.flaskURL+'scg/get_client_device_data',''); 
		
		} else {
		
		HttpRequest('get','get_ap_device_data',window.flaskURL+'scg/get_ap_device_data',''); 
		
		
		}
		
		
	}
	
	


	
	function HttpRequest(method,action, URL, parameter) {
		
		$rootScope.showLoader = true;
		
        var $promise = '';
        if(method==="post") {
            $promise = $http.post(URL, parameter);
        } else {
            $promise = $http.get(URL, parameter);
        }
        $promise.then(function (response) {
            var result = angular.fromJson(response.data);
            processTheData(action, result);
			
			$rootScope.showLoader = false;
			
        });
    };


	 function processTheData(action, response) {
        
		switch (action) {
			
			 case 'get_ap_activities_full':
			 
			 $scope.users = response.items;
			 
			 break;
			
			 case 'get_devices':
			 
			 $scope.scg_devices = response;
			 
			 break;
			 
			 case 'get_ap_activities':
			 
			 $scope.ap_activities = response;
			 
			 break;
			 
			 case 'get_control_plane':
			 
			 $scope.scg_info_box = true;
			 
			 $scope.get_scg_data = response;
			 
			 break;
			 
			 case 'get_ap_device_data':
			 
			 $scope.data = response;
			 
			 $scope.clientChart = {
        	options: {
            chart: {
				width:920,
				zoomType: 'x',
				spacingRight:1   
            },
			plotOptions: {
            series: {}
        },
        	},
		xAxis: {
            type: 'datetime',
			title: {
						text: 'Date and Time'
			}
        },
		yAxis: {
			type: 'logarithmic',
			title: {
			text: 'AP Count'
		 },
		},
		plotOptions: {
			series: {
               cursor: 'pointer',
            },
			legend: {
          	  enabled: false
        	}
        },
		series: $scope.data,
        title: {
            text: 'Time vs AP Count'
        },
		credits: {
     	 enabled: false
    	}
    };	
	
	
			 
			 
			 break;
			
			 case 'get_client_device_data':
	 
			 $scope.data = response;
			 
			 $scope.clientChart = {
        	options: {
            chart: {
				width:920,
				zoomType: 'x',
				spacingRight:1   
            },
			plotOptions: {
            series: {}
        },
        	},
		xAxis: {
            type: 'datetime',
			title: {
						text: 'Date and Time'
			}
        },
		yAxis: {
			type: 'logarithmic',
			title: {
			text: 'ClientCount'
		 },
		},
		plotOptions: {
			series: {
               cursor: 'pointer',
            },
			legend: {
          	  enabled: false
        	}
        },
		series: $scope.data,
        title: {
            text: 'Time vs Client Count'
        },
		credits: {
     	 enabled: false
    	}
    };	
	
	
	
			 break;
			
		}
		
	 }
	 
	 $scope.selectSingleRow = function(rowIndex) {
		 
		 $scope.selectedRowId = rowIndex;
		 
		 
	 }
	 
	 $scope.get_control_plane = function(ip) {
		 
		 var param = {"scg_ip":ip}
		 
		HttpRequest('post','get_control_plane',window.flaskURL+'scg/get_control_plane',param); 
		 
	 }
	
	HttpRequest('get','get_devices',window.flaskURL+'scg/get_devices',''); 
	
	HttpRequest('get','get_ap_activities',window.flaskURL+'scg/get_ap_activities',''); 
	
	HttpRequest('get','get_client_device_data',window.flaskURL+'scg/get_client_device_data',''); 
	
	HttpRequest('get','get_ap_activities_full',window.flaskURL+'scg/get_ap_activities_full',''); 

});
