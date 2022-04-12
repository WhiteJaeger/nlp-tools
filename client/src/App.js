import React, {useEffect, useState} from "react";


export default function App() {

    const [time, setTime] = useState('Loading...');

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(
                '/api/time',
            );

            setTime(JSON.stringify(await response.json()));
        };

        fetchData();
    }, [])

    return (
        <div>
            <h1>Hello there!</h1>
            <p>Current time is {time}</p>
        </div>
    );
}
