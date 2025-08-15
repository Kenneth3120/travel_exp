angular.module('towerAdminApp')
.controller('MainController', function($scope, $location, AuthService) {
    $scope.message = "Frontend is working";
    
    // Cache current user to prevent infinite digest
    $scope.currentUser = null;
    
    // Check if current route is active
    $scope.isActive = function(viewLocation) { 
        return viewLocation === $location.path();
    };
    
    // Get current user info - cached version to prevent infinite digest
    $scope.getCurrentUser = function() {
        if (!$scope.currentUser) {
            $scope.currentUser = AuthService.getCurrentUser();
        }
        return $scope.currentUser;
    };
    
    // Logout function
    $scope.logout = function() {
        $scope.currentUser = null; // Clear cache
        AuthService.logout();
    };
    
    // Check if user is authenticated to show/hide navigation
    $scope.isAuthenticated = function() {
        return AuthService.isAuthenticated();
    };
    
    // Initialize current user if authenticated
    if (AuthService.isAuthenticated()) {
        $scope.currentUser = AuthService.getCurrentUser();
    }
});