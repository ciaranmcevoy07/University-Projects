let ClinicalInfoSchema = require('../model/clincalinfo');

module.exports.newClinicalInfo = async(clinicalInfoID,admDate,bed,bodyTemp,bpm,sato2,bloodPress) => {
    try{
        let bloodPressureObject = {systolic:systolic, diastolic: diastolic};
        let newClinicalInfo = new ClinicalInfoSchema({
            clinicalInfoID: clinicalInfoID,
            admDate: admDate,
            bed: bed,
            bodyTemp,
            bpm,
            sato2,
            bloodPress:bloodPressureObject})
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