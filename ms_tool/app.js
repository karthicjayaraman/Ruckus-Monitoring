window.appName = 'Ruckus_Wireless';

window[appName] = angular.module(appName, ['ui.router','ngValidator','highcharts-ng','ngSanitize','angularUtils.directives.dirPagination']);

window.flaskURL = 'https://14.141.47.12:5000/';

window[appName].directive(
    "jgSlide",
    function () {

        function link($scope, element, attributes) {
			
            var expression, duration;
            expression = attributes.jgSlide;
            duration = (attributes.slideDuration || "fast");
            var isScrollable = ((attributes.jgSlideScroll != null) || (attributes.jgSlideScroll != undefined))  ? true: false;


            if (!$scope.$eval(expression)) {
                element.hide();
            }

            $scope.$watch(
                expression,
                function (newValue, oldValue) {

                    // watch for changes in the evaluation of the expression associated with jg-slide on any given element
                    if (newValue === oldValue) {
                        return;
                    }

                    if (newValue) {
                        if ( isScrollable ){
                            if ( element.parent().prev() && element.parent().prev().offset()){
                                var scrollPos = element.parent().prev().offset().top - 100;
                                $("body,html").animate({scrollTop: scrollPos}, duration);
                            }
                        }
                        element
                            .stop(true, true)
                            .slideDown(duration)
                        ;

                        //For IE - changing css
                        element.css("display","block");
                        element.css("overflow","visible");
                    } else {
                        element
                            .stop(true, true)
                            .slideUp(duration)
                        ;
                    }

                }
            );

        }

        return ({
            link: link,
            restrict: "A"
        });
    }
);



window[appName].config(function($stateProvider, $urlRouterProvider,$httpProvider) {

       //$httpProvider.defaults.useXDomain = true;

        //delete $httpProvider.defaults.headers.common['X-Requested-With'];

    $urlRouterProvider.otherwise('/');

    $stateProvider
        .state('scg_dashboard', {
            url: '/',
            templateUrl: 'modules/scg/dashboard/dashboard.html',
            controller: 'scg_dashboard_controller',
        });

    $stateProvider
        .state('scg_devices', {
            url: '/scg_devices',
            templateUrl:  'modules/scg/devices/devices.html',
            controller: 'scg_devices_controller'
        });
  
	$stateProvider
        .state('scg_settings', {
            url: '/scg_settings',
            templateUrl:  'modules/scg/settings/settings.html',
            controller: 'scg_settings_controller'
        });
	
	$stateProvider
        .state('scg_logs', {
            url: '/scg_logs',
            templateUrl:  'modules/scg/logs/logs.html',
            controller: 'scg_logs_controller'
        });
 

	$stateProvider
        .state('scg_trends', {
            url: '/scg_trends',
            templateUrl:  'modules/scg/trends/trends.html',
            controller: 'scg_trends_controller'
        });
		
	$stateProvider
        .state('scg_events', {
            url: '/scg_events',
            templateUrl:  'modules/scg/events/events.html',
            controller: 'scg_events_controller'
        });
	 
	$stateProvider
		.state('scg_maillogs', {
            url: '/scg_maillogs',
            templateUrl:  'modules/scg/maillogs/maillogs.html',
            controller: 'scg_maillogs_controller'
        });

	$stateProvider
		.state('zd_dashboard', {
			url: '/zd_dashboard',
			templateUrl:  'modules/zd/dashboard/dashboard.html',
			controller: 'zd_dashboard_controller'
		});
		
		
	$stateProvider
		.state('zd_devices', {
			url: '/zd_devices',
			templateUrl:  'modules/zd/devices/devices.html',
			controller: 'zd_devices_controller'
		});
		
		
	$stateProvider
		.state('zd_settings', {
			url: '/zd_settings',
			templateUrl:  'modules/zd/settings/settings.html',
			controller: 'zd_settings_controller'
		});

   $stateProvider
        .state('zd_logs', {
            url: '/zd_logs',
            templateUrl:  'modules/zd/logs/logs.html',
            controller: 'zd_logs_controller'
        });

   $stateProvider
        .state('zd_trends', {
            url: '/zd_trends',
           templateUrl:  'modules/zd/trends/trends.html',
            controller: 'zd_trends_controller'
        });

	
   $stateProvider
        .state('zd_events', {
            url: '/zd_events',
            templateUrl:  'modules/zd/events/events.html',
            controller: 'zd_events_controller'
        });

      $stateProvider
        .state('zd_maillogs', {
            url: '/zd_maillogs',
           templateUrl:  'modules/zd/maillogs/maillogs.html',
            controller: 'zd_maillogs_controller'
        });
		
		
		
		 $stateProvider
        .state('user_management', {
            url: '/user_management',
           templateUrl:  'modules/user_management/users/users.html',
            controller: 'user_controller'
        });
		
		
		
		 $stateProvider
        .state('authentication_servers', {
            url: '/authentication_servers',
           templateUrl:  'modules/user_management/authentication_servers/authentication_server.html',
            controller: 'authentication_server_controller'
        });
		
		
});


window[appName].factory('loginService',function($http,$location) {
	return {
		
		islogged:function() {
			
			var $checkSessionServer = $http.post('/check_session_data');
			
			return $checkSessionServer;
			
		}
		
	}
	
});


window[appName].factory('sessionService',function() {
	return {
		set:function(key,value) {
			return sessionStorage.setItem(key,value);	
		},
		get:function() {
			return sessionStorage.getItem(key);	
		},
		destroy:function() {
			return sessionStorage.removeItem(key);	
		}
	};
})



window[appName].run(function($rootScope,$window,$location){

	
	$rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
		
		//console.log('toState.name: '+toState.name);
	
		$rootScope.navigation.menu_item = toState.name;	
		
		$rootScope.expand = !$rootScope.expand;

		
  });

});




window[appName].controller('xcloud_controller',function($rootScope,$scope,$state,$http){
	
	$rootScope.showLoader = false;
	
	$rootScope.showConfirm = false;
	
	$rootScope.expand = true;
	
	$scope.innerAccordion = {};
	
	$rootScope.navigation = {};
	
	$rootScope.navigation.menu_item = 'scg_dashboard';
	
	$scope.innerAccordion.menu = 'SCG';
	
	//$rootScope.expand = true;
	
	$scope.navigate_menu = function(menu_name) {
		
		$scope.innerAccordion.menu = menu_name;
		
	}
	
	$rootScope.expand_menu = function() {
		
		$rootScope.expand = !$rootScope.expand;
		
	}
	
	//console.log($state.current);
  //$scope.logged_in = sessionStorage.getItem("name");

   
});
