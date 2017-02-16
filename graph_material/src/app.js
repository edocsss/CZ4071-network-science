import angular from 'angular';

import 'angular-animate';
import 'angular-aria';
import 'angular-material';
import 'angular-messages';
import 'angular-nvd3';
import 'ng-file-upload';

import AppController from 'src/AppController';
import FormController from 'src/FormController';
import GraphController from 'src/GraphController';

export default angular.module('graph-gui', ['ngMaterial', 'nvd3', 'ngFileUpload', 'ngMessages'])
    .config(function($mdThemingProvider) {
        $mdThemingProvider.theme('default')
            .primaryPalette('light-green')
            .accentPalette('pink');

    })
    .controller('AppController', AppController)
    .controller('GraphController', GraphController)
    .controller('FormController', FormController);