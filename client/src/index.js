import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import './index.css';
import {Home, Navigation, NGramMetrics, POSTagger, SentenceTrees, STM} from './components';

ReactDOM.render(
    <React.StrictMode>
        <Router>
            <Navigation/>
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/n-gram-metrics" element={<NGramMetrics/>}/>
                <Route path="/pos-tagger" element={<POSTagger/>}/>
                <Route path="/sentence-trees" element={<SentenceTrees/>}/>
                <Route path="/stm" element={<STM/>}/>
            </Routes>
        </Router>
    </React.StrictMode>,
    document.getElementById('root')
);
