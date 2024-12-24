       document.addEventListener("DOMContentLoaded", function() {
            Logger.show();
            //Logger.hide();
            //Logger.open();

            log("celery_app.html loaded.");
        });

        function startTemplateTask(taskName) {
            console.log("celery.html [ startTask() ] [ entry ]");
            log("celery.html [ startTemplateTask() ] [ entry ]");

            document.getElementById('task_running_status_'+taskName).innerText = 'tbd';
            document.getElementById('task_status_'+taskName).innerText = 'tbd';
            document.getElementById('task_result_'+taskName).innerText = 'tbd';

            now = new Date()
            document.getElementById('task_last_update_time_'+taskName).innerText = now.toLocaleString();

            updateResponseData('Fetching ...');

            fetch('/celery_examples/celery_start_template_task', { 
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

            fetch('/celery_examples/celery_stop_template_task', { 
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

            fetch('/celery_examples/celery_get_template_task_status', { 
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

        // ------------------------------------------------------------------------------ 

        // DEPRECATE THESE - these point to development tools routes

        function startTask() {
            console.log("celery.html [ startTask() ] [ entry ]");
            fetch('/celery_start_task', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Task started:', data);
                document.getElementById('task_status').innerText = data;
                
            })
            .catch(error => console.error('Error starting task:', error));            
        }

        function stopTask() {
            console.log("celery.html [ stopTask() ] [ entry ]");
            fetch('/celery_stop_task', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Task stopped:', data);
                document.getElementById('task_status').innerText = data;

            })
            .catch(error => console.error('Error stopping task:', error));              
        }  

        function getTaskResult() {
            console.log("celery.html [ getTaskResult() ] [ entry ]");
            fetch('/celery_get_task_result', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Task result:', data);
                document.getElementById('task_result').innerText = data;

            })
            .catch(error => console.error('Error stopping task:', error));              
        }          

        // ------------------------------------------------------------------------------ 

        // DEPRECATE THESE - these point to development tools routes
        /*
        function startAsyncioTask() {
            console.log("celery.html [ startAsyncioTask() ] [ entry ]");
            fetch('/celery_start_asyncio_task', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Asyncio Task started:', data);
                document.getElementById('asyncio_task_status').innerText = data;
                
            })
            .catch(error => console.error('Error starting asyncio task:', error));            
        }

        function stopAsyncioTask() {
            console.log("celery.html [ stopAsyncioTask() ] [ entry ]");
            fetch('/celery_stop_asyncio_task', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Asyncio Task stopped:', data);
                document.getElementById('asyncio_task_status').innerText = data;

            })
            .catch(error => console.error('Error stopping asyncio task:', error));              
        }  

        function getAsyncioTaskResult() {
            console.log("celery.html [ getAsyncioTaskResult() ] [ entry ]");
            fetch('/celery_get_task_asyncio_result', { 
                method: 'POST' 
            })
            .then(response => response.text())
            .then(data => {
                console.log('Asyncio Task result:', data);
                document.getElementById('asyncio_task_result').innerText = data;

            })
            .catch(error => console.error('Error stopping task:', error));              
        }   
        */

        // -------------------------------------------------------------------------------

        function getCeleryHealth() {
            console.log("celery.html [ getCeleryHealth() ] [ entry ]");
            document.getElementById('celery_health').innerText = "Checking celery health ...";

            fetch('/celery_examples/celery/health', { 
                method: 'GET' 
            })
            .then(response => response.text())
            .then(data => {
                document.getElementById('celery_health').innerText = data;

            })
            .catch(error => {
                console.error('Error stopping task:', error);
                document.getElementById('celery_health').innerText = "Error getting health: ", error;
            })
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




        // ------------------------------------------------------------------------------//
        // POLLER TASK STATUS AUTO REFRESH CODE

        /*
         Deprecated - refactored above

        let pollerTaskCountdownTimer = null; // Holds the countdown interval
        let pollerTaskAutoRefreshTimer = null; // Holds the main polling interval

        function pollerTaskStartAutoRefresh() {
            const pollerTaskRefreshFrequencyInput = document.getElementById("task_status_poller_refresh_frequency");
            const pollerTaskCountdownDisplay = document.getElementById("task_status_poller_countdown");

            pollerTaskStopAutoRefresh(); // Ensure no overlapping timers

            let pollerTaskRefreshFrequency = parseInt(pollerTaskRefreshFrequencyInput.value, 10);
            let timeRemaining = pollerTaskRefreshFrequency;

            // Countdown Timer
            pollerTaskCountdownTimer = setInterval(() => {
                pollerTaskCountdownDisplay.textContent = `Next refresh in: ${timeRemaining}s`;
                timeRemaining--;

                if (timeRemaining < 0) {
                    // Refresh and reset countdown
                    statusTemplateTask('poller');
                    pollerTaskRefreshFrequency = parseInt(pollerTaskRefreshFrequencyInput.value, 10); // Re-fetch the frequency value
                    timeRemaining = pollerTaskRefreshFrequency;
                }
            }, 1000);

            // Auto Refresh Timer (initial fetch)
            statusTemplateTask('poller');
            pollerTaskAutoRefreshTimer = setInterval(() => {
                refreshFrequency = parseInt(pollerTaskRefreshFrequencyInput.value, 10); // Update the refresh frequency dynamically
                timeRemaining = refreshFrequency; // Reset countdown
                statusTemplateTask('poller');
            }, pollerTaskRefreshFrequency * 1000);
        }

        function pollerTaskStopAutoRefresh() {
            const pollerTaskCountdownDisplay = document.getElementById("task_status_poller_countdown");

            clearInterval(pollerTaskAutoRefreshTimer);
            clearInterval(pollerTaskCountdownTimer);
            pollerTaskCountdownDisplay.textContent = "";
        }

        // Event listeners
        function onChange_pollerTaskAutoRefreshCheckbox() {
            const pollerTaskAutoRefreshCheckbox = document.getElementById("task_poller_auto_refresh_checkbox");

            if (pollerTaskAutoRefreshCheckbox.checked) {
                pollerTaskStartAutoRefresh();
            } else {
                pollerTaskStopAutoRefresh();
            }
        };

        function onInput_pollerTaskRefreshFrequency() {
            const pollerTaskAutoRefreshCheckbox = document.getElementById("task_poller_auto_refresh_checkbox");

            if (pollerTaskAutoRefreshCheckbox.checked) {
                pollerTaskStartAutoRefresh(); // Restart timers with updated frequency
            }
        };
        */

