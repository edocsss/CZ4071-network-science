 function ContentController($scope, EVENTS, GraphDataFactory) {
     $scope.isInitial = true;

     $scope.delay = 0;
     $scope.minDuration = 0;
     $scope.message = 'Please Wait...';
     $scope.backdrop = true;

     $scope.setPromise = function(promise) {
         $scope.myPromise = promise;
     }

     $scope.$on(EVENTS.NEW_GRAPH_DATA, function() {
         $scope.isInitial = false;
     });

     // initialization
     if ($scope.isInitial) {
         $scope.myPromise = GraphDataFactory.getExampleGraphData();
     }
 }

 export default ['$scope', 'EVENTS', 'GraphDataFactory', ContentController];