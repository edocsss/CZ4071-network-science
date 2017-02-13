function convertData(links) {
    var nodesById = {}

    links.forEach(function(link) {
        link.source = getNode(link.FromNodeId);
        link.target = getNode(link.ToNodeId);
    });
    
    function getNode(id) {
        return nodesById[id] || (nodesById[id] = {
            id: id
        });
    }

    return {
        nodes: nodes,
        links: links
    }
}

function readTsv(file_path){
    d3.tsv(file_path, function(error, data) {
        if (error) throw error;
        
        // convert data into graph links
        var graph = convertDataToGraph(data);
    });
}