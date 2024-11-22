    // Adjust textarea height dynamically
    function adjustTextareaHeight(element) {
        element.style.height = 'auto'; // Reset the height
        element.style.height = (element.scrollHeight) + 'px'; // Set it to scrollHeight
    }

    // Update response content
    function updateResponseData(content) {
        const textarea = document.getElementById('response-data');
        textarea.value = content;
        adjustTextareaHeight(textarea); // Adjust height after content update
    }