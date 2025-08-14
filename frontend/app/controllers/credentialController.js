angular.module('towerAdminApp')
.controller('CredentialController', function($scope, $http) {

    // Filter models
    $scope.filterName = '';
    $scope.filterType = '';
    $scope.filterInstance = '';

    // Data models
    $scope.credentials = [];
    $scope.filteredCredentials = [];
    $scope.towerInstances = [];
    $scope.totalCredentials = 0;

    // Load credentials via Django Proxy
    $scope.loadCredentials = function() {
        $http.get('http://localhost:8000/api/tower-credentials/')
        .then(function(response) {
            $scope.credentials = response.data.results || response.data;
            $scope.totalCredentials = $scope.credentials.length;
            $scope.filteredCredentials = $scope.credentials;
        })
        .catch(function(err) {
            console.error('Error fetching credentials from tower proxy:', err);
            alert("Error fetching credentials from tower proxy.");
        });
    };

    // Load organizations (instances) for filter dropdown
    $scope.loadInstances = function() {
        $http.get('http://localhost:8000/api/organizations/')
        .then(function(response) {
            $scope.towerInstances = response.data.results || response.data;
        })
        .catch(function(err) {
            console.error('Failed loading organizations:', err);
        });
    };

    // Filter function
    $scope.credFilter = function(cred) {
        const name = cred.name?.toLowerCase() || '';
        const type = cred.summary_fields?.credential_type?.name?.toLowerCase() || '';
        const org  = cred.summary_fields?.organization?.name?.toLowerCase() || '';

        const matchesName = !$scope.filterName || name.includes($scope.filterName.toLowerCase());
        const matchesType = !$scope.filterType || type.includes($scope.filterType.toLowerCase());
        const matchesOrg  = !$scope.filterInstance || org.includes($scope.filterInstance.toLowerCase());

        return matchesName && matchesType && matchesOrg;
    };

    // Watch for filter changes
    $scope.$watchGroup(['filterName', 'filterType', 'filterInstance', 'credentials'], function() {
        $scope.filteredCredentials = $scope.credentials.filter($scope.credFilter);
    });

    // Initialize
    $scope.loadCredentials();
    $scope.loadInstances();
});
