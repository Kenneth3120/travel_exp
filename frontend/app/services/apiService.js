angular.module('towerAdminApp')
.factory('apiService', function($http) {
    return {
        getExample: function() {
            return $http.get('/api/example');
        }
    };
});
