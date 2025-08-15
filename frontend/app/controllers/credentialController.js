angular.module('towerAdminApp')
.controller('CredentialController', function($scope, $http) {

    $scope.credentials = [];
    $scope.newCredential = {};
    $scope.organizations = [];
    $scope.credentialTypes = ['Machine', 'Network', 'Cloud', 'Source Control', 'Vault'];

    // Load credentials from backend API
    $scope.loadCredentials = function() {
        // Load from Django backend
        $http.get('http://localhost:8001/api/credentials/')
            .then(function(response) {
                $scope.credentials = response.data;
            })
            .catch(function(error) {
                console.error('Error loading credentials from backend:', error);
                // Fallback: Try loading from Tower proxy
                $http.get('http://localhost:8001/api/tower-credentials/')
                    .then(function(response) {
                        $scope.credentials = response.data;
                    })
                    .catch(function(proxyError) {
                        console.error('Error loading credentials from Tower proxy:', proxyError);
                        alert('Error loading credentials. Please check your connection.');
                    });
            });
    };

    // Load organizations
    $scope.loadOrganizations = function() {
        $http.get('http://localhost:8001/api/organizations/')
            .then(function(response) {
                $scope.organizations = response.data;
            })
            .catch(function(error) {
                console.error('Error loading organizations:', error);
                // Continue without organizations if they fail to load
            });
    };

    // Add new credential
    $scope.addCredential = function() {
        if (!$scope.newCredential.name || !$scope.newCredential.type) {
            alert('Name and Type are required');
            return;
        }

        $http.post('http://localhost:8001/api/credentials/', $scope.newCredential)
            .then(function(response) {
                $scope.credentials.push(response.data);
                $scope.newCredential = {}; // Reset form
                alert('Credential added successfully!');
            })
            .catch(function(error) {
                console.error('Error adding credential:', error);
                alert('Error adding credential. Please try again.');
            });
    };

    // Delete credential
    $scope.deleteCredential = function(id) {
        if (confirm('Are you sure you want to delete this credential?')) {
            $http.delete(`http://localhost:8001/api/credentials/${id}/`)
                .then(function() {
                    $scope.credentials = $scope.credentials.filter(c => c.id !== id);
                    alert('Credential deleted successfully!');
                })
                .catch(function(error) {
                    console.error('Error deleting credential:', error);
                    alert('Error deleting credential. Please try again.');
                });
        }
    };

    // Initialize data loading
    $scope.loadCredentials();
    $scope.loadOrganizations();
});