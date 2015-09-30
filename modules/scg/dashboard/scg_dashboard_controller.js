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


window[appName].controller('ThirdController',function($rootScope,$scope,$state,$http,$window,$location,$q,$filter){
	
	$scope.pageChanged = function(page) {
		
		$scope.pagination.current = page;
		
		$scope.ap_param = {"page":$scope.pagination.current,"timestamp":$scope.timestamp,"scg_name":$scope.scg_name,"scg_log":$scope.scg_log,"limit":$scope.usersPerPage};
		
		HttpRequest('post','get_critical_activities',window.flaskURL+'scg/get_critical_activities',$scope.ca_param); 	
		
	
		
	}
	
});



window[appName].controller('scg_dashboard_controller',function($rootScope,$scope,$state,$http,$window,$location,$q,$filter){
	
	
	var toUTCDate = function(date){
    var _utc = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),  date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds());
    return _utc;
  };
  
  $scope.millisToUTCDate = function(millis){
    return toUTCDate(new Date(millis));
  };
  
  
  $scope.tunnel_graph = false;
  
  $scope.scg_graph = {};
	
  $scope.scg_graph.menu = 'client_devices';
	
  $scope.timestamp = "";
  
  $scope.scg_name = "";
  
  $scope.scg_log = "";
	
	
	$scope.config = {};
	
	$scope.ap_activities = [];
	
	$scope.showSearch = false;
	
	$scope.showActionButtons = function() {
	
		console.log("Am Changed");	
		
	}
	
	$scope.customfunction = function() {
		
		$scope.config.hasSearch = true;
		
	}
	
	$scope.cancelSearch = function() {

		$scope.showSearch = false;
		
		$scope.config.hasSearch = false;
		
		$scope.timestamp = "";
		
		$scope.scg_name = "";
		
		$scope.scg_log = ""; 

		
	}

  
	$scope.get_tunnel_graph = function(scg_ip) {
		
		
		
		var tunnel = {"scg_ip":scg_ip};
		
		
		HttpRequest('post','get_tunnel_graph_data',window.flaskURL+'scg/get_tunnel_graph_data',tunnel); 

		
	}
	
	
	$scope.clearSearch = function() {
		
		$scope.showSearch = false;
		
		$scope.config.hasSearch = false;
		
		$scope.timestamp = "";
		
		$scope.scg_name = "";
		
		$scope.scg_log = ""; 
		
		
	}
	
	$scope.ap_search = function() {
		
		$scope.showSearch = !$scope.showSearch;
		
		$scope.config.hasSearch = false;
		
		
	}
	

	$scope.totalUsers = 0;
    
	$scope.usersPerPage = 10; 
	
    $scope.pagination = {current: 1};
	
	
	$scope.ca_pagination = {current: 1};

	
	
	$scope.polling = {};
	
	
	$scope.polling.graph = 7;
	
	$rootScope.closePopup = function() {
		
		$rootScope.showConfirm = false;
		
	}
	
	
	$scope.graph_polling = function(id) {
		
		var graph_param = {"days":id};
		
		if($scope.scg_graph.menu=="client_devices") {
			
			HttpRequest('post','get_client_device_data',window.flaskURL+'scg/get_client_device_data',graph_param); 
		
		
		
		} else {
		
		
		HttpRequest('post','get_ap_device_data',window.flaskURL+'scg/get_ap_device_data',graph_param); 
		
		}
		
		$scope.polling.graph = id;	
		
		
	}
	
	
	$scope.global_menu = function(id) {
		
		$rootScope.showConfirm = true;
		
	$scope.polling.menu = id;	
		
	}
	
	
	$scope.scg_info_box = false;
	
	$scope.hideBox = function () {
		
		$scope.scg_info_box = false;
		
	}

	
	
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
			
			
			case 'get_tunnel_graph_data':
			
			$scope.tunnel_data = response;
			
			alert($scope.tunnel_data.toSource());
			
			break;
			
			
			case 'global_config':
			
			$scope.global_config = response;
			
			break;
			
			 case 'get_ap_activities_full':
			 
			 $scope.users = response.items;
			 
			 break;
			
			 case 'get_devices':
			 
			 $scope.scg_devices = response;
			 
			 break;
			 
			 case 'get_ap_activities':
			 
			 $scope.ap_activities = response.items;
			  
              
			  $scope.totalUsers = response.filter_count;
			 
			 
			 break;
			 
			 
			 case 'get_critical_activities':
			 
			 
			  $scope.ca_activities = response.items;
			  
              
			  $scope.ca_items = response.filter_count;
			 
			 
			 
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
	 
	 
	 
	 
 	$scope.ap_param = {"page":$scope.pagination.current,"timestamp":$scope.timestamp,"scg_name":$scope.scg_name,"scg_log":$scope.scg_log,"limit":$scope.usersPerPage};
	
	
	$scope.ca_param = {"page":$scope.ca_pagination.current,"timestamp":$scope.timestamp,"scg_name":$scope.scg_name,"scg_log":$scope.scg_log,"limit":$scope.usersPerPage};
	
	
	$scope.CA_pageChanged = function(page) {
		
		
		$scope.ca_pagination.current = page;
		
		$scope.ca_param = {"page":$scope.ca_pagination.current,"timestamp":$scope.timestamp,"scg_name":$scope.scg_name,"scg_log":$scope.scg_log,"limit":$scope.usersPerPage};
		
		HttpRequest('post','get_ap_activities',window.flaskURL+'scg/get_ap_activities',$scope.ca_param); 
		
		
	}
	
	
	$scope.pageChanged = function(page) {
		
		
		$scope.pagination.current = page;
		
		$scope.ap_param = {"page":$scope.pagination.current,"timestamp":$scope.timestamp,"scg_name":$scope.scg_name,"scg_log":$scope.scg_log,"limit":$scope.usersPerPage};
		
		HttpRequest('post','get_critical_activities',window.flaskURL+'scg/get_critical_activities',$scope.ca_param); 	
		
	
		
	}
	
	
	
	
	$scope.ap_runSearch = function() {
		
		$scope.config.hasSearch = false;
		
		$scope.ap_param = {"page":$scope.pagination.current,"timestamp":$scope.timestamp,"scg_name":$scope.scg_name,"scg_log":$scope.scg_log,"limit":$scope.usersPerPage};
		
		HttpRequest('post','get_ap_activities',window.flaskURL+'scg/get_ap_activities',$scope.ap_param); 
		
		
	}
	
	
	HttpRequest('get','global_config',window.flaskURL+'scg/global_config',''); 
	
	HttpRequest('get','get_client_device_data',window.flaskURL+'scg/get_client_device_data',''); 
	
	HttpRequest('get','get_devices',window.flaskURL+'scg/get_devices',''); 
	
	HttpRequest('post','get_critical_activities',window.flaskURL+'scg/get_critical_activities',$scope.ca_param); 	
	
	HttpRequest('post','get_ap_activities',window.flaskURL+'scg/get_ap_activities',$scope.ap_param); 
	
	
	
	//HttpRequest('get','get_ap_activities_full',window.flaskURL+'scg/get_ap_activities_full',''); 
	
	

});
