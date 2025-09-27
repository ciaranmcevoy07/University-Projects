var mongoose=require('mongoose');
var Schema = mongoose.Schema;
const { v4: uuidv4 } = require('uuid');

var PatientSchema =  new Schema({
    patientid: {type:Number, unique:true, required:true, default:uuidv4}, 
    patientname: {type: String},
    patientage: {type: Number},
})

module.exports = mongoose.model('patient', PatientSchema)