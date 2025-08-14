angular.module('towerAdminApp')
.controller('MainController', function($scope, $location, AuthService) {
    $scope.message = "Frontend is working";
    
    // Check if current route is active
    $scope.isActive = function(viewLocation) { 
        return viewLocation === $location.path();
    };
    
    // Get current user info
    $scope.getCurrentUser = function() {
        return AuthService.getCurrentUser();
    };
    
    // Logout function
    $scope.logout = function() {
        AuthService.logout();
    };
    
    // Check if user is authenticated to show/hide navigation
    $scope.isAuthenticated = function() {
        return AuthService.isAuthenticated();
    };
});