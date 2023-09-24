
// Import libraries
const express = require('express');

//Import database file
const database = require("./database.js");



//Import python shells
const {PythonShell} = require('python-shell')


// Create express application
const app = express();
const cors = require("cors");


app.use(cors());
app.use(express.json());


//Server listens for requests on port 8000
app.listen(8000, () => {
    console.log(`Server is running on port 8000.`);
  });

// Access database module
var count_val = 1;
async function getDatabaseReadings(){
    var myData = await database.run()
    console.log(myData);
    count_val = count_val+ 1;
    console.log("got data " + count_val)

    return myData
}
var lastUpdate = 0;
function collectData(){

    app.get('/weatherData', (req, res) =>{

        //Responds once data has been recieved
        myData = getDatabaseReadings().then(function(myData){
            res.json({ weatherData: myData})
            
        })
        
    });

    var currentDate = Date.now();

    //Updates values after 24 hours
    if (((currentDate-14400000)>=lastUpdate) || lastUpdate == 0){
        lastUpdate= Date.now()

        var pythonScriptPath = "weatherPredictor.py"
        //Runs python code from nodejs
        var pyshell = new PythonShell(pythonScriptPath);
        var results

        //Collects data printed by the python program
        pyshell.on("message", function(message){
            async function get_msg(){
                results = await message
            }
            get_msg()
        })

        //Catches any errors
        pyshell.end(function(err){
            if (err){
                throw err;
            }
        })
        
        app.get('/predictions', (req, res) =>{
            //Sends weather predictions to port 8000
            console.log(results)
            results = results.replace(/"/g, "'")
            results = results.replace(/'/g, '"')
            strToArray = JSON.parse(results)
            console.log(strToArray)
            
            res.json({predictions: strToArray})   
        });
    }
}

collectData();






