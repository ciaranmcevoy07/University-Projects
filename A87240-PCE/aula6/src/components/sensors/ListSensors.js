import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


import axios from "axios";
import React, {useState, useEffect} from 'react'

export default function ListSensors() {
    const baseURL = "http://localhost:3000/sensors/list";

    const [sensorList, setSensorList] = useState([]);
    useEffect(() => {
        axios.get(baseURL).then((response) =>{ 
          setSensorList(response.data);
        });
    }, []);
        return (
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Sensores (ID)</TableCell>
                  <TableCell align="right">Numero do Sensor</TableCell>
                  <TableCell align="right">Tipo de Sensor</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {sensorList.map((sensor) => (
                  <TableRow
                    key={sensor.sensorid}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      {sensor.sensorid}
                    </TableCell>
                    <TableCell align="right">{sensor.sensornum}</TableCell>
                    <TableCell align="right">{sensor.type_of_sensor}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        );
      }