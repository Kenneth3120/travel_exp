angular.module('towerAdminApp')

.factory('AuthService', function($http, $window, $location) {
    const API_BASE = 'http://localhost:8000/api/';
    
    return {
        login: function(credentials) {
            return $http.post(API_BASE + 'login/', credentials)
                .then(function(response) {
                    if (response.data.access) {
                        // Store tokens in localStorage
                        $window.localStorage.setItem('access_token', response.data.access);
                        $window.localStorage.setItem('refresh_token', response.data.refresh);
                        $window.localStorage.setItem('user_info', JSON.stringify(response.data.user));
                        return response.data;
                    }
                    throw new Error('Login failed');
                });
        },
        
        logout: function() {
            const refreshToken = $window.localStorage.getItem('refresh_token');
            const logoutPromise = $http.post(API_BASE + 'logout/', {
                refresh: refreshToken
            });
            
            // Clear local storage regardless of API call success
            $window.localStorage.removeItem('access_token');
            $window.localStorage.removeItem('refresh_token');
            $window.localStorage.removeItem('user_info');
            
            // Redirect to login
            $location.path('/login');
            
            return logoutPromise;
        },
        
        isAuthenticated: function() {
            const token = $window.localStorage.getItem('access_token');
            return !!token;
        },
        
        getToken: function() {
            return $window.localStorage.getItem('access_token');
        },
        
        getUserInfo: function() {
            if (this.isAuthenticated()) {
                const userInfo = $window.localStorage.getItem('user_info');
                return Promise.resolve(userInfo ? JSON.parse(userInfo) : null);
            }
            
            return $http.get(API_BASE + 'user-info/')
                .then(function(response) {
                    $window.localStorage.setItem('user_info', JSON.stringify(response.data));
                    return response.data;
                })
                .catch(function() {
                    // If user-info fails, user is not authenticated
                    return null;
                });
        },
        
        getCurrentUser: function() {
            const userInfo = $window.localStorage.getItem('user_info');
            return userInfo ? JSON.parse(userInfo) : null;
        }
    };
})

.factory('UserService', function($http) {
    const base = 'http://localhost:8000/api/users/';
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
})

// HTTP Interceptor to add Authorization header
.factory('AuthInterceptor', function($window, $location) {
    return {
        request: function(config) {
            const token = $window.localStorage.getItem('access_token');
            if (token) {
                config.headers.Authorization = 'Bearer ' + token;
            }
            return config;
        },
        responseError: function(response) {
            if (response.status === 401) {
                // Token expired or invalid, redirect to login
                $window.localStorage.removeItem('access_token');
                $window.localStorage.removeItem('refresh_token');
                $window.localStorage.removeItem('user_info');
                $location.path('/login');
            }
            return Promise.reject(response);
        }
    };
})

.config(function($httpProvider) {
    $httpProvider.interceptors.push('AuthInterceptor');
});