angular.module('towerAdminApp')
.controller('SidebarController', function($scope, $location) {
    $scope.isActive = function(viewPath){
        return $location.path() === viewPath;
    };
});