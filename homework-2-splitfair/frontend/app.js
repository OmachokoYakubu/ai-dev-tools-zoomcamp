// SplitFair Frontend Client
// Default backend URL: http://localhost:8000
const API_BASE = window.API_BASE || 'http://localhost:8000';

// Mock state fallback if backend server is not running
const mockStore = {
    groups: [
        {
            id: 1,
            title: "Lake Tahoe Trip 2026",
            description: "Cabin rental, groceries, and ski passes",
            currency: "USD",
            created_at: new Date().toISOString()
        }
    ],
    members: {
        1: [
            { id: 1, group_id: 1, name: "Alice Smith", email: "alice@example.com" },
            { id: 2, group_id: 1, name: "Bob Jones", email: "bob@example.com" },
            { id: 3, group_id: 1, name: "Charlie Davis", email: "charlie@example.com" }
        ]
    },
    expenses: {
        1: [
            {
                id: 1,
                group_id: 1,
                title: "Cabin Rental Deposit",
                amount: 300.00,
                category: "Rent & Utilities",
                payer_id: 1,
                payer_name: "Alice Smith",
                split_member_ids: [1, 2, 3],
                created_at: new Date(Date.now() - 86400000).toISOString()
            },
            {
                id: 2,
                group_id: 1,
                title: "Groceries & Snacks",
                amount: 90.00,
                category: "Groceries",
                payer_id: 2,
                payer_name: "Bob Jones",
                split_member_ids: [1, 2, 3],
                created_at: new Date(Date.now() - 43200000).toISOString()
            }
        ]
    }
};

let currentGroupId = 1;
let currentMembers = [];
let isBackendLive = false;

// DOM Elements
const statusBadge = document.getElementById('backend-status');
const groupSelect = document.getElementById('group-select');
const totalSpentEl = document.getElementById('total-spent');
const memberCountEl = document.getElementById('member-count');
const memberPreviewEl = document.getElementById('member-list-preview');
const settlementCountEl = document.getElementById('settlement-count');
const expenseListEl = document.getElementById('expense-list');
const balanceListEl = document.getElementById('balance-list');
const settlementListEl = document.getElementById('settlement-list');

// Modals
const modalExpense = document.getElementById('modal-expense');
const modalGroup = document.getElementById('modal-group');
const expensePayerSelect = document.getElementById('expense-payer');
const splitMembersContainer = document.getElementById('split-members-container');

// API Helper with automatic mock fallback
async function apiCall(endpoint, options = {}) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (res.ok) {
            isBackendLive = true;
            updateStatusBadge(true);
            return await res.json();
        }
        throw new Error(`HTTP ${res.status}`);
    } catch (err) {
        // Fallback to client-side mock logic
        isBackendLive = false;
        updateStatusBadge(false);
        return handleMockApi(endpoint, options);
    }
}

function updateStatusBadge(live) {
    if (live) {
        statusBadge.textContent = '● Backend Connected (http://localhost:8000)';
        statusBadge.style.color = '#10b981';
    } else {
        statusBadge.textContent = '● Mock Mode (Backend Offline)';
        statusBadge.style.color = '#f59e0b';
    }
}

// Client-side Mock Implementation
function handleMockApi(endpoint, options = {}) {
    const method = options.method || 'GET';
    const body = options.body ? JSON.parse(options.body) : null;

    if (endpoint === '/api/groups' && method === 'GET') {
        return mockStore.groups;
    }
    if (endpoint === '/api/groups' && method === 'POST') {
        const newGroup = {
            id: mockStore.groups.length + 1,
            title: body.title,
            description: body.description || '',
            currency: body.currency || 'USD',
            created_at: new Date().toISOString()
        };
        mockStore.groups.push(newGroup);
        mockStore.members[newGroup.id] = [];
        mockStore.expenses[newGroup.id] = [];
        return newGroup;
    }
    if (endpoint.match(/\/api\/groups\/(\d+)$/) && method === 'GET') {
        const gId = parseInt(endpoint.split('/')[3]);
        const g = mockStore.groups.find(x => x.id === gId) || mockStore.groups[0];
        return { ...g, members: mockStore.members[g.id] || [] };
    }
    if (endpoint.match(/\/api\/groups\/(\d+)\/members$/) && method === 'POST') {
        const gId = parseInt(endpoint.split('/')[3]);
        const mList = mockStore.members[gId] || [];
        const newM = { id: mList.length + 1, group_id: gId, name: body.name, email: body.email };
        mList.push(newM);
        mockStore.members[gId] = mList;
        return newM;
    }
    if (endpoint.match(/\/api\/groups\/(\d+)\/expenses$/) && method === 'GET') {
        const gId = parseInt(endpoint.split('/')[3]);
        return mockStore.expenses[gId] || [];
    }
    if (endpoint.match(/\/api\/groups\/(\d+)\/expenses$/) && method === 'POST') {
        const gId = parseInt(endpoint.split('/')[3]);
        const expList = mockStore.expenses[gId] || [];
        const members = mockStore.members[gId] || [];
        const payer = members.find(m => m.id === body.payer_id);
        const newExp = {
            id: expList.length + 1,
            group_id: gId,
            title: body.title,
            amount: parseFloat(body.amount),
            category: body.category || 'General',
            payer_id: body.payer_id,
            payer_name: payer ? payer.name : 'Unknown',
            split_member_ids: body.split_member_ids,
            created_at: new Date().toISOString()
        };
        expList.push(newExp);
        mockStore.expenses[gId] = expList;
        return newExp;
    }
    if (endpoint.match(/\/api\/groups\/(\d+)\/balances$/) && method === 'GET') {
        const gId = parseInt(endpoint.split('/')[3]);
        return calculateMockBalances(gId);
    }
    if (endpoint.match(/\/api\/groups\/(\d+)\/settle$/) && method === 'POST') {
        const gId = parseInt(endpoint.split('/')[3]);
        const expList = mockStore.expenses[gId] || [];
        const fromM = (mockStore.members[gId] || []).find(m => m.id === body.from_member_id);
        const toM = (mockStore.members[gId] || []).find(m => m.id === body.to_member_id);
        const settleExp = {
            id: expList.length + 1,
            group_id: gId,
            title: `Settlement: ${fromM?.name || 'User'} paid ${toM?.name || 'User'}`,
            amount: parseFloat(body.amount),
            category: 'Settlement',
            payer_id: body.from_member_id,
            payer_name: fromM?.name || 'User',
            split_member_ids: [body.to_member_id],
            created_at: new Date().toISOString()
        };
        expList.push(settleExp);
        mockStore.expenses[gId] = expList;
        return settleExp;
    }
    return {};
}

// Calculate Net Balances and Optimal Settlements
function calculateMockBalances(groupId) {
    const members = mockStore.members[groupId] || [];
    const expenses = mockStore.expenses[groupId] || [];

    const memberStats = {};
    members.forEach(m => {
        memberStats[m.id] = { id: m.id, name: m.name, paid: 0, share: 0 };
    });

    expenses.forEach(exp => {
        if (memberStats[exp.payer_id]) {
            memberStats[exp.payer_id].paid += exp.amount;
        }
        const splitCount = exp.split_member_ids.length;
        if (splitCount > 0) {
            const perPerson = exp.amount / splitCount;
            exp.split_member_ids.forEach(mId => {
                if (memberStats[mId]) {
                    memberStats[mId].share += perPerson;
                }
            });
        }
    });

    const balances = Object.values(memberStats).map(st => ({
        member_id: st.id,
        member_name: st.name,
        paid: Math.round(st.paid * 100) / 100,
        share: Math.round(st.share * 100) / 100,
        net_balance: Math.round((st.paid - st.share) * 100) / 100
    }));

    // Simplify debts (greedy matching)
    const debtors = balances.filter(b => b.net_balance < -0.01).map(b => ({ ...b, amount: -b.net_balance }));
    const creditors = balances.filter(b => b.net_balance > 0.01).map(b => ({ ...b, amount: b.net_balance }));
    
    debtors.sort((a, b) => b.amount - a.amount);
    creditors.sort((a, b) => b.amount - a.amount);

    const settlements = [];
    let i = 0, j = 0;
    while (i < debtors.length && j < creditors.length) {
        const debtor = debtors[i];
        const creditor = creditors[j];
        const settleAmount = Math.min(debtor.amount, creditor.amount);

        if (settleAmount > 0.01) {
            settlements.push({
                from_member_id: debtor.member_id,
                from_member_name: debtor.member_name,
                to_member_id: creditor.member_id,
                to_member_name: creditor.member_name,
                amount: Math.round(settleAmount * 100) / 100
            });
        }

        debtor.amount -= settleAmount;
        creditor.amount -= settleAmount;

        if (debtor.amount <= 0.01) i++;
        if (creditor.amount <= 0.01) j++;
    }

    return { balances, settlements };
}

// Initial Load
async function init() {
    await loadGroups();
    await loadGroupData(currentGroupId);
    setupEventListeners();
}

async function loadGroups() {
    const groups = await apiCall('/api/groups');
    groupSelect.innerHTML = '';
    groups.forEach(g => {
        const opt = document.createElement('option');
        opt.value = g.id;
        opt.textContent = g.title;
        groupSelect.appendChild(opt);
    });
    if (groups.length > 0) {
        currentGroupId = groups[0].id;
        groupSelect.value = currentGroupId;
    }
}

async function loadGroupData(groupId) {
    const groupDetail = await apiCall(`/api/groups/${groupId}`);
    currentMembers = groupDetail.members || [];

    // Render Stats
    memberCountEl.textContent = currentMembers.length;
    memberPreviewEl.textContent = currentMembers.map(m => m.name).join(', ') || 'No members';

    // Populate Modals
    populateMemberSelectors(currentMembers);

    // Load Expenses
    const expenses = await apiCall(`/api/groups/${groupId}/expenses`);
    renderExpenses(expenses);

    // Calculate Balances
    await loadBalances(groupId);
}

function populateMemberSelectors(members) {
    expensePayerSelect.innerHTML = '';
    splitMembersContainer.innerHTML = '';

    members.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m.id;
        opt.textContent = m.name;
        expensePayerSelect.appendChild(opt);

        const lbl = document.createElement('label');
        lbl.className = 'checkbox-item';
        lbl.innerHTML = `<input type="checkbox" name="split_member" value="${m.id}" checked> ${m.name}`;
        splitMembersContainer.appendChild(lbl);
    });
}

function renderExpenses(expenses) {
    let total = 0;
    expenseListEl.innerHTML = '';

    if (!expenses || expenses.length === 0) {
        expenseListEl.innerHTML = '<div class="empty-state">No expenses recorded yet. Click "+ Add Expense" to start!</div>';
        totalSpentEl.textContent = '$0.00';
        return;
    }

    expenses.forEach(exp => {
        total += exp.amount;
        const item = document.createElement('div');
        item.className = 'expense-item';
        item.innerHTML = `
            <div>
                <div class="expense-title">${escapeHtml(exp.title)}</div>
                <div class="expense-meta">
                    Paid by <strong>${escapeHtml(exp.payer_name || 'Member ' + exp.payer_id)}</strong> 
                    &bull; Category: ${escapeHtml(exp.category || 'General')}
                    &bull; ${new Date(exp.created_at).toLocaleDateString()}
                </div>
            </div>
            <div class="expense-amount">$${exp.amount.toFixed(2)}</div>
        `;
        expenseListEl.appendChild(item);
    });

    totalSpentEl.textContent = `$${total.toFixed(2)}`;
}

async function loadBalances(groupId) {
    const data = await apiCall(`/api/groups/${groupId}/balances`);
    const balances = data.balances || [];
    const settlements = data.settlements || [];

    settlementCountEl.textContent = settlements.length;

    // Render Balances
    balanceListEl.innerHTML = '';
    if (balances.length === 0) {
        balanceListEl.innerHTML = '<div class="empty-state">No balances calculated.</div>';
    } else {
        balances.forEach(b => {
            const row = document.createElement('div');
            row.className = 'balance-row';
            let classColor = 'balance-zero';
            let sign = '';
            if (b.net_balance > 0.01) {
                classColor = 'balance-pos';
                sign = '+';
            } else if (b.net_balance < -0.01) {
                classColor = 'balance-neg';
            }
            row.innerHTML = `
                <div><strong>${escapeHtml(b.member_name)}</strong> (Paid: $${b.paid.toFixed(2)}, Share: $${b.share.toFixed(2)})</div>
                <div class="${classColor}">${sign}$${b.net_balance.toFixed(2)}</div>
            `;
            balanceListEl.appendChild(row);
        });
    }

    // Render Settlements
    settlementListEl.innerHTML = '';
    if (settlements.length === 0) {
        settlementListEl.innerHTML = '<div class="empty-state">All accounts are settled up! 🎉</div>';
    } else {
        settlements.forEach(s => {
            const card = document.createElement('div');
            card.className = 'settlement-card';
            card.innerHTML = `
                <div class="settlement-text">
                    <strong>${escapeHtml(s.from_member_name)}</strong> pays <strong>${escapeHtml(s.to_member_name)}</strong>
                </div>
                <button class="btn btn-sm btn-primary" onclick="settleDebt(${s.from_member_id}, ${s.to_member_id}, ${s.amount})">
                    Settle $${s.amount.toFixed(2)}
                </button>
            `;
            settlementListEl.appendChild(card);
        });
    }
}

window.settleDebt = async function(fromId, toId, amount) {
    await apiCall(`/api/groups/${currentGroupId}/settle`, {
        method: 'POST',
        body: JSON.stringify({
            from_member_id: fromId,
            to_member_id: toId,
            amount: amount
        })
    });
    await loadGroupData(currentGroupId);
};

function setupEventListeners() {
    groupSelect.addEventListener('change', (e) => {
        currentGroupId = parseInt(e.target.value);
        loadGroupData(currentGroupId);
    });

    // Modals
    document.getElementById('btn-open-expense-modal').addEventListener('click', () => {
        modalExpense.classList.remove('hidden');
    });
    document.getElementById('modal-close').addEventListener('click', () => {
        modalExpense.classList.add('hidden');
    });
    document.getElementById('btn-cancel-expense').addEventListener('click', () => {
        modalExpense.classList.add('hidden');
    });

    document.getElementById('btn-new-group').addEventListener('click', () => {
        modalGroup.classList.remove('hidden');
    });
    document.getElementById('modal-group-close').addEventListener('click', () => {
        modalGroup.classList.add('hidden');
    });
    document.getElementById('btn-cancel-group').addEventListener('click', () => {
        modalGroup.classList.add('hidden');
    });

    document.getElementById('btn-refresh-balances').addEventListener('click', () => {
        loadBalances(currentGroupId);
    });

    // Form Add Expense
    document.getElementById('form-add-expense').addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('expense-title').value.trim();
        const amount = parseFloat(document.getElementById('expense-amount').value);
        const category = document.getElementById('expense-category').value;
        const payer_id = parseInt(expensePayerSelect.value);

        const checkedBoxes = document.querySelectorAll('input[name="split_member"]:checked');
        const split_member_ids = Array.from(checkedBoxes).map(cb => parseInt(cb.value));

        if (split_member_ids.length === 0) {
            alert('Please select at least one member to split with.');
            return;
        }

        await apiCall(`/api/groups/${currentGroupId}/expenses`, {
            method: 'POST',
            body: JSON.stringify({
                title, amount, category, payer_id, split_member_ids
            })
        });

        modalExpense.classList.add('hidden');
        document.getElementById('form-add-expense').reset();
        await loadGroupData(currentGroupId);
    });

    // Form Add Group
    document.getElementById('form-add-group').addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('group-title').value.trim();
        const description = document.getElementById('group-desc').value.trim();
        const membersStr = document.getElementById('group-members-input').value.trim();
        const memberNames = membersStr.split(',').map(n => n.trim()).filter(n => n.length > 0);

        const group = await apiCall('/api/groups', {
            method: 'POST',
            body: JSON.stringify({ title, description, currency: 'USD' })
        });

        for (const name of memberNames) {
            await apiCall(`/api/groups/${group.id}/members`, {
                method: 'POST',
                body: JSON.stringify({ name, email: `${name.toLowerCase().replace(/\s+/g, '')}@example.com` })
            });
        }

        modalGroup.classList.add('hidden');
        document.getElementById('form-add-group').reset();
        await loadGroups();
        currentGroupId = group.id;
        groupSelect.value = group.id;
        await loadGroupData(group.id);
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    })[m]);
}

// Kickoff
window.addEventListener('DOMContentLoaded', init);
