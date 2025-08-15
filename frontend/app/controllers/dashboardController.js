angular.module('towerAdminApp')
.controller('DashboardController', function($scope, $http, $timeout, $q) {

    // Loader Flags
    $scope.loadingCounts = true;
    $scope.loadingLogs = true;

    // Initial values
    $scope.instanceCount = 0;
    $scope.credentialCount = 0;
    $scope.environmentCount = 0;
    $scope.recentChanges = [];
    $scope.toasts = [];

    // Toast Notification
    $scope.showToast = function(type, message) {
        const id = Date.now();
        $scope.toasts.push({ id, type, message });
        $timeout(() => {
            $scope.toasts = $scope.toasts.filter(t => t.id !== id);
        }, 4000);
    };

    $scope.closeToast = function(id) {
        $scope.toasts = $scope.toasts.filter(t => t.id !== id);
    };

    // Load Instance Count with Error Handling
    const loadInstanceCount = function() {
        $http.get('http://localhost:8001/api/instances/')
            .then(function(response) {
                $scope.instanceCount = response.data.length;
            })
            .catch(function(error) {
                console.error('Error loading instances:', error);
                $scope.instanceCount = 0;
            });
    };

    // Load Credential Count with Error Handling  
    const loadCredentialCount = function() {
        $http.get('http://localhost:8001/api/credentials/')
            .then(function(response) {
                $scope.credentialCount = response.data.length;
            })
            .catch(function(error) {
                console.error('Error loading credentials:', error);
                $scope.credentialCount = 0;
            });
    };

    // Load Environment Count with Error Handling
    const loadEnvironmentCount = function() {
        $http.get('http://localhost:8001/api/environments/')
            .then(function(response) {
                $scope.environmentCount = response.data.length;
            })
            .catch(function(error) {
                console.error('Error loading environments:', error);
                $scope.environmentCount = 0;
            });
    };

    // Load Counts with Promise.all to handle all at once
    const loadAllCounts = function() {
        $scope.loadingCounts = true;
        
        const promises = [
            $http.get('http://localhost:8001/api/instances/').catch(() => ({ data: [] })),
            $http.get('http://localhost:8001/api/credentials/').catch(() => ({ data: [] })),
            $http.get('http://localhost:8001/api/environments/').catch(() => ({ data: [] }))
        ];

        $q.all(promises).then(function(responses) {
            $scope.instanceCount = responses[0].data.length || 0;
            $scope.credentialCount = responses[1].data.length || 0;
            $scope.environmentCount = responses[2].data.length || 0;
            $scope.loadingCounts = false;
        }).catch(function(error) {
            console.error('Error loading counts:', error);
            $scope.instanceCount = 0;
            $scope.credentialCount = 0;
            $scope.environmentCount = 0;
            $scope.loadingCounts = false;
        });
    };

    // Load Recent Audit Logs
    const loadRecentChanges = function() {
        $scope.loadingLogs = true;
        
        $http.get('http://localhost:8001/api/audit-logs/?limit=5')
            .then(function(response) {
                $scope.recentChanges = response.data.results || response.data || [];
                $scope.loadingLogs = false;
            })
            .catch(function(error) {
                console.error('Error fetching audit logs:', error);
                $scope.recentChanges = [];
                $scope.loadingLogs = false;
            });
    };

    // Initialize Data Loading
    loadAllCounts();
    loadRecentChanges();

    // Chart Configuration and Rendering
    $timeout(function() {
        if ($scope.instanceCount > 0 || $scope.credentialCount > 0 || $scope.environmentCount > 0) {
            renderJobChart();
        }
    }, 1000);

    function renderJobChart() {
        const ctx = document.getElementById('JobChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Instances', 'Credentials', 'Environments'],
                    datasets: [{
                        data: [$scope.instanceCount, $scope.credentialCount, $scope.environmentCount],
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }
});