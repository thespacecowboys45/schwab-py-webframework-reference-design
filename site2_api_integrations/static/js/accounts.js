function maskValue(value) {
    // Only show the last 'n' characters of the real value
    return "*".repeat(value.length - 4) + value.slice(-4);
}

function updateAccountNumbersTable(data, showRealValues) {
    const tableBody = document.getElementById('account-numbers-table').querySelector('tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    data.forEach(account => {
        const row = document.createElement('tr');
        const accountCell = document.createElement('td');
        const hashCell = document.createElement('td');
        const selectCell = document.createElement('td');
        const selectButton = document.createElement('button');

        const accountValue = showRealValues ? account.accountNumber : maskValue(account.accountNumber);
        const hashValue = showRealValues ? account.hashValue : maskValue(account.hashValue);

        accountCell.textContent = accountValue;
        hashCell.textContent = hashValue;
        selectButton.textContent = 'Select';
        selectButton.onclick = () => selectAccount(account.accountNumber, account.hashValue);

        selectCell.appendChild(selectButton);
        row.appendChild(accountCell);
        row.appendChild(hashCell);
        row.appendChild(selectCell);
        tableBody.appendChild(row);
    });
}

function getAccountNumbers() {
    updateResponseData("fetching data for: /get_account_numbers"); // Display response data
    
    const checkbox = document.getElementById("toggle-account-numbers-visibility");
    checkbox.checked = false; // Reset checkbox when fetching new data

    fetch('/get_account_numbers')
        .then(response => response.json())
        .then(data => {
            updateResponseData(JSON.stringify(data, null, 4));

            const tableBody = document.getElementById('account-numbers-table').querySelector('tbody');
            tableBody.innerHTML = '';  // Clear any existing rows

            updateAccountNumbersTable(data, false);

            // Handle visibility toggle when checkbox is clicked
            checkbox.onchange = () => {
                updateAccountNumbersTable(data, checkbox.checked);
            };
        })
        .catch(error => console.error('Error fetching account numbers:', error));
}

function selectAccount(accountNumber, hashValue) {
    updateResponseData("fetching data for: /select_account"); // Display response data

    fetch('/select_account', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ accountNumber, hashValue })
    })
    .then(response => response.json())
    .then(data => {
        // Not a huge fan of javascript alert()
        //alert(data.message);
        location.reload(); // Refresh to update the banner
    })
    .catch(error => console.error('Error selecting account:', error));
}

function clearAccountSelection() {
    updateResponseData("fetching data for: /clear_account_selection"); // Display response data

    fetch('/clear_account_selection', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Not a huge fan of javascript alert()
            //alert(data.message);
            location.reload(); // Refresh to update the banner
        })
        .catch(error => console.error('Error clearing account selection:', error));
}

function getAccount() {
    updateResponseData("fetching data for: /get_account"); // Display response data

    fetch('/get_account')
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // Display message in the user message banner
                const banner = document.getElementById('user-message-banner');
                // If account data exists, show success message
                banner.textContent = data.message;
                banner.style.display = 'block';

                console.log("data:",data);

                if (data.account_data) {
                    updateResponseData(JSON.stringify(data.account_data, null, 4));
                } else {
                    // If no account data, show entire response from server
                    updateResponseData(JSON.stringify(data, null, 4));
                }

                // Hide the banner after 5 seconds
                setTimeout(() => {
                    banner.style.display = 'none';
                }, 5000);
            }
        })
        .catch(error => console.error('Error fetching account:', error));
}

function getAccounts() {
    updateResponseData("fetching data for: /get_accounts"); // Display response data

    fetch('/get_accounts')
        .then(response => response.json())
        .then(data => {
            updateResponseData(JSON.stringify(data, null, 4));

            const tableBody = document.getElementById('accounts-table').querySelector('tbody');
            tableBody.innerHTML = '';  // Clear any existing rows

            data.forEach(account => {
                const row = document.createElement('tr');
                const nameCell = document.createElement('td');
                const idCell = document.createElement('td');
                const fundsCell = document.createElement('td');


                nameCell.textContent = account.aggregatedBalance.currentLiquidationValue;
                idCell.textContent = account.securitiesAccount.accountNumber;
                fundsCell.textContent = account.securitiesAccount.currentBalances.availableFunds;


                row.appendChild(nameCell);
                row.appendChild(idCell);
                row.appendChild(fundsCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching account info:', error));
}

 function getUserPreferences() {
    updateResponseData("fetching data for: /get_user_preferences"); // Display response data

    fetch('/get_user_preferences', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            updateResponseData(JSON.stringify(data, null, 4));

        })
        .catch(error => console.error('Error fetching user preferences info:', error));            
}

function getPositions() {
    updateResponseData("fetching data for: /get_positions"); // Display response data

    fetch('/get_positions', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            updateResponseData(JSON.stringify(data, null, 4));
            updatePositionsTable(data);                    
        })
        .catch(error => console.error('Error fetching user preferences info:', error));       
}            

function updatePositionsTable(data) {
    console.log("DEBUG: " , data.securitiesAccount);
    const tableBody = document.getElementById('account-positions-table-body');
    const accountNumber = data.securitiesAccount.accountNumber; // Extract account number
    const positions = data.securitiesAccount.positions || []; // Extract positions array

    // Clear existing table rows
    tableBody.innerHTML = '';

    // Check if positions exist
    if (positions.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="7" style="text-align: center;">No positions available</td>
        `;
        tableBody.appendChild(row);
        return;
    }

    // Populate table with position data
    positions.forEach(position => {
        const row = document.createElement('tr');

        // Parse the required fields from the position object
        const averagePrice = position.averagePrice || 'N/A';
        const assetType = position.instrument.assetType || 'N/A';
        const symbol = position.instrument.symbol || 'N/A';
        // additional checks to handle the fact the value may be 0.0 (which is a falsy value)
        const longQuantity = position.longQuantity !== undefined && position.longQuantity !== null ? position.longQuantity : 'N/A';
        const shortQuantity = position.shortQuantity !== undefined && position.shortQuantity !== null ? position.shortQuantity : 'N/A';
        
        const taxLotAverageLongPrice = position.taxLotAverageLongPrice || 'N/A';

        // Construct the row
        row.innerHTML = `
            <td>${accountNumber}</td>
            <td>${symbol}</td>
            <td>${assetType}</td>
            <td>${averagePrice}</td>
            <td>${longQuantity}</td>
            <td>${shortQuantity}</td>
            <td>${taxLotAverageLongPrice}</td>
        `;

        // Append row to the table body
        tableBody.appendChild(row);
    });
}

