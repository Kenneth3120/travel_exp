angular.module('towerAdminApp')
.controller('InstanceController', function($scope, $http) {

    // Data models
    $scope.instances = [];
    $scope.newInstance = {};
    $scope.filters = {
        region: '',
        environment: ''
    };
    $scope.uniqueRegions = [];
    $scope.uniqueEnvironments = [];
    $scope.showAddInstanceModal = false; // Controls modal visibility  
    $scope.connectionTestStatus = '';
    $scope.connectionTestError = '';
    $scope.connectionSuccessful = false;
//Line no 13-16, 43-84, 87-90, 96
    // Load instances from API
    $scope.loadInstances = function() {
        $http.get('http://127.0.0.1:8000/api/instances/')
            .then(function(response) {
                $scope.instances = response.data;
                $scope.extractFilterValues();
            })
            .catch(function(error) {
                console.error('Failed to load instances:', error);
            });
    };

    // Extract unique values for dropdown filters
    $scope.extractFilterValues = function() {
        $scope.uniqueRegions = [...new Set($scope.instances.map(i => i.region))];
        $scope.uniqueEnvironments = [...new Set($scope.instances.map(i => i.environment))];
    };

    // Filter function for ng-repeat
    $scope.filterByRegionAndEnvironment = function(instance) {
        const matchRegion = !$scope.filters.region || instance.region === $scope.filters.region;
        const matchEnv = !$scope.filters.environment || instance.environment === $scope.filters.environment;
        return matchRegion && matchEnv;
    };

    $scope.openAddInstanceModal = function() {
        $scope.showAddInstanceModal = true;
        $scope.newInstance = {}; // Reset form fields
        $scope.connectionTestStatus = ''; // Reset status
        $scope.connectionTestError = ''; // Reset error
        $scope.connectionSuccessful = false; // Reset success flag
    };

    $scope.closeAddInstanceModal = function() {
        $scope.showAddInstanceModal = false;
    };

    $scope.testConnection = function() {
        $scope.connectionTestStatus = 'Testing...';
        $scope.connectionTestError = '';
        $scope.connectionSuccessful = false;

        // Simulate API call to test connection
        $http.post('http://127.0.0.1:8000/api/test-connection/', $scope.newInstance)
            .then(function(response) {
                if (response.status === 200 || response.status === 201) {
                    $scope.connectionTestStatus = 'Connection successful!';
                    $scope.connectionSuccessful = true;
                } else {
                    $scope.connectionTestStatus = 'Connection failed.';
                    $scope.connectionTestError = response.data.message || 'Unknown error';
                    $scope.connectionSuccessful = false;
                }
            })
            .catch(function(error) {
                $scope.connectionTestStatus = 'Connection failed.';
                if (error.status === 401 || error.status === 403) {
                    $scope.connectionTestError = 'Authentication failed: Invalid credentials.';
                } else if (error.status === -1) { // Timeout or network error
                    $scope.connectionTestError = 'Connection timeout or network error.';
                } else {
                    $scope.connectionTestError = error.data.message || 'An unexpected error occurred.';
                }
                $scope.connectionSuccessful = false;
            });
    };

    // Add a new instance
    $scope.addInstance = function() {
        if (!$scope.connectionSuccessful) {
            alert('Please test the connection successfully before creating an instance.');
            return;
        }
        $http.post('http://127.0.0.1:8000/api/instances/', $scope.newInstance)
            .then(function(response) {
                $scope.instances.push(response.data);
                $scope.newInstance = {}; // reset form
                $scope.extractFilterValues();
                $scope.closeAddInstanceModal(); // Close modal on success
            })
            .catch(function(error) {
                console.error('Failed to add instance:', error);
            });
    };

    // Delete an instance
    $scope.deleteInstance = function(id) {
        $http.delete(`http://127.0.0.1:8000/api/instances/${id}/`)
            .then(function() {
                $scope.instances = $scope.instances.filter(i => i.id !== id);
                $scope.extractFilterValues();
            })
            .catch(function(error) {
                console.error('Failed to delete instance:', error);
            });
    };

    // Initialize
    $scope.loadInstances();

});
