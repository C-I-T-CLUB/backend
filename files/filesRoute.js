// imports
const express = require('express');
const mongoose= require('mongoose');
const Files = require('../files/filesModel');
const {auth} =require("../middleware/auth");
const multer = require('multer');
const GridFsStorage = require("multer-gridfs-storage");
const db=require('../config/config').get(process.env.NODE_ENV);
const upload = require("../middleware/Storage");
// define files router.
const fileRouter = express.Router();


// db config for these functions
const connect = mongoose.createConnection(db.DATABASE, 
    { useNewUrlParser: true, useUnifiedTopology: true });

// storage var
var gfs;

connect.once('open', () => {
    // initialize stream
    gfs = new mongoose.mongo.GridFSBucket(connect.db, {
        bucketName: "upload"
    });
    console.log("Initialized well");
});


// Endpoinds
// get all files collection
fileRouter.get('/' , (req, res, next) => {
    
    gfs.find().toArray((err, files) => {
        if (!files || files.length === 0) {
            return res.status(200).json({
                success: false,
                message: 'No files available'
            });
        }
        res.status(200).json({
            success: true,
            files,
        });
    });
});


fileRouter.get('/getids' , (req, res, next) => {
    var ids = []
    gfs.find().toArray((err, files) => {
        if (!files || files.length === 0) {
            return res.status(200).json({
                success: false,
                message: 'No files available'
            });
        }

        files.forEach(oneFile => {
            ids.push(oneFile['_id']);
        //    console.log(oneFile['_id']); 
        });

        // find all items with the ids

        Files.find({})
        .then(files => {
            res.status(200).json({
                success: true,
                "Files":files,
                id : ids[0]
                });
            })
        .catch(err => res.status(500).json(err));
        
    });
});


// fetch by id.
fileRouter.get('/file/:id' , (req, res, next) => {
    gfs.find({ _id: req.params.id }).toArray((err, files) => {
        console.log(files);
        if (!files[0] || files.length === 0) {
            return res.status(200).json({
                success: false,
                message: 'No files available',
            });
        }
        res.status(200).json({
            success: true,
            file: files[0],
        });
    });
});






// delete
fileRouter.delete('/file/del/:id' , (req, res, next) => {
    console.log(req.params.id);
    gfs.delete(new mongoose.Types.ObjectId(req.params.id), (err, data) => {
        if (err) {
            return res.status(404).json({ err: err });
        }

        res.status(200).json({
            success: true,
            message: `File with ID ${req.params.id} is deleted`,
        });
    });
});


// fileRouter.get('/delete/:id' , (req, res, next) => {
//     Files.findOne({ _id: req.params.id })
//         .then((file) => {
//             if (file) {
//                 Files.deleteOne({ _id: req.params.id })
//                     .then(() => {
//                         return res.status(200).json({
//                             success: true,
//                             message: `File with ID: ${req.params.id} deleted`,
//                         });
//                     })
//                     .catch(err => { return res.status(500).json(err) });
//             } else {
//                 res.status(200).json({
//                     success: false,
//                     message: `File with ID: ${req.params.id} not found`,
//                 });
//             }
//         })
//         .catch(err => res.status(500).json(err));
//     });



// // post a max of 5 
// fileRouter.post("/multiple" , auth , upload.array('file', 5), (req, res, next) => {
//     console.log("Hi there\n\n")
//     if (req.files){
//         res.status(200).json({
//             success: true,
//             // message: `${req.files.length} files uploaded successfully`,
//         });
//     }
//     else{
//         res.status(500).json(
//             {
//                 message :"Not Successful",
//             }
//         )
//     }

// });





module.exports = fileRouter;





