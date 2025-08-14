angular.module('towerAdminApp')

.factory('AuthService', function($http) {
    return {
        getUserInfo: function() {
            return $http
                .get('http://127.0.0.1:8000/api/user-info/')
                .then(function(response) {
                    return response.data;
                });
        }
    };
})

.factory('UserService', function($http) {
    const base = 'http://127.0.0.1:8000/api/users/';
    return {
        list: function() {
            return $http.get(base).then(function(r) { return r.data; });
        },
        create: function(user) {
            return $http.post(base, user).then(function(r) { return r.data; });
        },
        update: function(user) {
            return $http.put(base + user.id + '/', user).then(function(r) { return r.data; });
        },
        delete: function(userId) {
            return $http.delete(base + userId + '/').then(function(r) { return r.data; });
        }
    };
});
