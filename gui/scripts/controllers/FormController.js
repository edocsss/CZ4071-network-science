function FormController($scope, GraphDataFactory) {
    $scope.graphComputationResult = {};

    // upload on file select
    $scope.uploadFile = function(file) {
        if (file) {
            GraphDataFactory.computeGraphProperties(file);
        }
    };

    $scope.graphOptions = {
        numberOfNodes: 10,
        probability: 0.25
    };

    // NEED TO HANDLE OPTION CHANGED!!
    $scope.onOptionChange = function() {
        console.log($scope.graphOptions);
    };
}

export default ['$scope', 'GraphDataFactory', FormController];
