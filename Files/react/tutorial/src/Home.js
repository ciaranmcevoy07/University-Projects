import { useState } from 'react';

const Home = () => {
    //let name = 'mario';
    const [name, setName] = useState('mario');
    const [age, setAge] = useState(25)

    const handleClick = () =>{
        setName('luigi');
        setAge(30);
    }
    return (
        <div className="home">
           <h2 style={{
            color:'red',
            borderRadius:'8px'
            }}>Homepage</h2>
            <p>{ name } is {age} years old</p>
            <p>{name}</p>
            <button onClick={handleClick}>Click me</button>
        </div>

      );
}
 
export default Home;