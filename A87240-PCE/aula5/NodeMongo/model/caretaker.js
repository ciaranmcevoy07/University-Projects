var mongoose=require('mongoose');
var Schema = mongoose.Schema;

var CaretakerSchema =  new Schema({
    caretakerid: {type:Number, unique:true}, 
    caretakername: {type: String},
})

module.exports = mongoose.model('caretaker', CaretakerSchema)