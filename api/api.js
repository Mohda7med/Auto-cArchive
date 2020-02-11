const express = require('express');
const bodyParser = require('body-parser');
const pg = require('pg');
const path = require('path');

// Init App and Router and redisClient
const router = express.Router();
const app = express();


const dbConfig = {
    user: 'postgres',
    password: 'password',
    database: 'postgres',
    host: 'url_of_ec2_instance_with_postgres',
    port: 5432,
    max: 100, // 100 clients at a any given time
    idleTimeoutMillis: 10000,
}


// init db
const db = new pg.Pool(dbConfig);
db.on('error', function (err) {
    console.error('idle client error' + err.message + err.stack);
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


/* ROUTER */

router.post('/query', function (req, res) {

    let querystring = req.body.querystring;


    db.query(querystring, [], (error, result) => {
        if (error) {
            return res.json({
                status: 0,
                message: error
            });
        }
        else if (result.rows.length > 0) {
            return res.json({
                status: 1,
                rows: result.rows
            });
        } else {
            return res.json({
                status: 0,
                message: 'No results available.'
            });
        }
    });
});

app.use('/', router);

// HTTP
app.listen(process.env.PORT || 80, () => {
    console.log(`App Started on PORT ${process.env.PORT || 80}`);
});
