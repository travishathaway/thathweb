var picturesApp = angular.module('pictures', ['pictures.directives']);

picturesApp.config( function($routeProvider) {
  $routeProvider.
      when('/', {controller: Pictures, templateUrl : '/static/templates/pictures/index.html'}).otherwise({redirectTo : '/'});
});
