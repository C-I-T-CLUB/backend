// models for files and its functionalities

var mongoose=require('mongoose');
const Files=mongoose.Schema({
    name:{
        type: String,
        required: true,
        maxlength: 500
    },
    course:{
        type: String,
        required: true,
        maxlength: 500
    },
    fileId: {
        required: true,
        type: String,
    },
    date: {
        default: Date.now(),
        type: Date,
    },
});



// operations methods
module.exports=mongoose.model('Files',Files);