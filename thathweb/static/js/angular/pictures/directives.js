angular.module('pictures.directives', []).directive('isotopeContainer', function($timeout){
    return function(scope, element, attrs) {
        scope.$watch('pictures', function(value) {
            console.log(value);
            $timeout( function() {
                $('#image-container').isotope({
                    itemSelector : '.picture',
                    masonry: {
                        columnWidth : 200,
                        gutterWidth : 25
                    }
                });
                $('#image-container').isotope('reLayout');
            }, 0);
        });
    }
});
