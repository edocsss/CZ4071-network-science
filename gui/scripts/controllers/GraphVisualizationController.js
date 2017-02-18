function GraphVisualizationController($scope, $window, $timeout, GraphDataFactory, EVENTS) {
    let s;
    let padding = 10;
    let g = new sigma.classes.graph();

    let h = Math.floor($window.innerHeight * (1 - padding / 100.0));

    $scope.fullHeight = {
        height: h + "px"
    }

    $scope.$on(EVENTS.NEW_GRAPH_DATA, function() {
        $scope.graphData = GraphDataFactory.getGraphGuiFormat();
        drawGraph();
    });

    function drawGraph() {
        g.clear();
        g.read($scope.graphData);

        if (s) s.kill();
        s = new sigma({
            graph: GraphDataFactory.getGraphGuiFormat(),
            container: 'graph-container',
            settings: {
                defaultEdgeType: 'curve',
                defaultLabelColor: '#fff',
                defaultLabelSize: 14,
                defaultLabelBGColor: '#fff',
                defaultLabelHoverColor: '#000',
                labelThreshold: 6,
                minNodeSize: 0,
                maxNodeSize: 10,
                minEdgeSize: 0,
                maxEdgeSize: 10,
                hideEdgesOnMove: true
            }
        });

        s.render();
        s.startForceAtlas2({
            worker: true,
            adjustSizes: true,
            barnesHutTheta: 1
        });

        $timeout(() => {
            s.stopForceAtlas2();
        }, 0);
    }
}

export default ['$scope', '$window', '$timeout', 'GraphDataFactory', 'EVENTS', GraphVisualizationController];