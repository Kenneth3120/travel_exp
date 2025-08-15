angular.module('towerAdminApp')
.controller('InstanceController', function($scope, $http) {

    $scope.instances = [];
    $scope.newInstance = {};
    $scope.uniqueRegions = [];
    $scope.uniqueEnvironments = [];
    $scope.filters = {
        region: '',
        environment: ''
    };

    // Load instances from API
    $scope.loadInstances = function() {
        $http.get('http://localhost:8001/api/instances/')
            .then(function(response) {
                $scope.instances = response.data;
                $scope.updateUniqueValues();
            })
            .catch(function(error) {
                console.error('Error loading instances:', error);
                alert('Error loading instances. Please check your connection.');
            });
    };

    // Update unique values for filters
    $scope.updateUniqueValues = function() {
        $scope.uniqueRegions = [...new Set($scope.instances.map(i => i.region).filter(r => r))];
        $scope.uniqueEnvironments = [...new Set($scope.instances.map(i => i.environment).filter(e => e))];
    };

    // Add new instance
    $scope.addInstance = function() {
        if (!$scope.newInstance.name || !$scope.newInstance.url) {
            alert('Name and URL are required');
            return;
        }

        $http.post('http://localhost:8001/api/instances/', $scope.newInstance)
            .then(function(response) {
                $scope.instances.push(response.data);
                $scope.newInstance = {}; // Reset form
                $scope.updateUniqueValues();
                alert('Instance added successfully!');
            })
            .catch(function(error) {
                console.error('Error adding instance:', error);
                alert('Error adding instance. Please try again.');
            });
    };

    // Delete instance
    $scope.deleteInstance = function(id) {
        if (confirm('Are you sure you want to delete this instance?')) {
            $http.delete(`http://localhost:8001/api/instances/${id}/`)
                .then(function() {
                    $scope.instances = $scope.instances.filter(i => i.id !== id);
                    $scope.updateUniqueValues();
                    alert('Instance deleted successfully!');
                })
                .catch(function(error) {
                    console.error('Error deleting instance:', error);
                    alert('Error deleting instance. Please try again.');
                });
        }
    };

    // Filter function for instances
    $scope.filterByRegionAndEnvironment = function(instance) {
        const regionMatch = !$scope.filters.region || instance.region === $scope.filters.region;
        const environmentMatch = !$scope.filters.environment || instance.environment === $scope.filters.environment;
        return regionMatch && environmentMatch;
    };

    // Initialize data loading
    $scope.loadInstances();
});