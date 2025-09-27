var express = require("express");
var router = express.Router();
var axios = require('axios');
const { route } = require('mongoose')
const SensorModel = require('../model/sensor')
const SensorController = require ('../controller/sensor')


router.get("/", (req, res) => {
    res.json({
        rota: "sensores"
    })
})

router.get("/identificador/:id", (req, res) => {
    res.json({
        identificador: req.params.id,
    })
})

router.get("/acedehpeixoto/:id", (req, res) => {
    axios.get(
        'http://nosql.hpeixoto.me/api/sensor/' + req.params.id
    )
    .then(response => {
        res.json(response.data)
    })
    .catch(err =>{
        console.log(err)
        res.json(err)
    })
})
router.get("/list", (req, res) =>{
    SensorModel.find((err, sensors) => {
        if (err) {
            res.json(err)
        } else {
            res.json(sensors)
        }
    });
})
router.get("/list/:id", (req,res) =>{
    SensorModel.find({sensorid:req.params.id}, (err,sensors))
    if (err){
        res.json(err)
    } else {
        res.json(sensors)
    }
})

router.delete("delete/:id", (req,res) =>{
    const { sensorid, sensornum, type_of_sensor} = req.body;
    let SensorRemove = SensorController.SensorRemove(sensorid, sensornum, type_of_sensor)
    if (SensorRemove.success){
        res.status(200).json({info:"Sensor removido com sucesso"})
    } else {
        res.status(200).json({info:"Erro na remocao do sensor"})
    }
})

router.put("/update", async (req, res) =>{
    const { sensorid, sensornum, type_of_sensor} = req.body;
    let SensorUpdate = await SensorController.updateSensor(sensorid, sensornum, type_of_sensor)
    if (SensorUpdate.sucess){
        res.status(200).json({info:"Sensor atualizado com sucesso"})
    } else {
        res.status(200).json({info:"Sensor nao foi atualizado com sucesso"})
    }

}) 


module.exports = router;
