        var source;

        document.addEventListener("DOMContentLoaded", function() {
            Logger.show();
            //Logger.hide();
            //Logger.open();

            log("streaming_quotes.html loaded.");
        });

        /* ported from automations.js */

        function setSymbolsList() {
            console.log("automations_autotrader.js [ setSymbolsList() ] [ entry ]");

            // Read the input value
            const symbolsInput = document.getElementById('symbols_list_input').value;

            console.log("[setSymbolsList()] [ symbols: " + symbolsInput + " ]");

            fetch('/streaming_quotes/set_symbols_list', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbols: symbolsInput })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                console.log('symbols list set:', data);
                document.getElementById('symbols_list_output').value = data;

            })
            .catch(error => console.error('Error setting quote list:', error));              
        }  

        function getSymbolsList() {
            console.log("automations_autotrader.js [ getSymbolsList() ] [ entry ]");

            fetch('/streaming_quotes/get_symbols_list', { 
                method: 'POST'       
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                console.log('symbols list get:', data);
                document.getElementById('symbols_list_output').value = data;
            })
            .catch(error => console.error('Error getting symbols list:', error));              
        }  



        function startTemplateTask(taskName) {
            console.log("celery.html [ startTask() ] [ entry ]");
            log("celery.html [ startTemplateTask() ] [ entry ]");

            document.getElementById('task_running_status_'+taskName).innerText = 'tbd';
            document.getElementById('task_status_'+taskName).innerText = 'tbd';
            document.getElementById('task_result_'+taskName).innerText = 'tbd';

            now = new Date()
            document.getElementById('task_last_update_time_'+taskName).innerText = now.toLocaleString();

            updateResponseData('Fetching ...');

            fetch('/streaming_quotes/celery_start_template_task', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({taskName})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                console.log('Task ' + taskName + ' starting:', data);
                updateResponseData(data);

                try {
                    const parsed = JSON.parse(data);

                    // Validate parameters
                    const { running_status, task_status, task_result } = parsed;

                    // Check for missing or undefined keys and set default values
                    const safeRunningStatus = running_status ?? "Unknown status";
                    const safeTaskStatus = task_status ?? "Unknown status";
                    const safeTaskResult = task_result ?? "No result";

                    // Orr ...........

                    // Safely access specific properties with default fallback values
                    const runningStatus = parsed.running_status || "No status provided";
                    const taskStatus = parsed.task_status || "No status provided";
                    const taskResult = parsed.task_result || "No result provided";

                    // Update DOM elements safely
                    document.getElementById(`task_running_status_${taskName}`).innerText = runningStatus;
                    document.getElementById(`task_status_${taskName}`).innerText = taskStatus;
                    document.getElementById(`task_result_${taskName}`).innerText = taskResult;
                    
                    now = new Date()
                    document.getElementById(`task_last_update_time_${taskName}`).innerText = now.toLocaleString();
                } catch (error) {
                    console.error("Error parsing or handling data:", error);
                    updateResponseData("Failed to process response data.");
                }        
             })
            .catch(error => {
                updateResponseData("Error: " + error);
                console.error('Error starting task:', error)
                log('Error starting task:', error)
            });            
        }

        function stopTemplateTask(taskName) {
            console.log("celery.html [ stopTask() ] [ entry ]");

            document.getElementById('task_running_status_'+taskName).innerText = 'tbd';
            document.getElementById('task_status_'+taskName).innerText = 'tbd';
            document.getElementById('task_result_'+taskName).innerText = 'tbd';

            now = new Date()
            document.getElementById('task_last_update_time_'+taskName).innerText = now.toLocaleString();

            fetch('/streaming_quotes/celery_stop_template_task', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({taskName})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                console.log('Task ' + taskName + ' stopping:', data);
                updateResponseData(data);

                try {
                    const parsed = JSON.parse(data);

                    // Validate parameters
                    const { running_status, task_status, task_result } = parsed;

                    // Check for missing or undefined keys and set default values
                    const safeRunningStatus = running_status ?? "Unknown status";
                    const safeTaskStatus = task_status ?? "Unknown status";
                    const safeTaskResult = task_result ?? "No result";

                    // Orr ...........

                    // Safely access specific properties with default fallback values
                    const runningStatus = parsed.running_status || "No status provided";
                    const taskStatus = parsed.task_status || "No status provided";
                    const taskResult = parsed.task_result || "No result provided";

                    // Update DOM elements safely
                    document.getElementById(`task_running_status_${taskName}`).innerText = runningStatus;
                    document.getElementById(`task_status_${taskName}`).innerText = taskStatus;
                    document.getElementById(`task_result_${taskName}`).innerText = taskResult;

                    now = new Date()
                    document.getElementById(`task_last_update_time_${taskName}`).innerText = now.toLocaleString();
                } catch (error) {
                    console.error("Error parsing or handling data:", error);
                    updateResponseData("Failed to process response data.");
                }        
            })
            .catch(error => {
                console.error('Error stopping task:', error)
            });            
        }  

        function statusTemplateTask(taskName) {
            console.log("celery.html [ statusTemplateTask() ] [ entry ]");
            log("celery.html [ statusTemplateTask() ] [ entry ]");

            document.getElementById('task_running_status_'+taskName).innerText = 'tbd';
            document.getElementById('task_status_'+taskName).innerText = 'tbd';
            document.getElementById('task_result_'+taskName).innerText = 'tbd';

            now = new Date()
            document.getElementById('task_last_update_time_'+taskName).innerText = now.toLocaleString();

            updateResponseData('Fetching ...');

            fetch('/streaming_quotes/celery_get_template_task_status', { 
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({taskName})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                console.log('Task ' + taskName + ' status:', data);
                updateResponseData(data);

                try {
                    const parsed = JSON.parse(data);

                    // Validate parameters
                    const { running_status, task_status, task_result } = parsed;

                    // Check for missing or undefined keys and set default values
                    const safeRunningStatus = running_status ?? "Unknown status";
                    const safeTaskStatus = task_status ?? "Unknown status";
                    const safeTaskResult = task_result ?? "No result";

                    // Orr ...........

                    // Safely access specific properties with default fallback values
                    const runningStatus = parsed.running_status || "No status provided";
                    const taskStatus = parsed.task_status || "No status provided";
                    const taskResult = parsed.task_result || "No result provided";

                    // Update DOM elements safely
                    document.getElementById(`task_running_status_${taskName}`).innerText = runningStatus;
                    document.getElementById(`task_status_${taskName}`).innerText = taskStatus;
                    document.getElementById(`task_result_${taskName}`).innerText = taskResult;

                    now = new Date()
                    document.getElementById(`task_last_update_time_${taskName}`).innerText = now.toLocaleString();
                } catch (error) {
                    console.error("Error parsing or handling data:", error);
                    updateResponseData("Failed to process response data.");
                }
            })
            .catch(error => {
                console.error('Error getting status task:', error)
            });            
        }  

        // ------------------------------------------------------------------------------//
        // ALL TASKS - STATUS AUTO REFRESH CODE (standard pattern)

        const taskCountdownTimers = {};
        const taskRefreshTimers = {};

        // Event listeners
        function onChange_taskAutoRefreshCheckbox(taskName) {
            elementId = "task_"+taskName+"_auto_refresh_checkbox";
            log("Reference elementId: " + elementId);
            const taskAutoRefreshCheckbox = document.getElementById("task_"+taskName+"_auto_refresh_checkbox");

            if (taskAutoRefreshCheckbox.checked) {
                taskStartAutoRefresh(taskName);
            } else {
                taskStopAutoRefresh(taskName);
            }
        };

        function onInput_taskRefreshFrequency(taskName) {
            const taskAutoRefreshCheckbox = document.getElementById("task_"+taskName+"_auto_refresh_checkbox");

            if (taskAutoRefreshCheckbox.checked) {
                taskStartAutoRefresh(taskName); // Restart timers with updated frequency
            }
        };

        function taskStartAutoRefresh(taskName) {
            const taskRefreshFrequencyInput = document.getElementById("task_status_"+taskName+"_refresh_frequency");
            const taskCountdownDisplay = document.getElementById("task_status_"+taskName+"_countdown");

            taskStopAutoRefresh(taskName); // Ensure no overlapping timers

            let taskRefreshFrequency = parseInt(taskRefreshFrequencyInput.value, 10);
            let timeRemaining = taskRefreshFrequency;

            // Countdown Timer
            taskCountdownTimers[taskName] = setInterval(() => {
                taskCountdownDisplay.textContent = `Next refresh in: ${timeRemaining}s`;
                timeRemaining--;

                if (timeRemaining < 0) {
                    // Refresh and reset countdown
                    statusTemplateTask(taskName);
                    taskRefreshFrequency = parseInt(taskRefreshFrequencyInput.value, 10); // Re-fetch the frequency value
                    timeRemaining = taskRefreshFrequency;
                }
            }, 1000);

            // Auto Refresh Timer (initial fetch)
            statusTemplateTask(taskName);
            taskRefreshTimers[taskName] = setInterval(() => {
                refreshFrequency = parseInt(taskRefreshFrequencyInput.value, 10); // Update the refresh frequency dynamically
                timeRemaining = refreshFrequency; // Reset countdown
                statusTemplateTask(taskName);
            }, taskRefreshFrequency * 1000);
        }

        function taskStopAutoRefresh(taskName) {
            const taskCountdownDisplay = document.getElementById("task_status_"+taskName+"_countdown");

            clearInterval(taskRefreshTimers[taskName]);
            clearInterval(taskCountdownTimers[taskName]);
            taskCountdownDisplay.textContent = "";
        }


        // ---------------------------------------------------------------------------------------------------

        // Original code - to deprecate

        function startStreamClient() {
            console.log("schwab_stream.html [ startStreamClient() ] [ entry ]");

            // Get the symbol from the input field
            // const symbol = document.getElementById('symbol').value;
            const symbol = document.getElementById('symbol').value || "";

            // Create the request payload with the symbol
            const payload = { symbol: symbol.toUpperCase() };
            console.log("schwab_stream.html [ startStreamClient() ] [ symbol: '" + symbol + "' ]");

            fetch('/streaming_quotes/schwab_start_stream_client', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
            .then(response => response.text())
            .then(data => {
                console.log('Stream Client started:', data);
                document.getElementById('stream_client_status').innerText = data;
            })
            .catch(error => console.error('Error starting stream client:', error));            
        }

        function stopStreamClient() {
            console.log("schwab_stream.html [ stopStreamClient() ] [ entry ]");
            fetch('/streaming_quotes/schwab_stop_stream_client', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Stream Client stopped:', data);
                document.getElementById('stream_client_status').innerText = data;

            })
            .catch(error => console.error('Error stopping stream client:', error));              
        }        

        /*
         deprecate

        function getLatestStreamClientData() {
            console.log("Requesting latest data from the backend");

            // Make a GET request to the backend route
            fetch('/streaming_quotes/schwab_get_latest_stream_client_data', {
                method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                let ts = new Date();
                const now = ts.toLocaleString();
                console.log('[ ' + now + ' ] Latest stream-client-data data:', data);

                // Tell user when we got data
                document.getElementById('std-update-time').innerHTML = "<b>"+now+"</b";

                // Set the latest data into the textarea
                document.getElementById('latest-stream-client-data').value = JSON.stringify(data, null, 4);
            })
            .catch(error => {
                console.error('Error fetching latest data:', error);
            });
        }
        */


        function updateStreamingQuotesTableRows(data) {
            const tableBody = document.getElementById('streaming-quotes-table-body');
            const tableHeader = document.getElementById('streaming-quotes-table-header');

            tableHeader.style.color = 'green';

            // Check if there is an existing error row and remove it if new data is valid
            const errorRow = document.querySelector(`#streaming-quotes-table-body tr[data-symbol="error"]`);
            if (errorRow) {
                tableBody.removeChild(errorRow);
            }

            if (!data || data.length === 0) {
                // Add an error row if no valid data is provided
                tableHeader.style.color = 'red';
                tableBody.innerHTML = `
                    <tr data-symbol="error">
                        <td>no data</td>
                        <td>n/a</td>
                    </tr>`;
                return;
            }
    
            data.forEach(item => {
                const existingRow = document.querySelector(`#streaming-quotes-table-body tr[data-symbol="${item.key}"]`);

                if (existingRow) {
                    // Update existing row
                    existingRow.cells[1].textContent = item.LAST_PRICE;
                } else {
                    // Add a new row
                    const row = document.createElement('tr');
                    row.setAttribute('data-symbol', item.key);

                    row.innerHTML = `
                        <td>${item.key}</td>
                        <td>${item.LAST_PRICE}</td>
                    `;

                    tableBody.appendChild(row);
                }
            });
        }


        function updateTableRows(data) {
            const tableBody = document.getElementById('update-table-body');

            data.forEach(item => {
                const existingRow = document.querySelector(`#update-table-body tr[data-symbol="${item.key}"]`);

                if (existingRow) {
                    // Update existing row
                    existingRow.cells[1].textContent = item.LAST_PRICE;
                } else {
                    // Add a new row
                    const row = document.createElement('tr');
                    row.setAttribute('data-symbol', item.key);

                    row.innerHTML = `
                        <td>${item.key}</td>
                        <td>${item.LAST_PRICE}</td>
                    `;

                    tableBody.appendChild(row);
                }
            });
        }

        function appendTableRows(data) {
            const tableBody = document.getElementById('append-table-body');

            data.forEach(item => {
                const row = document.createElement('tr');

                row.innerHTML = `
                    <td>${item.key}</td>
                    <td>${item.LAST_PRICE}</td>
                `;

                tableBody.appendChild(row);
            });
        }        

        // --------------------------------------------------------------------------------------
        // NEW way (december 2024)

        function startStreamingData() {
            console.log("schwab_stream.html [ startStreamingData() ] [ entry ]");

            if (source) {
                console.log("startStreamingData [ previous source already open ]");
                source.close();
                source = null;
            }

            console.log("startStreamingData [ create new source ]");
            source = new EventSource('/streaming_quotes/schwab_stream_latest_data');

            document.getElementById('stream_status').innerText = "Streaming start requeted";

            source.onmessage = function(event) {
                try {
                    let ts = new Date()
                    const now = ts.toLocaleString();
                    const data = JSON.parse(event.data);

                    // Debug/dev
                    console.log("[ " + now + " ] Latest streaming data: " + JSON.stringify(data, null, 4));

                    // Update latest time page updates
                    document.getElementById('streaming-data-update-time').innerHTML = "<b>"+now+"</b>";

                    // Indicate the stream has started
                    document.getElementById('stream_status').innerText = "Streaming started.";

                    // Update 'pre' area on page
                    //document.getElementById('streaming-data').innerText = JSON.stringify(data, null, 4);

                    // Use 'value' instead of 'innerHTML' to get the data to look right
                    //document.getElementById('streaming-data2').value = JSON.stringify(data, null, 4);
                    

                    try {
                        const data = JSON.parse(event.data);

                        console.log("DATA: " , data);

                        // Update the first table (dynamic updates)
                        //updateTableRows(data);
                        if (data.status) {
                            updateStreamingQuotesTableRows(null);
                        } else {
                            updateStreamingQuotesTableRows(data);    
                        }

                        

                        // Add rows to the second table (append-only)
                        //appendTableRows(data);
                    } catch (error) {
                        console.error("Error parsing JSON data:", error);
                        updateResponseData("Error parsing JSON data:" + error);
                    }                    

                } catch (error) {
                    console.error("Error parsing JSON data:", error);
                    // deprecate
                    //document.getElementById('streaming-data').innerText = "Error parsing JSON data:" + error;
                    updateResponseData("Error parsing JSON data:" + error);

                }
            };

            source.onerror = function(e) {
                document.getElementById('stream_status').innerText = "Streaming connection error.";

                console.error("Error with the event source connection: " , e);
            }

/*

            fetch('/schwab_start_stream_latest_data', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Streaming started:', data);
                document.getElementById('stream_status').innerText = data;
            })
            .catch(error => console.error('Error starting streaming data:', error));
*/            
        }

        function stopStreamingData() {
            console.log("schwab_stream.html [ stopStreamingData() ] [ entry ]");

            if (!source) {
                document.getElementById('stream_status').innerText = "Streaming is not running.  Nothing to do.";
                return

            }

            document.getElementById('stream_status').innerText = "Streaming requested stop.";

            fetch('/streaming_quotes/schwab_stop_stream_latest_data', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Streaming stopped:', data);

                document.getElementById('stream_status').innerText = "Streaming stopped.";

                source.close();  // Close the EventSource connection
                source = null;   // unset the variable so we can re-start the connection if we want                
                document.getElementById('stream_status').value = data;
            })
            .catch(error => console.error('Error stopping streaming data:', error));              
        }


