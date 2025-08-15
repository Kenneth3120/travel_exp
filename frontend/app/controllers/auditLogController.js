angular.module('towerAdminApp')
.controller('AuditlogController', function($scope, $http) {

    $scope.auditlogs = [];
    
    // Load audit logs
    $http.get("http://localhost:8001/api/audit-logs/")
        .then(function(response) {
            $scope.auditlogs = response.data.results || response.data || [];
        })
        .catch(function(error) {
            console.error('Error loading audit logs:', error);
            alert('Error loading audit logs. Please check your connection.');
        });

    // Filter function for audit logs
    $scope.auditFilter = function(log) {
        let userMatch = true;
        let typeMatch = true;

        if ($scope.searchUser && $scope.searchUser.trim()) {
            userMatch = log.user && log.user.toLowerCase().includes($scope.searchUser.toLowerCase());
        }

        if ($scope.searchType && $scope.searchType.trim()) {
            typeMatch = log.object_type && log.object_type.toLowerCase().includes($scope.searchType.toLowerCase());
        }

        return userMatch && typeMatch;
    };
});