// imports
const express = require('express');
// define user router.
const userRouter = express.Router();
const User = require('../users/userModel');
const {auth} =require("../middleware/auth");

// run the routes
userRouter.get('/',function(req,res){
    const homepage ={
        "login" : "/api/v1/users/login",
        "register" : "/api/v1/users/register",
        "view profile" : "/api/v1/users/profile",
        "post a paper" : "/api/v1/users/post",
        "logout" : "/api/v1/users/logout",
    }
    res.status(200).send(homepage);
});
// adding new user (sign-up route)
userRouter.post('/register',function(req,res){
    // taking a user
    const newuser=new User(req.body);
    
   if(newuser.password!=newuser.password2)
   return res.status(400).json(
       {
           isAuth : false ,
           error : true,
           message: "password does not match!"
        }
       );
    
    User.findOne({email:newuser.email},
        function(err,user){
        if(user) return res.status(400).json(
            { 
                isAuth : false,
                error : true, 
                message :"Email exits"
            }
            );
 
        newuser.save((err,myuser)=>{
            if(err) {console.log(err);
                return res.status(400).json({ success : false});}
            res.status(200).json({
                isAuth:true,
                user : myuser,
                error : true,
                message: "Registered Successfully!",
            });
        });
    });
 });


 // login endpoint
 userRouter.post('/login', function(req,res){
    // console.log("Body has  "+ req.body.password);
    let token=req.cookies.auth;
    User.SearchByToken(token,(err,user)=>{
        if(err) return  res(err);
        if(user) return res.status(400).json({
            error :true,
            isAuth : true ,
            message:"You are currently logged in!"
        });
    
        else{
            // console.log(req.body);
            User.findOne(
                {'email':req.body.email},function(err,user){
                if(!user) return res.json(
                    {
                        isAuth : false, 
                        error : false,
                        message : ' Failed ,email not found'
                    });
                // console.log(req.body.password);
        
                user.comparePassword(req.body.password,(err,isTrue)=>{
                    if(!isTrue) return res.json(
                        {
                             isAuth : false,
                             message : "Incorrect Password ",
                             error : true,
                            });
        
                user.createToken((err,user)=>{
                    if(err) return res.status(400).send(err);
                    res.cookie('auth',user.token).json({
                        isAuth : true,
                        message : "Logged successfully!",
                        error : false,
                        id : user._id,
                        email : user.email
                    });
                });    
            });
          });
        }
    });
});

// get logged in user
userRouter.get('/profile',auth,function(req,res){
    res.json({
        isAuth: true,
        error: false,
        id: req.user._id,
        email: req.user.email,
        name: req.user.firstname + req.user.lastname
        
    })
});


//logout user
userRouter.get('/logout',auth,function(req,res){
    req.user.deleteToken(req.token,(err,user)=>{
        if(err) return res.status(400).send(err);
        res.sendStatus(200);
    });

}); 

// Getting all users
userRouter.get('/all', async (req, res) => {
    console.log("we are home of champions");
    try {
      const users = await User.find()
      res.status(200).json(users);
    } catch (err) {
      res.status(500).json({ message: err.message })
    }
  }) 


// export the route
module.exports = userRouter;