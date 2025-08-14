angular.module('towerAdminApp')

.controller('LoginController', function($scope, $location, AuthService) {
    $scope.credentials = {
        username: '',
        password: ''
    };
    
    $scope.loginError = '';
    $scope.isLogging = false;
    
    // If already authenticated, redirect to dashboard
    if (AuthService.isAuthenticated()) {
        $location.path('/dashboard');
        return;
    }
    
    $scope.login = function() {
        if (!$scope.credentials.username || !$scope.credentials.password) {
            $scope.loginError = 'Please enter both username and password';
            return;
        }
        
        $scope.isLogging = true;
        $scope.loginError = '';
        
        AuthService.login($scope.credentials)
            .then(function(response) {
                $scope.isLogging = false;
                // Redirect to dashboard on successful login
                $location.path('/dashboard');
            })
            .catch(function(error) {
                $scope.isLogging = false;
                if (error.data && error.data.error) {
                    $scope.loginError = error.data.error;
                } else {
                    $scope.loginError = 'Login failed. Please try again.';
                }
            });
    };
    
    $scope.clearError = function() {
        $scope.loginError = '';
    };
});