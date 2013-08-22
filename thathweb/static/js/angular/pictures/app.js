var refundApp = angular.module('pictures', []);

refundApp.config( function($routeProvider) {
  $routeProvider.
      when('/', {controller: Pictures, templateUrl : '/static/templates/pictures/index.html'}).otherwise({redirectTo : '/'});
});
