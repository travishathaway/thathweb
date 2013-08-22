function Pictures($scope, $http){
    // Variables
    $scope.pictures = [];
    $scope.STATIC_URL = $('#static-url').val();

    // Initialize
    $http.get(
        '/pictures/'
    ).success( function(data) {
        $scope.pictures = data;
    }).error( function(data) {
        
    });

    // Functions
    $scope.getPage = function(page) {
        $http.get(
            '/pictures/page/'+page
        ).success( function(data) {
            $scope.pictures = data;
        }).error( function(data) {
            alert('server error');
        });
    };
}
