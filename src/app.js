const express = require("express");
const app = express();
const path = require("path");
const hbs = require("hbs");
const User = require("./models/usermessage");
const bodyParser = require("body-parser");
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

require("./db/conn");
const port = process.env.PORT || 3001
const staticpath = path.join(__dirname, "../public");
const templatepath = path.join(__dirname, "../templates/views");
const partialpath = path.join(__dirname, "../templates/partials");
const pythonScriptPath = path.join(__dirname, 'E:\HRD\ntlk3.py');

app.use(express.json());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use("/css", express.static(path.join(__dirname, "../node_modules/bootstrap/dist/css")));
app.use("/js", express.static(path.join(__dirname, "../node_modules/bootstrap/dist/js")));
app.use("/jq", express.static(path.join(__dirname, "../node_modules/jquery/dist")));
app.use(express.static(staticpath));



app.set("view engine", "hbs");
app.set("views", templatepath);
hbs.registerPartials(partialpath)


app.get("/", (req, res) => {
    res.render("index");
})

app.get("/contact", (req, res) => {
    res.render("contact");
})
app.get("/login", (req, res) => {
    res.render("login");
})

app.post("/contact", async (req, res) => {
    try {
        //res.send(req.body)
        const userData = new User(req.body);
        await userData.save();
        res.status(201).render("index");
    } catch (error) {
        res.status(500).send(error);
    }


})

app.post('/sentiment-analysis', upload.single('csvFile'), async (req, res) => {
    try {
        if (!req.file) {
            console.log('No file uploaded.'); // Debugging
            return res.status(400).send('No file uploaded.');
        }
        const csvFilePath = req.file.path; // Get the path of the uploaded CSV file
        console.log('CSV file path:', csvFilePath); // Debugging

        // Now, you can use child_process to run your Python script
        const { spawn } = require('child_process');
        const pythonProcess = spawn('python', ['E:/Temp/nodejsproject/ntlk3.py', csvFilePath]);

        let scriptOutput = ''; // Store the output from the script

        pythonProcess.stdout.on('data', (data) => {
            // Capture the data (emotion counts) printed by the Python script
            scriptOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                // Parse the scriptOutput and format it as an object
                const sentimentData = parseSentimentData(scriptOutput);

                // Send the formatted data as JSON response
                res.json(sentimentData);
            } else {
                // Script encountered an error, send an error response
                console.error(`Script execution failed with code ${code}`);
                res.status(500).json({ error: 'Script execution failed' });
            }
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Function to parse the sentiment data from the script output
function parseSentimentData(scriptOutput) {
    const lines = scriptOutput.trim().split('\n');
    const sentimentData = {
        'Emotion Counts': {}
    };

    lines.forEach((line) => {
        const parts = line.split(':');
        const key = parts[0].trim();
        const value = parseInt(parts[1].trim(), 10);

        if (key === 'Total Count') {
            sentimentData['Total Count'] = value;
        } else {
            sentimentData['Emotion Counts'][key] = value;
        }
    });

    return sentimentData;
}

app.listen(port, () => {
    console.log(`server is running at port ${port}`);
});