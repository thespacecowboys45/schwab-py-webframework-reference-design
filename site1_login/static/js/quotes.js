    // Utility to format a timestamp into a readable date and time
    function formatTimestamp(timestamp) {
        return new Date(timestamp).toLocaleString();
    }


    // Populate the table with parsed data
    function populateTable(data) {
        const table = document.getElementById('quote-table-body');
        const header = document.getElementById('quote-table-header');

        // Clear existing rows
        table.innerHTML = '';

        // Reset header color
        header.style.color = 'green';

        // Check for error or empty result
        if (!data || !data.result) {
            header.style.color = 'red';
            table.innerHTML = `
                <tr>
                    <td>error retrieving quote</td>
                    <td>n/a</td>
                    <td>n/a</td>
                    <td>n/a</td>
                    <td>n/a</td>
                    <td>n/a</td>
                </tr>`;
            return;
        }

        // Iterate over symbols and add rows
        for (const [symbol, details] of Object.entries(data.result)) {
            const quote = details.quote;
            table.innerHTML += `
                <tr>
                    <td>${symbol}</td>
                    <td>${quote.lastPrice ?? 'n/a'}</td>
                    <td>${quote.bidPrice ?? 'n/a'}</td>
                    <td>${quote.askPrice ?? 'n/a'}</td>
                    <td>${quote.quoteTime ? formatTimestamp(quote.quoteTime) : 'n/a'}</td>
                    <td>${quote.tradeTime ? formatTimestamp(quote.tradeTime) : 'n/a'}</td>
                </tr>`;
        }
    }

    // stub
    function getFormParams() {
        params = {"stubParamsKey":"subParamsValue"}
        return params
    }

    // stub
    function validateFormParams(params) {
        return true
    }    

    // AJAX call function
    async function submitForm(endpoint, inputId) {
        const inputField = document.getElementById(inputId);
        const inputData = inputField.value;

        updateResponseData("fetching quotes for: " + inputData); // Display response data

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input: inputData })
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();
            populateTable(data);
            updateResponseData(JSON.stringify(data, null, 2)); // Display response data

        } catch (error) {
            console.error(error);
            populateTable(null); // Pass null to indicate an error
            updateResponseData(`Failed to fetch data: ${error.message}`);

        }
    }

    function fetchData(route) {
        const params = getFormParams()
        valid = validateFormParams(params)

        if (valid) {
            submitForm(route, params);
        } else {
            alert("Form parameters are not valid");
        }

    }    
    