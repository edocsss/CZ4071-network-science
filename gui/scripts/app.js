import angular from 'angular';
import 'angular-animate';
import 'angular-aria';
import 'angular-busy';
import 'angular-material';
import 'angular-messages';
import 'angular-material-data-table';
import 'angular-material/angular-material.min.css!';
import 'angular-busy/dist/angular-busy.min.css!';
import 'angular-material-data-table/dist/md-data-table.min.css!';
import 'style/app.css!';
import 'ng-file-upload';

import ContentController from 'src/controllers/ContentController';
import GraphVisualizationController from 'src/controllers/GraphVisualizationController';
import GraphGeneratorController from 'src/controllers/GraphGeneratorController';
import GraphPropertyController from 'src/controllers/GraphPropertyController';
import GraphDataFactory from 'src/factories/GraphDataFactory';
import URL from 'src/constants/URL';
import EVENTS from 'src/constants/Events';

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
        };
    })
    .filter('propValFilter', function($filter) {
        return function(str, precision) {
            if (!isNaN(str)) {
                return $filter('number')(str, precision);
            }
            return str;
        };
    })
    .constant('URL', URL)
    .constant('EVENTS', EVENTS);