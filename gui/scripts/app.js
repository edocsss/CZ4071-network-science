import angular from 'angular';
import 'angular-animate';
import 'angular-aria';
import 'angular-busy';
import 'angular-material';
import 'angular-messages';
import 'angular-material-data-table';
import 'ng-file-upload';

import ContentController from './controllers/ContentController';
import GraphVisualizationController from './controllers/GraphVisualizationController';
import GraphGeneratorController from './controllers/GraphGeneratorController';
import GraphPropertyController from './controllers/GraphPropertyController';
import GraphDataFactory from './factories/GraphDataFactory';
import URL from './constants/URL';
import EVENTS from './constants/Events';

export default angular.module('graph-gui', ['ngMaterial', 'ngFileUpload', 'ngMessages', 'cgBusy', 'ngAnimate', 'md.data.table'])
    .config(function($mdThemingProvider) {
        $mdThemingProvider.theme('default').primaryPalette('light-green').accentPalette('pink');
    })
    .controller('ContentController', ContentController)
    .controller('GraphVisualizationController', GraphVisualizationController)
    .controller('GraphPropertyController', GraphPropertyController)
    .controller('GraphGeneratorController', GraphGeneratorController)
    .factory('GraphDataFactory', GraphDataFactory)
    .filter('propNameFilter', function() {
        return function(str) {
            let new_str = str.split("_").join(" ");
            return new_str.charAt(0).toUpperCase() + new_str.slice(1);
        }
    })
    .filter('propValFilter', function($filter) {
        return function(str, precision) {
            if (!isNaN(str)) {
                return $filter('number')(str, precision);
            }
            return str;
        }
    })
    .constant('URL', URL)
    .constant('EVENTS', EVENTS);