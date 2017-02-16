function GraphVisualizationController($scope, GraphDataFactory) {
    $scope.options = {
        chart: {
            type: 'forceDirectedGraph',
            margin: {
                top: 20,
                right: 20,
                bottom: 20,
                left: 20
            },
            color: function (d) {
                return 1;
            },
            noData: ''
        },
        styles: {
            css: {
                width: '100%',
                height: '100%'
            }
        }
    };

    $scope.graphData = GraphDataFactory.getGraphGuiFormat;
    GraphDataFactory.getExampleGraphData();
}

export default ['$scope', 'GraphDataFactory', GraphVisualizationController];
