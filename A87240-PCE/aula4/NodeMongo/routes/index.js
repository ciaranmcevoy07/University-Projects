var express = require("express");
var router = express.Router();
var axios = require('axios');
let SensorSchema = require ('../controller/sensor')

router.get("/", (req, res) => {
  res.json({
    rota: "index"
  })
})

module.exports = router;

router.get("/acedehpeixoto/:id", (req, res) => {
  axios.get(
      'http://nosql.hpeixoto.me/api/sensor/' + req.params.id
  )
  .then(async response => {
      const {sensorid, sensornum, type_of_sensor} = response.data;
      let newSensorResponse = await SensorSchema.newSensor(sensorid, sensornum, type_of_sensor)
      if (newSensorResponse.success){
          res.status(200).json({info:"Novo sensor adicionado com sucesso"})
      } else {
          res.status(200).json({info:"Erro ao adicionar novo sensor"})
      }
      res.json(response.data);
  })
  .catch(err => {
      console.log(err)
      res.json(err);
  })

})