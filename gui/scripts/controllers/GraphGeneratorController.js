function GraphGeneratorController($scope, $window, GraphDataFactory) {
    if ($scope.isInitial) {
        let percent = 22;
        let w = $window.innerWidth;

        $scope.navRight = {
            width: Math.round(w * percent / 100.0) + "px"
        };
    }

    $scope.graphComputationResult = {};
    $scope.uploadFile = function(file) {
        if (file) {
            $scope.setPromise(GraphDataFactory.computeGraphProperties(file));
        }
    };

    $scope.graphOptions = {
        n: 10,
        p: 0.1
    };

    $scope.submitJson = function() {
        $scope.setPromise(GraphDataFactory.getRandomGraphData($scope.graphOptions));
    };
}

export default ['$scope', '$window', 'GraphDataFactory', GraphGeneratorController];
