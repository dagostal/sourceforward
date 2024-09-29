const express = require('express');
const { exec } = require('child_process'); // Import exec from child_process
const bodyParser = require('body-parser'); // Import body-parser
const app = express();
const port = process.env.PORT || 3000; // You can change this to any port you want

app.use(bodyParser.json()); // Enable parsing of JSON bodies

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

// Endpoint to run Python script
app.get('/run-script', (req, res) => {
    const scriptPath = './scraper.py'; // Replace with the path to your Python script

    exec(`python3 -W ignore ${scriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error.message}`);
            return res.status(500).send(`Error: ${error.message}`);
        }
        if (stderr) {
            // console.error(`Script stderr: ${stderr}`);
            // return res.status(500).send(`Script Error!!: ${stderr}`);
        }
        console.log("---")
        console.log(`Script output: ${stdout}`);
        const data = stdout
        .replace(/\n/g, ', ') // Replace new lines with commas
        .replace(/(\w+)\s+([^,]+)/g, '"$1": "$2"') // Convert to key-value pairs
        .replace(/,\s*}/g, '}') // Clean up trailing commas
        .replace(/},\s*{/g, '}, {'); // Clean up object separators
   
        try {
            // Attempt to parse stdout directly as JSON
            const jsonObject = JSON.parse(stdout);
                       
            // Pretty print the JSON object
            console.log('Parsed JSON:', JSON.stringify(jsonObject, null, 2));
           
            // Set the response header and send the formatted JSON
            res.setHeader('Content-Type', 'application/json');
            res.send(JSON.stringify(jsonObject, null, 2)); // Send formatted JSON
        } catch (e) {
            console.error('Error parsing JSON:', e);
            return res.status(500).send('Error parsing JSON output');
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});