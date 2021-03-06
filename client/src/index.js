import React from 'react';
import {createRoot} from "react-dom/client";
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import './index.css';
import {Home, Navigation, NGramMetrics, POSTagger, SentenceTrees, STM} from './components';

const container = document.getElementById('root');
const root = createRoot(container);


root.render(
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
    </React.StrictMode>
);
