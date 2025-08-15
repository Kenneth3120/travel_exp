angular.module('towerAdminApp')
.controller('EnvironmentController', function($scope, $http) {

    $scope.environments = [];
    $scope.instances = [];
    $scope.newEnv = {};

    // Load environment data
    $scope.loadEnvironments = function() {
        $http.get('http://localhost:8001/api/environments/')
            .then(function(response) {
                $scope.environments = response.data;
            })
            .catch(function(error) {
                console.error('Error loading environments:', error);
                alert('Error loading environments. Please check your connection.');
            });
    };

    // Load instances for dropdown
    $scope.loadInstances = function() {
        $http.get('http://localhost:8001/api/instances/')
            .then(function(response) {
                $scope.instances = response.data;
            })
            .catch(function(error) {
                console.error('Error loading instances:', error);
                // Continue without instances if they fail to load
            });
    };

    // Load environments from API
    $scope.loadEnvironments = function() {
        $http.get('http://localhost:8001/api/environments/')
            .then(function(response) {
                $scope.environments = response.data;
            })
            .catch(function(error) {
                console.error('Error loading environments:', error);
            });
    };

    // Add new environment
    $scope.addEnvironment = function() {
        if (!$scope.newEnv.name) {
            alert('Name is required');
            return;
        }

        $http.post('http://localhost:8001/api/environments/', $scope.newEnv)
            .then(function(response) {
                $scope.environments.push(response.data);
                $scope.newEnv = {}; // Reset form
                alert('Environment added successfully!');
            })
            .catch(function(error) {
                console.error('Error adding environment:', error);
                alert('Error adding environment. Please try again.');
            });
    };

    // Delete environment
    $scope.deleteEnvironment = function(id) {
        if (confirm('Are you sure you want to delete this environment?')) {
            $http.delete(`http://localhost:8001/api/environments/${id}/`)
                .then(function() {
                    $scope.environments = $scope.environments.filter(e => e.id !== id);
                    alert('Environment deleted successfully!');
                })
                .catch(function(error) {
                    console.error('Error deleting environment:', error);
                    alert('Error deleting environment. Please try again.');
                });
        }
    };

    // Initialize data loading
    $scope.loadEnvironments();
    $scope.loadInstances();
});