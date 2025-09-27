let PatientSchema = require('../model/patient');

module.exports.newPatient = async(patientid, patientname, patientage) => {
    try{
        let patient = new PatientSchema({patientid: patientid, patientname: patientname, patientage: patientage})
        let response = await patient.save();
        console.log(response)
        return {success: true, response};
    } catch (err){
        console.log(err)
        return{success: false, response: err};
    }
}

module.exports.findPatientByID = async(patientid) =>{
}