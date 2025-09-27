let DoenteModel = require('../model/Doente');

module.exports.newDoente = async (id_paciente, nome, data_nascimento, genero, cod_postal, registos) => {
    try {
        let Doente = new DoenteModel({id_paciente, nome, data_nascimento, genero, cod_postal, registos});
        let response = await Doente.save();
        return {success: true, response};
    } catch(err) {
        console.log(err);
        return {success: false, response: err}
    }
}