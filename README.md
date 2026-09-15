!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Employee Leave Management</title>
  <style>
    :root {
      --primary: #0d6efd;
      --primary-dark: #0b5ed7;
      --success: #198754;
      --danger: #dc3545;
      --warning: #ffc107;
      --light: #f8f9fa;
      --dark: #212529;
      --muted: #6c757d;
      --border: #dee2e6;
      --bg: #eef3f9;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--bg);
      color: var(--dark);
    }

    .navbar {
      background: var(--primary);
      color: white;
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    .brand {
      font-size: 1.4rem;
      font-weight: bold;
      letter-spacing: 0.3px;
    }

    .nav-actions {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .btn {
      border: none;
      border-radius: 8px;
      padding: 10px 16px;
      cursor: pointer;
      font-size: 0.96rem;
      transition: 0.2s ease;
      display: inline-block;
      text-decoration: none;
      text-align: center;
    }

    .btn-primary {
      background: var(--primary);
      color: white;
    }

    .btn-primary:hover { background: var(--primary-dark); }

    .btn-success {
      background: var(--success);
      color: white;
    }

    .btn-danger {
      background: var(--danger);
      color: white;
    }

    .btn-warning {
      background: var(--warning);
      color: var(--dark);
    }

    .container {
      max-width: 1100px;
      margin: 28px auto;
      padding: 0 18px;
    }

    .card {
      background: white;
      border: 1px solid var(--border);
      border-radius: 12px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.05);
      padding: 22px;
    }

    .login-wrap {
      max-width: 460px;
      margin: 40px auto;
    }

    h2, h3 {
      margin-top: 0;
      margin-bottom: 18px;
    }

    .form-group {
      margin-bottom: 16px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
    }

    input, select, textarea {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 1rem;
      outline: none;
    }

    input:focus, select:focus, textarea:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(13,110,253,0.15);
    }

    .alert {
      border-radius: 8px;
      padding: 12px 14px;
      margin-bottom: 16px;
      font-size: 0.95rem;
    }

    .alert-success { background: #d1e7dd; color: #0f5132; }
    .alert-danger { background: #f8d7da; color: #842029; }

    .dashboard-grid {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 20px;
    }

    .summary-box {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--light);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 15px 18px;
      margin-bottom: 20px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
    }

    th, td {
      border-bottom: 1px solid var(--border);
      padding: 12px 10px;
      text-align: left;
      vertical-align: top;
    }

    th {
      background: var(--light);
    }

    .badge {
      display: inline-block;
      padding: 5px 10px;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 600;
    }

    .badge-pending { background: #fff3cd; color: #664d03; }
    .badge-approved { background: #d1e7dd; color: #0f5132; }
    .badge-rejected { background: #f8d7da; color: #842029; }

    .actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 10px;
    }

    .small-note {
      background: #f8f9fa;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
      color: var(--muted);
      line-height: 1.5;
    }

    .hidden { display: none !important; }

    @media (max-width: 800px) {
      .dashboard-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <nav class="navbar">
    <div class="brand">Employee Leave Management</div>
    <div class="nav-actions">
      <span id="userLabel"></span>
      <button id="logoutBtn" class="btn btn-danger hidden">Logout</button>
    </div>
  </nav>

  <div class="container">
    <div id="alertBox" class="alert hidden"></div>

    <section id="loginSection" class="card login-wrap">
      <h2>Login</h2>
      <form id="loginForm">
        <div class="form-group">
          <label for="username">Username</label>
          <input id="username" name="username" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" name="password" type="password" required />
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%;">Login</button>
      </form>
      <hr />
      <div class="small-note">
        <strong>Demo accounts</strong><br />
        Employee: employee / employee123<br />
        Admin: admin / admin123
      </div>
    </section>

    <section id="dashboardSection" class="hidden">
      <div id="employeeDashboard" class="hidden">
        <div class="summary-box">
          <h3>Employee Dashboard</h3>
          <button class="btn btn-primary" id="showLeaveFormBtn">Apply Leave</button>
        </div>

        <div id="leaveFormCard" class="card hidden" style="margin-bottom: 20px;">
          <h3>Apply for Leave</h3>
          <form id="leaveForm">
            <div class="form-group">
              <label>Leave Type</label>
              <select id="leaveType" required>
                <option value="">Select</option>
                <option>Casual Leave</option>
                <option>Sick Leave</option>
                <option>Annual Leave</option>
                <option>Personal Leave</option>
              </select>
            </div>
            <div class="form-group">
              <label>Start Date</label>
              <input type="date" id="startDate" required />
            </div>
            <div class="form-group">
              <label>End Date</label>
              <input type="date" id="endDate" required />
            </div>
            <div class="form-group">
              <label>Reason</label>
              <textarea id="reason" rows="3" required></textarea>
            </div>
            <button type="submit" class="btn btn-success">Submit Leave Request</button>
          </form>
        </div>

        <div class="card">
          <h3>Your Leave Requests</h3>
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Dates</th>
                <th>Reason</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="employeeLeavesTable"></tbody>
          </table>
        </div>
      </div>

      <div id="adminDashboard" class="hidden">
        <div class="summary-box">
          <h3>Admin Dashboard</h3>
        </div>

        <div class="card">
          <h3>All Leave Requests</h3>
          <table>
            <thead>
              <tr>
                <th>Employee</th>
                <th>Type</th>
                <th>Dates</th>
                <th>Reason</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="adminLeavesTable"></tbody>
          </table>
        </div>
      </div>
    </section>
  </div>

  <script>
    const STORAGE_KEY = 'employee-leave-app';

    const defaultData = {
      users: [
        {
          username: 'employee',
          password: 'employee123',
          role: 'employee',
          name: 'Demo Employee',
          email: 'employee@example.com'
        },
        {
          username: 'admin',
          password: 'admin123',
          role: 'admin',
          name: 'System Administrator',
          email: 'admin@example.com'
        }
      ],
      leaves: []
    };

    const appState = {
      currentUser: null,
      data: loadData()
    };

    const loginSection = document.getElementById('loginSection');
    const dashboardSection = document.getElementById('dashboardSection');
    const alertBox = document.getElementById('alertBox');
    const logoutBtn = document.getElementById('logoutBtn');
    const userLabel = document.getElementById('userLabel');
    const employeeDashboard = document.getElementById('employeeDashboard');
    const adminDashboard = document.getElementById('adminDashboard');
    const leaveFormCard = document.getElementById('leaveFormCard');
    const showLeaveFormBtn = document.getElementById('showLeaveFormBtn');

    function loadData() {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultData));
        return JSON.parse(JSON.stringify(defaultData));
      }
      try {
        return JSON.parse(raw);
      } catch {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultData));
        return JSON.parse(JSON.stringify(defaultData));
      }
    }

    function saveData() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(appState.data));
    }

    function showAlert(message, type = 'success') {
      alertBox.textContent = message;
      alertBox.className = `alert alert-${type}`;
      alertBox.classList.remove('hidden');
    }

    function hideAlert() {
      alertBox.classList.add('hidden');
    }

    function isLoggedIn() {
      return !!appState.currentUser;
    }

    function setLoggedInUser(user) {
      appState.currentUser = user;
      userLabel.textContent = user.name + ' (' + user.role + ')';
      logoutBtn.classList.remove('hidden');
      loginSection.classList.add('hidden');
      dashboardSection.classList.remove('hidden');

      if (user.role === 'admin') {
        employeeDashboard.classList.add('hidden');
        adminDashboard.classList.remove('hidden');
      } else {
        adminDashboard.classList.add('hidden');
        employeeDashboard.classList.remove('hidden');
        renderEmployeeLeaves();
      }

      renderAdminLeaves();
    }

    function logout() {
      appState.currentUser = null;
      userLabel.textContent = '';
      logoutBtn.classList.add('hidden');
      dashboardSection.classList.add('hidden');
      loginSection.classList.remove('hidden');
      document.getElementById('loginForm').reset();
      hideAlert();
    }

    function renderEmployeeLeaves() {
      const tbody = document.getElementById('employeeLeavesTable');
      const myLeaves = appState.data.leaves.filter(item => item.employeeUsername === appState.currentUser.username);

      if (!myLeaves.length) {
        tbody.innerHTML = '<tr><td colspan="4">No leave requests yet.</td></tr>';
        return;
      }

      tbody.innerHTML = myLeaves.map(item => `
        <tr>
          <td>${item.leaveType}</td>
          <td>${item.startDate} to ${item.endDate}</td>
          <td>${item.reason}</td>
          <td><span class="badge badge-${item.status.toLowerCase()}">${item.status}</span></td>
        </tr>
      `).join('');
    }

    function renderAdminLeaves() {
      const tbody = document.getElementById('adminLeavesTable');
      const leaves = appState.data.leaves;

      if (!leaves.length) {
        tbody.innerHTML = '<tr><td colspan="6">No leave requests available.</td></tr>';
        return;
      }

      tbody.innerHTML = leaves.map(item => {
        const employee = appState.data.users.find(user => user.username === item.employeeUsername);
        const actionButtons = item.status === 'Pending' ? `
          <div class="actions">
            <button class="btn btn-success" data-action="approve" data-id="${item.id}">Approve</button>
            <button class="btn btn-danger" data-action="reject" data-id="${item.id}">Reject</button>
          </div>
        ` : '<span class="badge badge-' + item.status.toLowerCase() + '">' + item.status + '</span>';

        return `
          <tr>
            <td>${employee ? employee.name : item.employeeUsername}</td>
            <td>${item.leaveType}</td>
            <td>${item.startDate} to ${item.endDate}</td>
            <td>${item.reason}</td>
            <td><span class="badge badge-${item.status.toLowerCase()}">${item.status}</span></td>
            <td>${actionButtons}</td>
          </tr>
        `;
      }).join('');

      document.querySelectorAll('[data-action]').forEach(button => {
        button.addEventListener('click', function () {
          const id = Number(this.dataset.id);
          const action = this.dataset.action;
          updateLeaveStatus(id, action === 'approve' ? 'Approved' : 'Rejected');
        });
      });
    }

    function updateLeaveStatus(id, status) {
      const item = appState.data.leaves.find(entry => entry.id === id);
      if (!item) return;
      item.status = status;
      saveData();
      renderEmployeeLeaves();
      renderAdminLeaves();
      showAlert(`Leave request ${status.toLowerCase()} successfully.`, 'success');
    }

    document.getElementById('loginForm').addEventListener('submit', function (event) {
      event.preventDefault();
      const username = document.getElementById('username').value.trim();
      const password = document.getElementById('password').value;

      const user = appState.data.users.find(item => item.username === username && item.password === password);

      if (!user) {
        showAlert('Invalid username or password.', 'danger');
        return;
      }

      setLoggedInUser(user);
      hideAlert();
      this.reset();
    });

    showLeaveFormBtn.addEventListener('click', function () {
      leaveFormCard.classList.toggle('hidden');
    });

    document.getElementById('leaveForm').addEventListener('submit', function (event) {
      event.preventDefault();
      const leaveType = document.getElementById('leaveType').value.trim();
      const startDate = document.getElementById('startDate').value;
      const endDate = document.getElementById('endDate').value;
      const reason = document.getElementById('reason').value.trim();

      if (!leaveType || !startDate || !endDate || !reason) {
        showAlert('Please fill in all fields.', 'danger');
        return;
      }

      if (endDate < startDate) {
        showAlert('End date cannot be before start date.', 'danger');
        return;
      }

      const newId = appState.data.leaves.length ? Math.max(...appState.data.leaves.map(item => item.id)) + 1 : 1;

      appState.data.leaves.unshift({
        id: newId,
        employeeUsername: appState.currentUser.username,
        leaveType,
        startDate,
        endDate,
        reason,
        status: 'Pending'
      });

      saveData();
      renderEmployeeLeaves();
      renderAdminLeaves();
      this.reset();
      leaveFormCard.classList.add('hidden');
      showAlert('Leave request submitted successfully.', 'success');
    });

    logoutBtn.addEventListener('click', logout);

    if (isLoggedIn()) {
      setLoggedInUser(appState.currentUser);
    }
  </script>
</body>
</html>
<
