function FormController($scope, Upload, $timeout) {
    $scope.graphComputationResult = {};

    // upload later on form submit
    $scope.submit = function() {
        if ($scope.form.file.$valid && $scope.file) {
            $scope.upload($scope.file);
        }
    };

    // upload on file select
    $scope.uploadFile = function(file) {
        if (file) {
            $scope.file = file;
            Upload.upload({
                url: 'http://localhost:3000/api/network', // flask
                data: { file: file },
                method: 'POST'
            }).then(function(response) {
                $scope.graphComputationResult = response.data;
                $scope.file = {};
                console.log($scope.graphComputationResult);
            }, function(response) {
                if (response.status > 0) {
                    $scope.errorMsg = response.status + ': ' + response.data;
                    $scope.file = {};
                    console.log('Error status: ' + response.status);
                }
            });
        }
    };

    $scope.graphOptions = {
        numberOfNodes: 10,
        probability: 0.25
    };

    $scope.change = function() {
        console.log($scope.graphOptions);
    };
}

export default ['$scope', 'Upload', '$timeout', FormController];
