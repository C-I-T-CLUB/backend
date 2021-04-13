var mongoose=require('mongoose');
const jwt=require('jsonwebtoken');
const bcrypt=require('bcrypt');
const confiq=require('../config/config').get(process.env.NODE_ENV);
const salt=12;

const userSchema=mongoose.Schema({
    firstname:{
        type: String,
        required: true,
        maxlength: 50
    },
    lastname:{
        type: String,
        required: true,
        maxlength: 50
    },
    email:{
        type: String,
        required: true,
        trim: true,
        unique: 1
    },
    phone:{
        type: String,
        required: true,
        trim: true,
        unique: 1
    },
    password:{
        type:String,
        required: true,
        minlength:8
    },
    // this is used for comfirmation
    password2:{
        type:String,
        required: true,
        minlength:8
    },
    // for verification and authentication
    token:{
        type: String
    }
});


// check if password match
userSchema.methods.comparePassword=function(password,cb){
    bcrypt.compare(password,this.password,function(err,isTrue){
        if(err) return cb(err);
        cb(null,isTrue);
    });
}


// save the user instance  after password encription
// we need to encript the password before saving
userSchema.pre('save',function(next){
    // get current user instance
    var user=this;
    if(user.isModified('password')){
        bcrypt.genSalt(salt,function(err,salt){
            if(err)
            return next(err);

            bcrypt.hash(user.password,salt,function(err,hash){
                if(err) return next(err);
                user.password=hash;
                // user.password2=hash;
                next();
            })

        })
    }
    else{
        next();
    }
});


// Create token for verification on browsers
userSchema.methods.createToken=function(cb){
    var user =this;
    console.log(user._id)
    var token=jwt.sign(user._id.toHexString(),confiq.SECRET);
    user.token=token;
    user.save(function(err,user){
        if(err) return cb(err);
        cb(null,user);
    })
}



// find a user using token
userSchema.statics.SearchByToken=function(token,cb){
    var user=this;
    jwt.verify(token,confiq.SECRET,function(err,decode){
        user.findOne({"_id": decode, "token":token},function(err,user){
            if(err) return cb(err);
            cb(null,user);
        })
    })
};


// remove token
userSchema.methods.deleteToken=function(token,cb){
    var user=this;

    user.update({$unset : {token :1}},function(err,user){
        if(err) return cb(err);
        cb(null,user);
    })
}


module.exports=mongoose.model('User',userSchema);