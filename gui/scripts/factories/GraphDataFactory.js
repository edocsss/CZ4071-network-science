function GraphDataFactory($rootScope, $http, Upload, URL, EVENTS) {
    let graphData = {
        guiNetworkFormat: {},
        networkProperties: {}
    };

    return {
        getGraphData: getGraphData,
        getGraphGuiFormat: getGraphGuiFormat,
        getGraphProperties: getGraphProperties,
        computeGraphProperties: computeGraphProperties,
        getExampleGraphData: getExampleGraphData
    };

    function getGraphData() {
        return graphData;
    }

    function getGraphGuiFormat() {
        return graphData.guiNetworkFormat;
    }

    function getGraphProperties() {
        return graphData.networkProperties;
    }

    function _updateGraphData(newGraphData) {
        graphData = newGraphData;
        $rootScope.$broadcast(EVENTS.NEW_GRAPH_DATA);
    }

    function computeGraphProperties(file) {
        Upload.upload({
            url: URL.NETWORK_UPLOAD_URL,
            data: { file: file },
            method: 'POST'
        }).then(function(response) {
            _updateGraphData(response.data);
        }, function(response) {
            if (response.status > 0) {
                console.error(response.status + ': ' + response.data);
            }
        });
    }

    function getExampleGraphData() {
        $http({
            method: 'GET',
            url: URL.GET_EXAMPLE_NETWORK_URL
        }).then(function success (response) {
            _updateGraphData(response.data);
        }, function failure (response) {
            if (response.status > 0) {
                console.error(response.status + ': ' + response.data);
            }
        });
    }
}

export default ['$rootScope', '$http', 'Upload', 'URL', 'EVENTS', GraphDataFactory];
