function FormController($scope, Upload, $timeout) {

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
            console.log(file);
            // Upload.upload({
            //     url: '', // flask
            //     data: { file: file },
            // }).then(function(response) {
            //     $timeout(function() {
            //         file.result = response.data;
            //     });
            //     console.log('Success ' + response.config.data.file.name + 'uploaded. Response: ' + response.data);
            // }, function(response) {
            //     if (response.status > 0) {
            //         $scope.errorMsg = response.status + ': ' + response.data;
            //         console.log('Error status: ' + response.status);
            //     }
            // }, function(evt) {
            //     // loading progress
            //     var percentProgress = parseInt(100.0 * evt.loaded / evt.total);
            //     file.progress = Math.min(100, percentProgress);
            //     console.log('progress: ' + percentProgress + '% ' + evt.config.data.file.name);
            // });
        }
    }

    $scope.graphOptions = {
        numberOfNodes: 10,
        probability: 0.25
    };

    $scope.change = function() {
        console.log($scope.graphOptions);
    }
}

export default ['$scope', 'Upload', '$timeout', FormController];