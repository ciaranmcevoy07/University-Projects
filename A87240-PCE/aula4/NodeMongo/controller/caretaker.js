let CaretakerSchema = require('../model/caretaker');

module.exports.newCaretaker = async(caretakerid, caretakername) => {
    try{
        let caretaker = new CaretakerSchema({caretakerid: caretakerid, caretakername: caretakername})
        let response = await caretaker.save();
        console.log(response)
        return {success: true, response};
    } catch (err){
        console.log(err)
        return{success: false, response: err};
    }
}

module.exports.findCaretakerByID = async(caretakerid) =>{
}