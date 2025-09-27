var mongoose=require('mongoose');
var Schema = mongoose.Schema;

var BloodPressSchema =  new Schema({
    systolic: {type: Number,}, 
    diastolic: {type: Number},
})
var ClinicalInfoSchema =  new Schema({
    clinicalInfoID:{type:String, unique:true},
    admDate: {type:Date}, 
    bed: {type: String},
    bodyTemp: {type: Number},
    bpm: {type: Number},
    sato2: {type: Number},
    bloodPress: {type: BloodPressSchema},
    timestamp: {type: Date}
})

module.exports = mongoose.model('clinicalinfo', ClinicalInfoSchema)