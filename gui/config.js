System.config({
    baseURL: "/",
    defaultJSExtensions: true,
    transpiler: "babel",
    babelOptions: {
        "optional": [
            "runtime",
            "optimisation.modules.system"
        ]
    },
    separateCSS: true,
    paths: {
        "src/*": "scripts/*.js",
        "style/*": "css/*",
        "github:*": "jspm_packages/github/*",
        "npm:*": "jspm_packages/npm/*"
    },

    map: {
        "angular": "github:angular/bower-angular@1.6.2",
        "angular-animate": "github:angular/bower-angular-animate@1.6.2",
        "angular-aria": "github:angular/bower-angular-aria@1.6.2",
        "angular-block-ui": "npm:angular-block-ui@0.2.2",
        "angular-busy": "npm:angular-busy@4.1.4",
        "angular-material": "github:angular/bower-material@1.1.3",
        "angular-material-data-table": "npm:angular-material-data-table@0.10.10",
        "angular-messages": "github:angular/bower-angular-messages@1.6.2",
        "babel": "npm:babel-core@5.8.38",
        "babel-runtime": "npm:babel-runtime@5.8.38",
        "core-js": "npm:core-js@1.2.7",
        "css": "github:systemjs/plugin-css@0.1.32",
        "json": "github:systemjs/plugin-json@0.3.0",
        "ng-file-upload": "npm:ng-file-upload@12.2.13",
        "text": "github:systemjs/plugin-text@0.0.9",
        "github:angular/bower-angular-animate@1.6.2": {
            "angular": "github:angular/bower-angular@1.6.2"
        },
        "github:angular/bower-angular-aria@1.6.2": {
            "angular": "github:angular/bower-angular@1.6.2"
        },
        "github:angular/bower-angular-messages@1.6.2": {
            "angular": "github:angular/bower-angular@1.6.2"
        },
        "github:angular/bower-material@1.1.3": {
            "angular": "github:angular/bower-angular@1.6.2",
            "angular-animate": "github:angular/bower-angular-animate@1.6.2",
            "angular-aria": "github:angular/bower-angular-aria@1.6.2",
            "css": "github:systemjs/plugin-css@0.1.32"
        },
        "github:jspm/nodelibs-assert@0.1.0": {
            "assert": "npm:assert@1.4.1"
        },
        "github:jspm/nodelibs-buffer@0.1.0": {
            "buffer": "npm:buffer@3.6.0"
        },
        "github:jspm/nodelibs-path@0.1.0": {
            "path-browserify": "npm:path-browserify@0.0.0"
        },
        "github:jspm/nodelibs-process@0.1.2": {
            "process": "npm:process@0.11.9"
        },
        "github:jspm/nodelibs-util@0.1.0": {
            "util": "npm:util@0.10.3"
        },
        "github:jspm/nodelibs-vm@0.1.0": {
            "vm-browserify": "npm:vm-browserify@0.0.4"
        },
        "npm:angular-busy@4.1.4": {
            "process": "github:jspm/nodelibs-process@0.1.2"
        },
        "npm:angular-material-data-table@0.10.10": {
            "angular": "npm:angular@1.6.2",
            "angular-material": "npm:angular-material@1.1.3",
            "process": "github:jspm/nodelibs-process@0.1.2"
        },
        "npm:angular-material@1.1.3": {
            "angular": "github:angular/bower-angular@1.6.2",
            "angular-animate": "github:angular/bower-angular-animate@1.6.2",
            "angular-aria": "github:angular/bower-angular-aria@1.6.2",
            "angular-messages": "github:angular/bower-angular-messages@1.6.2",
            "css": "github:systemjs/plugin-css@0.1.32"
        },
        "npm:assert@1.4.1": {
            "assert": "github:jspm/nodelibs-assert@0.1.0",
            "buffer": "github:jspm/nodelibs-buffer@0.1.0",
            "process": "github:jspm/nodelibs-process@0.1.2",
            "util": "npm:util@0.10.3"
        },
        "npm:babel-runtime@5.8.38": {
            "process": "github:jspm/nodelibs-process@0.1.2"
        },
        "npm:buffer@3.6.0": {
            "base64-js": "npm:base64-js@0.0.8",
            "child_process": "github:jspm/nodelibs-child_process@0.1.0",
            "fs": "github:jspm/nodelibs-fs@0.1.2",
            "ieee754": "npm:ieee754@1.1.8",
            "isarray": "npm:isarray@1.0.0",
            "process": "github:jspm/nodelibs-process@0.1.2"
        },
        "npm:core-js@1.2.7": {
            "fs": "github:jspm/nodelibs-fs@0.1.2",
            "path": "github:jspm/nodelibs-path@0.1.0",
            "process": "github:jspm/nodelibs-process@0.1.2",
            "systemjs-json": "github:systemjs/plugin-json@0.1.2"
        },
        "npm:inherits@2.0.1": {
            "util": "github:jspm/nodelibs-util@0.1.0"
        },
        "npm:ng-file-upload@12.2.13": {
            "process": "github:jspm/nodelibs-process@0.1.2"
        },
        "npm:path-browserify@0.0.0": {
            "process": "github:jspm/nodelibs-process@0.1.2"
        },
        "npm:process@0.11.9": {
            "assert": "github:jspm/nodelibs-assert@0.1.0",
            "fs": "github:jspm/nodelibs-fs@0.1.2",
            "vm": "github:jspm/nodelibs-vm@0.1.0"
        },
        "npm:util@0.10.3": {
            "inherits": "npm:inherits@2.0.1",
            "process": "github:jspm/nodelibs-process@0.1.2"
        },
        "npm:vm-browserify@0.0.4": {
            "indexof": "npm:indexof@0.0.1"
        }
    }
});