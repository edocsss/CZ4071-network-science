function GraphPropertyController($scope, GraphDataFactory, URL, EVENTS) {
    $scope.haveImage = false;

    $scope.$on(EVENTS.NEW_GRAPH_DATA, function() {
        $scope.realProps = GraphDataFactory.getRealNetworkProperties();
        $scope.scaleFreeProps = GraphDataFactory.getScaleFreeNetworkProperties();
        $scope.randomProps = GraphDataFactory.getRandomNetworkProperties();

        if (GraphDataFactory.haveImage()) {
            if ($scope.realProps) {
                if ($scope.realProps.degree_prob_distribution_plot_file_name) {
                    $scope.degreeDistPlotSrc = URL.GET_IMAGE_URL + $scope.realProps.degree_prob_distribution_plot_file_name;
                } else {
                    $scope.degreeDistPlotSrc = "";
                }
                if ($scope.realProps.distance_prob_distribution_plot_file_name) {
                    $scope.shortestDistPlotSrc = URL.GET_IMAGE_URL + $scope.realProps.distance_prob_distribution_plot_file_name;
                } else {
                    $scope.shortestDistPlotSrc = "";
                }
                $scope.expectedDegreeDistPlotSrc = "";
            }

            if ($scope.randomProps) {
                if ($scope.randomProps.expected_degree_distribution_plot_file_name) {
                    $scope.expectedDegreeDistPlotSrc = URL.GET_IMAGE_URL + $scope.randomProps.expected_degree_distribution_plot_file_name;
                } else {
                    $scope.expectedDegreeDistPlotSrc = "";
                }
            }

            $scope.haveImage = !!$scope.degreeDistPlotSrc || !!$scope.shortestDistPlotSrc || !!$scope.expectedDegreeDistPlotSrc;
        } else {
            $scope.haveImage = false;
        }
    });

    $scope.validValue = function(propName, propVal) {
        if (propName.indexOf('plot_file_name') != -1) {
            return false;
        }
        return propVal === 0 || !!propVal;
    };
}

export default ['$scope', 'GraphDataFactory', 'URL', 'EVENTS', GraphPropertyController];