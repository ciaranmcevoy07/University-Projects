const { model } = require('mongoose')
let ClinicalInfoSchema = require('../model/clinicalinfo');

module.exports.newClinicalInfo = async(clinicalInfoID, admDate, bed, bodyTemp, bpm, sato2, bloodPress, timestamp) => {
    try{
        let bloodPressureObject = {systolic, diastolic};
        let newClinicalInfo = new ClinicalInfoSchema({
            clinicalInfoID,
            admDate,
            bed,
            bodyTemp,
            bpm,
            sato2,
            bloodPressureObject,
            timestamp})
        let newClinicalInfoResponse = await newClinicalInfo.save();
        console.log(response)
        return {success: true, response: newClinicalInfoResponse};
    } catch (err){
        console.log(err)
        return{success: false, response: err};
    }
}

module.exports.findClinicalInfoByID = async(clinicalInfoID) =>{
}