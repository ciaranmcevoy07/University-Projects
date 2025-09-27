import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';

const types = [
    {
      value: 'Cerebral',
      label: 'Cerebral',
    },
    {
      value: 'Cardiac',
      label: 'Cardiac',
    },
    {
        value: 'Lung',
        label: 'Lung',
      },
  ];

export default function FormSensors() {  
    return (
    <Box
      component="form"
      sx={{
        '& .MuiTextField-root': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <div>
      <TextField id="outlined-basic" label="Sensor ID" variant="outlined" />
      <br></br> 
      <TextField id="outlined-basic" label="Sensor Number" variant="outlined" />
      <br></br>
      <TextField
          id="outlined-select-type_of_sensor"
          select
          label="Select"
          defaultValue="Cardiac"
          helperText="Please select the type of sensor"
        >
            {types.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
        <br></br>
        <Button variant="contained">Create</Button>
      </div>
      </Box>
  );
}