function GraphDataFactory($http, Upload, URL) {
    let graphData = {};

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
        return graphData;
    }

    function getGraphProperties() {
        return graphData;
    }

    function computeGraphProperties(file) {
        Upload.upload({
            url: URL.NETWORK_UPLOAD_URL, // flask
            data: { file: file },
            method: 'POST'
        }).then(function(response) {
            graphData = response.data;
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
            graphData = response.data;
            console.log(graphData);
        }, function failure (response) {
            if (response.status > 0) {
                console.error(response.status + ': ' + response.data);
            }
        });
    }
}

export default ['$http', 'Upload', 'URL', GraphDataFactory];
