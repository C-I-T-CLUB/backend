const db=require('../config/config').get(process.env.NODE_ENV);
// create storage engine
var crypto = require('crypto')
var GridFsStorage = require('multer-gridfs-storage');
var multer  = require('multer');

const storage = new GridFsStorage({
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


var upload = multer({ storage});
 

module.exports = upload;