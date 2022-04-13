import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import './index.css';
import {About, Home, Navigation, NGramMetrics} from './components';

ReactDOM.render(
    <React.StrictMode>
        <Router>
            <Navigation/>
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/n-gram-metrics" element={<NGramMetrics/>}/>
                <Route path="/pos-tagger" element={<About/>}/>
                <Route path="/sentence-trees" element={<About/>}/>
                <Route path="/stm" element={<About/>}/>
            </Routes>
        </Router>
    </React.StrictMode>,
    document.getElementById('root')
);
