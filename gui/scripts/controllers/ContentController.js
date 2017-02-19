 function ContentController($scope, $window, EVENTS, GraphDataFactory) {
     $scope.isInitial = true;

     $scope.delay = 0;
     $scope.minDuration = 0;
     $scope.message = 'Loading Graph...';
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
         let circularProgressTop = 35;
         let loadingMessageTop = 50;
         let h = $window.innerHeight;
         $scope.circularTopPos = {
             top: Math.round(h * circularProgressTop / 100.0) + 'px'
         }
         $scope.loadingMessageTopPos = {
             top: Math.round(h * loadingMessageTop / 100.0) + 'px'
         }
     }
 }

 export default ['$scope', '$window', 'EVENTS', 'GraphDataFactory', ContentController];