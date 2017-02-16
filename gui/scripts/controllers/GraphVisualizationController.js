function GraphVisualizationController($scope, $timeout, GraphDataFactory, EVENTS) {
    let s;
    let g = new sigma.classes.graph();

    GraphDataFactory.getExampleGraphData();
    $scope.$on(EVENTS.NEW_GRAPH_DATA, function () {
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

export default ['$scope', '$timeout', 'GraphDataFactory', 'EVENTS', GraphVisualizationController];
