var mongoose=require('mongoose');
var Schema = mongoose.Schema;

var SensorSchema =  new Schema({
    sensorid: {type:Number, unique:true}, 
    sensornum: {type: Number, unique:true},
    type_of_sensor: {type: String}
})

module.exports = mongoose.model('sensor', SensorSchema)