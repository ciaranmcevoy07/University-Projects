var mongoose=require('mongoose');
var Schema = mongoose.Schema;

var PatientSchema =  new Schema({
    patientid: {type:Number, unique:true}, 
    patientname: {type: String},
    patientage: {type: Number},
})

module.exports = mongoose.model('patient', PatientSchema)