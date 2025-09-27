var mongoose=require('mongoose');
var Schema = mongoose.Schema;
const{v4:uuidv4} = require('uuid');

var BloodPressSchema =  new Schema({
    systolic: {type:Number,}, 
    diastolic: {type: Number},
})
var ClinicalInfoSchema =  new Schema({
    clinicalInfoID:{type:String, unique:true, required:true, default:uuidv4},
    admDate: {type:Date}, 
    bed: {type: String},
    bodyTemp: {type: Number},
    bpm: {type: Number},
    sato2: {type: Number},
    bloodPress: {type: BloodPressSchema},
})

module.exports = mongoose.model('clinicalinfo', ClinicalInfoSchema)