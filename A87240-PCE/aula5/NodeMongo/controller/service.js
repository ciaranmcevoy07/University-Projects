let ServiceSchema = require('../model/service');

module.exports.newService = async(serviceCod, sensorDesc) => {
    try{
        let service = new ServiceSchema({serviceCod: serviceCod, serviceDesc: serviceDesc})
        let response = await service.save();
        console.log(response)
        return {success: true, response};
    } catch (err){
        console.log(err)
        return{success: false, response: err};
    }
}

module.exports.findServiceByID = async(serviceCod) =>{
}