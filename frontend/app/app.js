// app.js

angular.module('towerAdminApp', ['ngRoute', 'ngResource'])

.config(function($routeProvider) {

  $routeProvider

    /* ================= Login ================= */
    .when('/login', {
      template: `
        <div class="login-container">
          <div class="login-card">
            <div class="login-header">
              <h1 class="login-title">AAP Administration</h1>
              <p class="login-subtitle">Sign in to your account</p>
            </div>
            
            <form ng-submit="login()" class="login-form" novalidate>
              <div class="form-group">
                <label for="username">Username</label>
                <input 
                  type="text" 
                  id="username"
                  ng-model="credentials.username" 
                  placeholder="Enter your username"
                  ng-focus="clearError()"
                  required 
                />
              </div>
              
              <div class="form-group">
                <label for="password">Password</label>
                <input 
                  type="password" 
                  id="password"
                  ng-model="credentials.password" 
                  placeholder="Enter your password"
                  ng-focus="clearError()"
                  required 
                />
              </div>
              
              <div ng-if="loginError" class="error-message">
                {{loginError}}
              </div>
              
              <button type="submit" class="login-btn" ng-disabled="isLogging">
                <span ng-if="!isLogging">Sign In</span>
                <span ng-if="isLogging">Signing In...</span>
              </button>
            </form>
            
            <div class="login-footer">
              <p>Default credentials: admin / admin123</p>
            </div>
          </div>
        </div>
      `,
      controller: 'LoginController'
    })

    /* ================= Dashboard ================= */
    .when('/dashboard', {
      template: `
        <div class="toast-stack">
          <div class="toast" ng-repeat="toast in toasts" ng-class="toast.type">
            <span class="icon">
              <span ng-if="toast.type === 'success'">✔</span>
              <span ng-if="toast.type === 'error'">✖</span>
              <span ng-if="toast.type === 'info'">ℹ</span>
              <span ng-if="toast.type === 'warning'">⚠</span>
            </span>
            <span class="message">{{toast.message}}</span>
            <span class="close" ng-click="closeToast(toast.id)">X</span>
          </div>
        </div>

        <div class="dashboard-container">
          <h2 class="title">Welcome to AAP Administration Dashboard</h2>
          <div ng-if="loadingCounts" class="loader"></div>

          <div class="cards-row">
            <div class="stat-card">Instances: {{instanceCount}}</div>
            <div class="stat-card">Credentials: {{credentialCount}}</div>
            <div class="stat-card">Environments: {{environmentCount}}</div>
          </div>

          <div class="card">
            <div class="recent-logs">
              <h3>Recent Changes</h3>
              <h4>The latest 5 changes</h4>
              <div ng-if="loadingLogs" class="loader"></div>
              <ul ng-if="!loadingLogs">
                <li ng-repeat="log in recentChanges">
                  <strong>{{log.user}}</strong>
                  <strong>{{log.action}}</strong> the 
                  <strong>{{log.object_type}}</strong>
                </li>
              </ul>
            </div>
          </div>

          <div class="chart-container" ng-if="!loadingCounts">
            <div class="chart-box">
              <h3>Job Chart</h3>
              <canvas id="JobChart"></canvas>
            </div>
          </div>
        </div>
      `,
      controller: 'DashboardController'
    })

    /* ================= Instances ================= */
    .when('/instances', {
      template: `
        <div class="card">
          <h2 class="title">Tower Instances</h2>
          <div class="filters">
            <label>
              Region:
              <select ng-model="filters.region">
                <option value="">All</option>
                <option ng-repeat="region in uniqueRegions">{{region}}</option>
              </select>
            </label>
            <label>
              Environment:
              <select ng-model="filters.environment">
                <option value="">All</option>
                <option ng-repeat="env in uniqueEnvironments">{{env}}</option>
              </select>
            </label>
          </div>

          <form name="instanceForm" ng-submit="addInstance()" class="instance-form" novalidate>
            <input type="text" name="name" placeholder="Name" ng-model="newInstance.name" required />
            <input type="url" name="url" placeholder="URL" ng-model="newInstance.url" required />
            <input type="text" name="username" placeholder="Username" ng-model="newInstance.username" />
            <input type="password" name="password" placeholder="Password" ng-model="newInstance.password" />
            <input type="text" name="region" placeholder="Region" ng-model="newInstance.region" required />
            <input type="text" name="environment" placeholder="Environment" ng-model="newInstance.environment" required />
            <button type="submit" ng-disabled="instanceForm.$invalid">Add Instance</button>
          </form>

          <table class="instance-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>URL</th>
                <th>Username</th>
                <th>Region</th>
                <th>Environment</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr ng-repeat="i in instances | filter:filterByRegionAndEnvironment" ng-class="{'inactive': i.status !== 'active'}">
                <td>{{i.name}}</td>
                <td><a href="{{i.url}}" target="_blank">{{i.url}}</a></td>
                <td>{{i.username}}</td>
                <td>{{i.region}}</td>
                <td>{{i.environment}}</td>
                <td>{{i.status}}</td>
                <td><button class="delete-btn" ng-click="deleteInstance(i.id)">Delete</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      `,
      controller: 'InstanceController'
    })

    /* ================= Credentials ================= */
    .when('/credentials', {
      template: `
        <div class="card">
          <h2>Manage Credentials</h2>
          <form ng-submit="addCredential()">
            <input type="text" ng-model="newCredential.name" placeholder="Name" required />
            <input type="text" ng-model="newCredential.type" placeholder="Type" required />
            <input type="text" ng-model="newCredential.username" placeholder="Username" />
            <input type="password" ng-model="newCredential.password" placeholder="Password" />
            <button type="submit">Add</button>
          </form>

          <ul>
            <li ng-repeat="c in credentials">
              {{c.name}} ({{c.type}})
              <button ng-click="deleteCredential(c.id)">Delete</button>
            </li>
          </ul>
        </div>
      `,
      controller: 'CredentialController'
    })

    /* ================= Environments ================= */
    .when('/environments', {
      template: `
        <div class="card">
          <h2>Manage Environments</h2>
          <form ng-submit="addEnvironment()">
            <input type="text" ng-model="newEnvironment.name" placeholder="Name" required />
            <input type="text" ng-model="newEnvironment.description" placeholder="Description" />
            <button type="submit">Add</button>
          </form>

          <ul>
            <li ng-repeat="e in environments">
              {{e.name}} - {{e.description}}
              <button ng-click="deleteEnvironment(e.id)">Delete</button>
            </li>
          </ul>
        </div>
      `,
      controller: 'EnvironmentController'
    })

    /* ================= Statistics ================= */
    .when('/statistics', {
      template: `
        <div class="card">
          <h2>Statistics</h2>
          <canvas id="statsChart"></canvas>
        </div>
      `,
      controller: 'StatisticsController'
    })

    /* ================= Audit Logs ================= */
    .when('/audit-logs', {
      template: `
        <div class="card">
          <h2>Audit Logs</h2>
          <input type="text" ng-model="searchUser" placeholder="Search by user" />
          <input type="text" ng-model="searchType" placeholder="Search by type" />

          <ul>
            <li ng-repeat="log in auditlogs | filter:auditFilter">
              {{log.timestamp}} - {{log.user}} - {{log.object_type}} - {{log.action}}
            </li>
          </ul>
        </div>
      `,
      controller: 'AuditlogController'
    })

    /* ================= User Management ================= */
    .when('/users', {
      template: `
        <div class="card">
          <h2>User Management</h2>
          <button ng-click="showAddForm = !showAddForm">
            {{showAddForm ? 'Cancel' : 'Add User'}}
          </button>

          <div ng-if="showAddForm">
            <input type="text" ng-model="newUser.username" placeholder="Username" />
            <input type="email" ng-model="newUser.email" placeholder="Email" />
            <select ng-model="newUser.role">
              <option value="viewer">Viewer</option>
              <option value="admin">Admin</option>
            </select>
            <button ng-click="addUser()">Save</button>
          </div>

          <ul>
            <li ng-repeat="u in users">
              {{u.username}} - {{u.email}} ({{u.role}})
              <button ng-click="updateUser(u)">Update</button>
              <button ng-click="deleteUser(u.id)">Delete</button>
            </li>
          </ul>
        </div>
      `,
      controller: 'UserMgmtController'
    })

    /* ================= Config ================= */
    .when('/config', {
      template: `
        <div class="card">
          <h2>Configuration</h2>
          <form ng-submit="saveConfig()">
            <input type="text" ng-model="config.username" placeholder="Username" required />
            <input type="password" ng-model="config.password" placeholder="Password" required />
            <label>
              <input type="checkbox" ng-model="config.ldap_enabled" /> LDAP Enabled
            </label>
            <button type="submit">Save</button>
          </form>
        </div>
      `,
      controller: 'ConfigController'
    })

    /* ================= Default ================= */
    .otherwise({
      redirectTo: '/login'
    });

})

.run(function($rootScope, $location, AuthService) {
  
  // Check authentication on route change
  $rootScope.$on('$routeChangeStart', function(event, next, current) {
    const isLoginPage = next.$$route && next.$$route.originalPath === '/login';
    
    if (!isLoginPage && !AuthService.isAuthenticated()) {
      event.preventDefault();
      $location.path('/login');
    } else if (isLoginPage && AuthService.isAuthenticated()) {
      // If user is already authenticated and tries to access login, redirect to dashboard
      event.preventDefault();
      $location.path('/dashboard');
    }
  });
  
  // Load user info if authenticated
  if (AuthService.isAuthenticated()) {
    AuthService.getUserInfo().then(function(user) {
      $rootScope.currentUser = user;
    });
  }
});