function GraphPropertyController($scope, GraphDataFactory) {
    $scope.graphProperties = GraphDataFactory.getGraphProperties;
}

export default ['$scope', 'GraphDataFactory', GraphPropertyController];
