import angular from 'angular';
import 'angular-animate';
import 'angular-aria';
import 'angular-material';
import 'angular-messages';
import 'angular-nvd3';
import 'ng-file-upload';

import FormController from './controllers/FormController';
import GraphVisualizationController from './controllers/GraphVisualizationController';
import GraphPropertyController from './controllers/GraphPropertyController';
import GraphDataFactory from './factories/GraphDataFactory';
import URL from './constants/URL';

export default angular.module('graph-gui', ['ngMaterial', 'nvd3', 'ngFileUpload', 'ngMessages'])
    .config(function($mdThemingProvider) {
        $mdThemingProvider.theme('default')
            .primaryPalette('light-green')
            .accentPalette('pink');

    })
    .controller('GraphVisualizationController', GraphVisualizationController)
    .controller('GraphPropertyController', GraphPropertyController)
    .controller('FormController', FormController)
    .factory('GraphDataFactory', GraphDataFactory)
    .constant('URL', URL);
