
const mongoose = require("mongoose");

const uri = "mongodb+srv://lrosesmith23:Ziggyepq22@mystation.uoil79h.mongodb.net/weatherStationData?retryWrites=true&w=majority";
const { Schema } = mongoose;


async function connect(){
    try {
        await mongoose.connect(uri);
        console.log("Connected to MongoDB");
    } catch (error){
        console.error(error);
    }
};

//Retrieve data from the database
connect()
//Defines the structure and properties of the document
const myDataSchema = new Schema({
    timestamp: Number,
    temp: Number,
    humidity: Number,
    pressure: Number,
    altitude: Number,
    airQual: String,
    lpo_val: Number,
    dust_ratio: Number,
    dust_conc: Number,
    light: Number,
    sound: Number
}, {collection : "weather"});
async function run(){
    
    
    
    //Creates model for weather collection
    var Weather = mongoose.model('weather', myDataSchema)
    console.log("database collection")

    //Collects all data in database
    const docs = await Weather.find().sort({timestamp: -1})

    
    //Displays data in the terminal
    
    return docs
    

    
}


module.exports = {run}