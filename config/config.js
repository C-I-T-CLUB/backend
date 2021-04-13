
const config={
    production :{
        SECRET: process.env.SECRET,
        DATABASE: process.env.MONGODB_URI
    },
    default : {
        SECRET: 'citclubpassword',
        DATABASE: 'mongodb://localhost:27017/'
    }
}


exports.get = function get(env){
    return config[env] || config.default
}