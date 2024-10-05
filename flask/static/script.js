var currentTab = '#tab1'; // Default to the first tab

window.onload = setDefaultDateTime;

function setDefaultDateTime() {
    // Get today's date and time
    const today = new Date();
    
    // Format the date and time as YYYY-MM-DDTHH:MM (T separates date and time)
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0'); // Add leading zero if needed
    const day = String(today.getDate()).padStart(2, '0'); // Add leading zero if needed
    const hours = '09'; // Set default hour to 09 (9 AM)
    const minutes = '15'; // Set default minute to 15
    const hours_end = '15'; // Set default hour to 09 (9 AM)
    const minutes_end = '30'; // Set default minute to 15

    // Combine into the required format for datetime-local
    const formattedDateTime_start = `${year}-${month}-${day}T${hours}:${minutes}`;
    const formattedDateTime_end = `${year}-${month}-${day}T${hours_end}:${minutes_end}`;
    

    // Set default date and time value to the input
    const dateTimeInput_start = document.getElementsByName('start_date');
    const dateTimeInput_end = document.getElementsByName('end_date');
    const dateTimeInput_start_1 = document.getElementsByName('start_date1');
    const dateTimeInput_end_1 = document.getElementsByName('end_date1');
    const dateTimeInput_start_2 = document.getElementsByName('start_date2');
    const dateTimeInput_end_2 = document.getElementsByName('end_date2');

    dateTimeInput_start.forEach(dateTimeInput_start => {
        dateTimeInput_start.value = formattedDateTime_start;
    });
    dateTimeInput_start_1.forEach(dateTimeInput_start_1 => {
        dateTimeInput_start_1.value = formattedDateTime_start;
    });
    dateTimeInput_start_2.forEach(dateTimeInput_start_2 => {
        dateTimeInput_start_2.value = formattedDateTime_start;
    });


    dateTimeInput_end.forEach(dateTimeInput_end => {
        dateTimeInput_end.value = formattedDateTime_end;
    });
    dateTimeInput_end_1.forEach(dateTimeInput_end_1 => {
        dateTimeInput_end_1.value = formattedDateTime_end;
    });
    dateTimeInput_end_2.forEach(dateTimeInput_end_2 => {
        dateTimeInput_end_2.value = formattedDateTime_end;
    });
};

function onSelectionChange() {
    const dropdown = document.getElementById('dropdown');
    const selectedOption = dropdown.value;

    let dayName = '';
    if (selectedOption === 'BANKNIFTY') {
        dayName = 'Wednesday';
    } else if (selectedOption === 'NIFTY') {
        dayName = 'Thursday';
    }

    const dates = getNextDates(dayName);
    displayDates(dates);
}

function getNextDates(dayName) {
    const dates = [];
    const today = new Date();
    const twoMonthsLater = new Date();
    twoMonthsLater.setMonth(today.getMonth() + 2);

    let currentDate = new Date(today);

    // Adjust to the next occurrence of the dayName
    currentDate.setDate(currentDate.getDate() + ((7 - currentDate.getDay() + getDayIndex(dayName)) % 7));

    // Collect all occurrences within the next two months
    while (currentDate <= twoMonthsLater) {
        dates.push(formatDate(currentDate));
        currentDate.setDate(currentDate.getDate() + 7); // move to next week
    }

    return dates;
}

function getDayIndex(dayName) {
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return daysOfWeek.indexOf(dayName);
}

function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = date.toLocaleString('en', { month: 'short' }).toUpperCase();
    const year = String(date.getFullYear()).slice(-2);
    return `${day}${month}${year}`;
}

function displayDates(dates) {
    const dateList = document.getElementById('dates');
    dateList.innerHTML = '';  // Clear previous dates

    if (dates.length > 0) {
        document.getElementById('dateList').style.display = 'block';
        dates.forEach((date, index) => {
            const listItem = document.createElement('li');

            const radioButton = document.createElement('input');
            radioButton.type = 'radio';
            radioButton.name = 'dateRadio';
            radioButton.value = date;
            radioButton.id = `date${index}`;
            radioButton.onclick = function() {
                updateSymbolsInput(date);
            };

            const label = document.createElement('label');
            label.htmlFor = `date${index}`;
            label.textContent = date;

            listItem.appendChild(radioButton);
            listItem.appendChild(label);
            dateList.appendChild(listItem);
        });
    } else {
        document.getElementById('dateList').style.display = 'none';
    }
}

function updateSymbolsInput(selectedDate) {
    const symbolsInput_symbols_nf = document.getElementById('symbol_nf').value;

    // Replace the date in the input field using regex pattern to match dates like '05SEP24'
    const updatedSymbols_symbols_nf = symbolsInput_symbols_nf.replace(/\d{2}[A-Z]{3}\d{2}/g, selectedDate);

    // Set the updated value back to the input field
    document.getElementById('symbol_nf').value = updatedSymbols_symbols_nf;

    const symbolsInput_symbols_sx = document.getElementById('symbol_sx').value;

    // Replace the date in the input field using regex pattern to match dates like '05SEP24'
    const updatedSymbols_symbols_sx = symbolsInput_symbols_sx.replace(/\d{2}[A-Z]{3}\d{2}/g, selectedDate);

    // Set the updated value back to the input field
    document.getElementById('symbol_sx').value = updatedSymbols_symbols_sx;
    
    const symbolsInput = document.getElementById('symbols1').value;

    // Replace the date in the input field using regex pattern to match dates like '05SEP24'
    const updatedSymbols = symbolsInput.replace(/\d{2}[A-Z]{3}\d{2}/g, selectedDate);

    // Set the updated value back to the input field
    document.getElementById('symbols1').value = updatedSymbols;

    const symbolsInput_2 = document.getElementById('symbols2').value;

    // Replace the date in the input field using regex pattern to match dates like '05SEP24'
    const updatedSymbols_2 = symbolsInput_2.replace(/\d{2}[A-Z]{3}\d{2}/g, selectedDate);

    // Set the updated value back to the input field
    document.getElementById('symbols2').value = updatedSymbols_2;
}

function autoRefreshImage(formId, imgId, url, event) {
    // Show the loader before the AJAX request
    $('#loading-screen').show();
    $('#loading-screen2').show();
    const serialized = $(formId).serialize();
    console.log('Serialized Form Data:', serialized);
    // Convert serialized data to an object
    const formDataObject = {};
    serialized.split('&').forEach(function(pair) {
        const [key, value] = pair.split('=');
        formDataObject[decodeURIComponent(key)] = decodeURIComponent(value);
    }); 
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Set time to midnight for comparison
    
    const end_date = new Date(formDataObject['end_date'] + 'T00:00:00'); // Append time to handle date string
    const end_date1 = new Date(formDataObject['end_date1'] + 'T00:00:00');
    const end_date2 = new Date(formDataObject['end_date2'] + 'T00:00:00'); 
    const isAnyDateValid = end_date >= today || end_date1 >= today || end_date2 >= today;

    if (!event){
        if(!isAnyDateValid) {
            $('#loading-screen').hide();
            $('#loading-screen2').hide();
            return; 
        }
    }
    
    $.ajax({
        url: url,
        type: 'POST',
        data: $(formId).serialize(),
        beforeSend: function() {
            // Optional: Add any pre-request logic here if needed
            console.log('Fetching data...');
        },
        success: function(response, status, xhr) {
            const lastValue = xhr.getResponseHeader('X-Last-Value');
            console.log('Last Value:', lastValue);
            
            if (lastValue === 'True' || lastValue === true) {
                const serializedData = $(formId).serialize();
                console.log('Serialized Form Data:', serializedData);
                
                // Convert serialized data to an object
                const formDataObject = {};
                serializedData.split('&').forEach(function(pair) {
                    const [key, value] = pair.split('=');
                    formDataObject[decodeURIComponent(key)] = decodeURIComponent(value);
                });
                console.log('Form Data Object:', formDataObject);

                // Access individual values from the object
                const symbol1 = formDataObject['symbol_nf'];
                const symbol2 = formDataObject['symbol_sx'];
                const startDate = formDataObject['start_date'];
                const endDate = formDataObject['end_date'];
                const resampleFreq = formDataObject['resample_freq'];
                const enable_alert = formDataObject['enable_alert'];
                const chatId = formDataObject['chatId'];
                const botToken = formDataObject['botToken'];

                console.log('Symbol 1:', symbol1);
                console.log('Symbol 2:', symbol2);
                console.log('Start Date:', startDate);
                console.log('End Date:', endDate);
                console.log('Resample Frequency:', resampleFreq);
                
                if (enable_alert) {
                    sendAlertToTelegram(symbol1, symbol2, startDate, endDate, resampleFreq, chatId, botToken);
                }
            }

            // Create blob URL for the image
            var imgBlob = new Blob([response], { type: 'image/png' });
            var imgUrl = URL.createObjectURL(imgBlob);
            $(imgId).attr('src', imgUrl);

            // Hide the loader after the image is updated
            $('#loading-screen').hide();
            $('#loading-screen2').hide();
        },
        error: function() {
            console.error('Failed to load image');
            // Hide the loader in case of error
            $('#loading-screen').hide();
        },
        xhrFields: {
            responseType: 'blob'
        }
    });
}

function autoStrike(formId, rowData, symbolInputId, callback) {
    // Show the loader before the AJAX request
    var newForm = $(formId).clone();
    newForm.find('input[name="' + symbolInputId + '"]').val(rowData);
    console.log('newForm Form newForm:', newForm);
    
    let url = '/doubleCalPrice';
    if (symbolInputId === 'symbols2') {
        url = '/ironflyPrice';
    }

    $.ajax({
        url: url,
        type: 'POST',
        data: newForm.serialize(),
        beforeSend: function() {
            console.log('Fetching data...');
        },
        success: function(response) {
            // Read values from the JSON response
            const valuesString = response.values_string;
            const pnl = response.pnl;

            console.log('Values String:', valuesString);
            console.log('P&L:', pnl);

            // If you want to return an array from values_string
            const valuesArray = valuesString.split(','); // Adjust delimiter if needed

            // Invoke the callback with valuesArray and pnl
            if (callback) {
                callback(valuesArray, pnl); // Pass both values to the callback
            }
        },
        error: function() {
            console.error('Failed to load data');
        }
    });
}

function sendAlertToTelegram(symbol1, symbol2, startDate, endDate, resampleFreq, chatId, botToken) {
    //const chatId = '1161971259'; // Replace with your Telegram chat ID
    //const botToken = '7293565324:AAFi_BVJ2c1CBQlEDTytkKRXV39KJnB7gAM'; // Replace with your Telegram bot token
    const message = `Alert set for ${symbol1} and ${symbol2} from ${startDate} to ${endDate} with resample frequency ${resampleFreq}.`;
    // Sending alert to Telegram
    fetch(`https://api.telegram.org/bot${botToken}/sendMessage?chat_id=${chatId}&text=${encodeURIComponent(message)}`)
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                console.log('Alert sent to Telegram successfully!');
            } else {
                console.log('Failed to send alert to Telegram.');
            }
        })
        .catch(error => {
            alert('Error sending alert to Telegram.');
            console.error(error);
        });
}

function onTabChange(event) {
    var selectedTab = '#' + event.target.value;
    $('.tab-content').hide(); // Hide all tabs
    $(selectedTab).show(); // Show the selected tab
    currentTab = selectedTab; // Update current tab
    updateSavedDataDropdown(); // Update the saved data dropdown for the current tab
    setDefaultDateTime()
}

setInterval(function() {
    if ($(currentTab).is(':visible')) {
        var formId, imgId, url;

        if (currentTab === '#tab1') {
            formId = '#dataForm1';
            imgId = '#graph-img-tab1';
            url = '/straddle';
        } else if (currentTab === '#tab2') {
            formId = '#dataForm2';
            imgId = '#graph-img-tab2';
            url = '/cal';
            //generateStrikePrices('symbols1', 'outputTable1');
            //generateStrikePrices('symbols2', 'outputTable2');
        } else if (currentTab === '#tab3') {
            formId = '#dataForm3';
            imgId = '#graph-img-tab3';
            url = '/trend'; 
        }else if (currentTab === '#tab4') {
            formId = '#dataForm4';
            imgId = '#graph-img-tab4';
            url = '/doubleCal'; 
        }else if (currentTab === '#tab5') {
            formId = '#dataForm5';
            imgId = '#graph-img-tab5';
            url = '/ironfly'; 
        }else if (currentTab === '#tab6') {
            formId = '#dataForm6';
            imgId = '#graph-img-tab6';
            url = '/spreadchart'; 
        }
        autoRefreshImage(formId, imgId, url, false);
    }
}, 60000); // Refresh every 10 seconds

// Function to save form data with a name
function saveFormData(formId) {
    const formData = $(formId).serializeArray();
    const dataObject = {};
    formData.forEach(item => {
        dataObject[item.name] = item.value;
    });

    const savedName = prompt("Enter a name for this save:");
    if (savedName) {
        const currentTabKey = currentTab + '-saves';
        let savedDataList = JSON.parse(localStorage.getItem(currentTabKey)) || [];
        savedDataList.push({ name: savedName, data: dataObject });
        localStorage.setItem(currentTabKey, JSON.stringify(savedDataList));
        updateSavedDataDropdown();
    }
}

// Function to load saved form data
function loadFormData(formId) {
    const savedName = $(currentTab + ' .saved-data-dropdown').val();
    if (savedName) {
        const currentTabKey = currentTab + '-saves';
        const savedDataList = JSON.parse(localStorage.getItem(currentTabKey)) || [];
        const selectedData = savedDataList.find(item => item.name === savedName);

        if (selectedData) {
            for (let key in selectedData.data) {
                $(`${formId} [name="${key}"]`).val(selectedData.data[key]);
            }
        } else {
            alert('No saved data found with that name.');
        }
    } else {
        alert('Please select saved data to load.');
    }
}

// Function to delete saved form data
function deleteFormData() {
    const savedName = $(currentTab + ' .saved-data-dropdown').val();
    if (savedName) {
        const currentTabKey = currentTab + '-saves';
        let savedDataList = JSON.parse(localStorage.getItem(currentTabKey)) || [];
        savedDataList = savedDataList.filter(item => item.name !== savedName);
        localStorage.setItem(currentTabKey, JSON.stringify(savedDataList));
        alert('Saved data deleted: ' + savedName);
        updateSavedDataDropdown();
    } else {
        alert('Please select saved data to delete.');
    }
}

// Function to update the saved data dropdown
function updateSavedDataDropdown() {
    const currentTabKey = currentTab + '-saves';
    const savedDataList = JSON.parse(localStorage.getItem(currentTabKey)) || [];
    const dropdown = $(currentTab + ' .saved-data-dropdown');
    dropdown.empty();
    dropdown.append('<option value="">Select saved data</option>');
    savedDataList.forEach(item => {
        dropdown.append(`<option value="${item.name}">${item.name}</option>`);
    });
}

$(document).ready(function() {
    // Prevent default form submissions and handle auto-refresh
    $('#dataForm1').on('submit', function(event) {
        event.preventDefault();
        autoRefreshImage('#dataForm1', '#graph-img-tab1', '/straddle', true);
    });

    $('#dataForm2').on('submit', function(event) {
        event.preventDefault();
        generateStrikePrices('symbols1', 'outputTable1');
        generateStrikePrices('symbols2', 'outputTable2');
        autoRefreshImage('#dataForm2', '#graph-img-tab2', '/cal', true);
    });

    $('#dataForm3').on('submit', function(event) {
        event.preventDefault();
        autoRefreshImage('#dataForm3', '#graph-img-tab3', '/trend', true);
    });

    $('#dataForm4').on('submit', function(event) {
        event.preventDefault();
        autoRefreshImage('#dataForm4', '#graph-img-tab4', '/doubleCal', true);
    });

    $('#dataForm5').on('submit', function(event) {
        event.preventDefault();
        autoRefreshImage('#dataForm5', '#graph-img-tab5', '/ironfly'), true;
    });

    $('#dataForm6').on('submit', function(event) {
        event.preventDefault();
        autoRefreshImage('#dataForm6', '#graph-img-tab6', '/spreadchart', true);
    });
    // Trigger initial image loads
    autoRefreshImage('#dataForm1', '#graph-img-tab1', '/straddle', true);
    autoRefreshImage('#dataForm2', '#graph-img-tab2', '/cal', true);
    autoRefreshImage('#dataForm3', '#graph-img-tab3', '/trend', true);
    autoRefreshImage('#dataForm4', '#graph-img-tab4', '/doubleCal', true);
    autoRefreshImage('#dataForm5', '#graph-img-tab5', '/ironfly', true);
    autoRefreshImage('#dataForm6', '#graph-img-tab6', '/spreadchart', true);

    // Initialize tabs
    $('.tab-content').hide(); // Hide all tabs by default
    $('#tab1').show(); // Show the first tab

    // Update saved data dropdown for the first tab
    updateSavedDataDropdown();
});


function toggleTable(tableId) {
    const table = document.getElementById(tableId);
    table.style.display = (table.style.display === 'none' || table.style.display === '') ? 'table' : 'none';
}

function generateStrikePrices(symbolInputId, outputTableId) {
    let input = document.getElementById(symbolInputId).value;
    let segments = input.split(':');
    let outputRows = [];

    // Extract the call and put segments from the input
    let strikes = segments.map(segment => {
        let match = segment.match(/(NIFTY|BANKNIFTY)-(\d+)([CP])-([\dA-Z]+)/);
        if (match) {
            return {
                symbol: match[1],
                strike: parseInt(match[2]),
                type: match[3],
                expiry: match[4],
                original: segment // Preserve the original segment
            };
        }
    }).filter(Boolean); // Remove undefined entries

    // Generate output by adjusting strike prices for both calls and puts
    for (let i = -5; i <= 5; i++) {
        let outputRow = [];

        // Preserve the input order of calls and puts
        strikes.forEach(strike => {
            let stepSize = (strike.symbol === 'NIFTY') ? 50 : 100;
            let newStrike = strike.strike + (i * stepSize);
            let newSegment = `${strike.symbol}-${newStrike}${strike.type}-${strike.expiry}`;
            outputRow.push(newSegment);
        });

        // Join the strikes with ':' and add to the output
        outputRows.push(outputRow.join(':'));
    }

    // Clear the existing table rows
    const tableBody = document.getElementById(outputTableId).getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    // Variable to track the selected row
    let selectedRowIndex = -1;

    // Populate the table with the generated rows
    outputRows.forEach((rowData, index) => {
        let row = tableBody.insertRow();

        // Create the first cell for the rowData
        let cell = row.insertCell(0);
        cell.className = 'output-row';
        cell.textContent = rowData;

        // Add two new cells for the returned values and P&L
        let returnCell = row.insertCell(1);
        let returnCell_1 = row.insertCell(2);

        // Call autoStrike and update the new cells with returned values
        autoStrike('#dataForm2', rowData, symbolInputId, function(valuesArray, pnl) {
            returnCell.textContent = valuesArray.join(', '); // Convert array to comma-separated string
            returnCell_1.textContent = pnl; // Display the P&L value
        });

        // Add click event to update input field, highlight row, and trigger an event
        row.onclick = function() {
            // Update input field with selected row data
            document.getElementById(symbolInputId).value = rowData;

            // Remove highlighting from the previously selected row
            const selectedRow = tableBody.querySelector('.selected-row');
            if (selectedRow) {
                selectedRow.classList.remove('selected-row');
            }

            // Highlight the clicked row
            row.classList.add('selected-row');
        };

        // Check if this row matches the current input value to select it by default
        if (input === rowData) {
            row.classList.add('selected-row');
            document.getElementById(symbolInputId).value = rowData; // Set input to the selected value
            selectedRowIndex = index; // Mark as selected
            console.log('Row auto-selected for ' + symbolInputId); // Debugging log
        }
    });

    // Log a message if no matching row is highlighted
    if (selectedRowIndex === -1) {
        console.log('No matching row found for ' + symbolInputId); // Debugging log
    }
}
