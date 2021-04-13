// get the model

const User = require("../users/userModel");
let auth =(req,res,next)=>{
    let token =req.cookies.auth;
    User.SearchByToken(token,(err,user)=>{
        if(err) throw err;
        if(!user) return res.json({
            error :true,
            message : "Not Logged in!",
            isAuth : false,
        });

        req.token= token;
        req.user=user;
        next();

    })
}

module.exports={auth};