var mongoose= require('mongoose');
var Schema = mongoose.Schema;

var CodigoPostalSchema =  new Schema({
    cod_postal: {type:Number, unique:true}, 
    localidade: {type: String},
})

var RegistoSchema =  new Schema({
    numseq: {type:Number, unique:true}, 
    dataRegisto: {type: Date},
    temperatura: {type: String},
    falta_ar: {type: String},
    dor_cabeca: {type: String},
    dor_muscular: {type: String},
    tosse: {type: String},
    diarreia: {type: String},
    olfato_paladar: {type: String},
    avaliacao_global: {type: String},
})

var DoenteSchema =  new Schema({
    id_paciente:  {type:Number, unique:true}, 
    nome: {type: String},
    data_nascimento: {type: Date},
    genero: {type: String},
    codigo_postal: CodigoPostalSchema,
    registos: [RegistoSchema]
})

module.exports = mongoose.model('Doente', DoenteSchema)