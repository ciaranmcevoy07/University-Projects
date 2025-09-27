var express = require("express");
var router = express.Router();
var axios = require('axios');
var SensorController = require ('../controller/sensor')
var CaretakerController = require('../controller/caretaker')
var PatientController = require('../controller/patient')
var ClinicalInfoController = require('../controller/clinicalinfo')
var ServiceController = require('../controller/service')

router.get("/", (req, res) => {
  res.json({
    rota: "index"
  })
})

router.get("/acedehpeixoto/:id", (req, res) => {
  axios.get(
      'http://nosql.hpeixoto.me/api/sensor/' + req.params.id
  )
  .then(async response => {
      const {sensorid, sensornum, type_of_sensor} = response.data;
      var response_sensor;
      let newSensorResponse = await SensorController.newSensor(sensorid, sensornum, type_of_sensor)
      if (newSensorResponse.success){
          response_sensor = "Novo sensor adicionado com sucesso"
      } else {
          response_sensor = "Erro ao adicionar novo sensor"
      }
      

      const {patientid, patientname, patientage} = response.data;
      var response_patient;
      let newPatientResponse = await PatientController.newPatient(patientid, patientname, patientage)
      if (newPatientResponse.success){
          response_patient = "Novo paciente adicionado com sucesso"
      } else {
          response_patient = "Erro ao adicionar novo paciente"
      }
      

      const {serviceCod, serviceDesc} = response.data;
      var response_service;
      let newServiceResponse = await ServiceController.newService(serviceCod, serviceDesc)
      if (newServiceResponse.success){
          response_service = "Novo servico adicionado com sucesso"
      } else {
          response_service = "Erro ao adicionar novo serviço"
      }
     

      const {caretakerid, caretakername} = response.data;
      var response_caretaker;
      let newCaretakerResponse = await CaretakerController.newCaretaker(caretakerid, caretakername)
      if (newCaretakerResponse.success){
          response_caretaker = "Novo caretaker adicionado"
      } else {
          response_caretaker = "Erro ao adicionar novo caretaker"
      }
      
      const {clinicalInfoID, admDate, bed, bodyTemp,bpm, sato2, bloodPress, timestamp} = response.data;
      var response_clinicalInfo;
      let newClinicalInfoResponse = await ClinicalInfoController.newClinicalInfo(clinicalInfoID, admDate, bed, bodyTemp,bpm, sato2, bloodPress, timestamp)
      if (newClinicalInfoResponse.success){
          response_clinicalInfo = "Novos Dados Clincos adicionados com sucesso"
      } else {
          response_clinicalInfo = "Erro ao adicionar novos dados clinicos"
      }
      res.status(200).json({
        "Paciente":response_patient,
        "Sensor":response_sensor,
        "Caretaker":response_caretaker,
        "Clinical Info":response_clinicalInfo,
        "Service":response_service,
    });
  })
  .catch(err => {
      console.log(err)
      res.json(err);
  })
})


module.exports = router;