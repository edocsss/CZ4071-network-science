function GraphDataService($q) {
    // var graph = getGraph(); // api call to web server
    return {
        loadGraph: function() {
            // return $q.when(graph); // callback
        }
    };
}

export default ['$q', GraphDataService];
