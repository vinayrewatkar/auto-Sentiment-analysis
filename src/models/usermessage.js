const mongoose = require("mongoose");
const validator = require("validator");

const userSchema = mongoose.Schema({
    firstname : {
        type : String,
        required : true
    },
    lastname : {
        type : String,
        required : true
    },
    email : {
        type : String,
        required : true,
        unique : true,
        // validate: {
        //     validator: function (value) {
        //       return validator.isEmail(value);
        //     },
        //     message: "Invalid email address"
        //   }
    },
    password : {
        type : String,
        required : true
    }

})

const User = mongoose.model("User",userSchema);
module.exports = User;