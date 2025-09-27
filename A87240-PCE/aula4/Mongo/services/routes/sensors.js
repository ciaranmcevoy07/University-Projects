var express = require('express');
var router = express.Router();
var axios = require('axios');

/* GET home page. */
router.get('/', (req, res) => {
    res.json({
        rota: 'sensors' 
    });
});

router.get("/identificador/:id", (req, res) =>{
    res.json({
        identificador: req.params.id,
    })
});

router.get("/acedeHpeixoto/:id", (req, res) => {
    axios.get(
        'http://nosql.hpeixoto.me./api/sensor/' + req.params.id
    )
    .then(response => {
        res.json(response.data);
    })
    .catch(err => {
        console.log(err)
        res.json(err)
    })
});

module.exports = router;