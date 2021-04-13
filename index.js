// varibale imports
const express=require('express');
const mongoose= require('mongoose');
const bodyparser=require('body-parser');
const cookieParser=require('cookie-parser');
const db=require('./config/config').get(process.env.NODE_ENV);
const multer = require('multer');
const GridFsStorage = require("multer-gridfs-storage");
const overider =  require("method-override");
const Files = require('./files/filesModel');
// express config
const app=express();
app.use(express.json())
var crypto = require('crypto')
app.use(bodyparser.urlencoded({extended : false }));
app.use(bodyparser.json());
app.use(cookieParser());
// database connection
mongoose.Promise=global.Promise;
mongoose.connect(
    // "mongodb://localhost/CIT",
    db.DATABASE,
    { useNewUrlParser: true,
      useUnifiedTopology:true 
    },
    function(err){
    if(err) console.log(err);
    console.log("Database  connected Successfully!");
});


// define a place to save 
var multer1  = require('multer')

var storage = new GridFsStorage({
    url: db.DATABASE,
    file: (req, file) => {
        console.log("We have Acceesed storage part");
        return new Promise((resolve, reject) => {
            crypto.randomBytes(16, (err, buf) => {
                if (err) {
                    return reject(err);
                }
                console.log("We are here kutesa!")
                const filename = file.originalname;
                const fileInfo = {
                    filename: filename,
                    bucketName: 'uploads'
                };
                resolve(fileInfo);
            });
        });
    }
});


var upload1 = multer1({ storage })
 


// post filey
app.post('/api/v1/upload' , upload1.any() ,function (req, res , next){

    var myfiles = req.body
    // console.log(myfiles);
    // console.log(myfiles[0]['filename']) 
    // console.log(req.body);
    // console.log(Object.values(req.body)[0])
    // console.log(myfiles[0]['id'])
    let newFile = new Files({
        course: Object.values(req.body)[0],
        name: "myfiles[0]['filename']",
        fileId: "myfiles[0]['id']",
    });

    newFile.save()
        .then((file) => {

            res.status(200).json({
                success: true,
                file :file,
                saved : true,
            });
        })
    .catch(err => res.status(500).json({
        err : err,
        saved :false,
    }));
});


// run the routes
app.get('/',function(req,res){
    const homepage ={
        "login" : "/api/v1/users/login",
        "register" : "/api/v1/users/register",
        "view profile" : "/api/v1/users/profile",
        "post a paper" : "/api/v1/users/post",
        "logout" : "/api/v1/users/logout",
    }
    res.status(200).send(homepage);
});


// get the routes from other files
const userRoute = require("./users/userRoute");
const fileRouter = require("./files/filesRoute");

app.use("/api/v1/users/" , userRoute);
app.use("/api/v1/files/" , fileRouter);
// run the app with a port
const PORT=process.env.PORT||3000;
app.listen(PORT,()=>{
    console.log(`app is live at ${PORT}`);
});