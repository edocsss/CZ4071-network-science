function GraphPropertyController($scope, GraphDataFactory, URL, EVENTS) {
    $scope.haveImage = false;

    $scope.$on(EVENTS.NEW_GRAPH_DATA, function() {
        $scope.realProps = GraphDataFactory.getRealNetworkProperties();
        $scope.scaleFreeProps = GraphDataFactory.getScaleFreeNetworkProperties();
        $scope.randomProps = GraphDataFactory.getRandomNetworkProperties();

        if (GraphDataFactory.haveImage()) {
            $scope.degreeDistPlotSrc = URL.GET_IMAGE_URL + $scope.realProps.degree_prob_distribution_plot_file_name;
            $scope.shortestDistPlotSrc = URL.GET_IMAGE_URL + $scope.realProps.distance_prob_distribution_plot_file_name;
            $scope.haveImage = true;
        } else {
            $scope.haveImage = false;
        }

        console.log(GraphDataFactory.getGraphData());
    });

    $scope.validValue = function(propName, propVal) {
        if (propName == 'degree_prob_distribution_plot_file_name' || propName == 'distance_prob_distribution_plot_file_name') {
            return false;
        }
        return propVal === 0 || typeof propVal == 'number' || typeof propVal == 'string';
    }
}

export default ['$scope', 'GraphDataFactory', 'URL', 'EVENTS', GraphPropertyController];