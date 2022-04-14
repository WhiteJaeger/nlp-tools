import React, {useEffect, useState, useRef} from "react";
import {fetchAndSetData} from "../utils";
import Checkbox from "./shared/Checkbox";


export default function NGramMetrics() {

    const [metrics, setMetrics] = useState({});
    const [hypothesis, setHypothesis] = useState('');
    const [reference, setReference] = useState('');
    const [metric, setMetric] = useState('');
    const expandContractions = useRef(null);
    const removeSpecialCharacters = useRef(null);
    const lowercase = useRef(null);

    useEffect(() => {
        fetchAndSetData('/api/available-metrics', setMetrics);
    }, []);

    function renderMetrics(metricsData) {
        const metricsView = []
        for (const [metric, displayName] of Object.entries(metricsData)) {
            metricsView.push(<option value={metric}>{displayName}</option>)
        }
        return metricsView;
    }

    function handleSubmit(event) {
        event.preventDefault();
        console.log(expandContractions.current.checked);
    }


    return (
        <div className="container" id="n-gram-metrics">
            <form className="form-control" onSubmit={handleSubmit}>
                <div className="input-group mb-3 options">
                    <div className="input-group-prepend">
                        <label className="input-group-text" htmlFor="metric-select">Metrics</label>
                    </div>
                    <select className="custom-select" name="metric" required onChange={(e) => {
                        setMetric(e.target.value)
                    }}>
                        <option selected disabled value="">Choose Metric</option>
                        {renderMetrics(metrics)}
                    </select>
                </div>
                <div className="container border-top border-bottom" id="preprocessing">
                    <h3>Text pre-processing:</h3>
                    <Checkbox
                        reference={expandContractions}
                        id={"expand-contractions"}
                        label={"Expand contractions (e.g. I`m -> I am)"}
                    />
                    <Checkbox
                        reference={removeSpecialCharacters}
                        id={"remove-special-characters"}
                        label={"Remove special characters (e.g. \",\""}
                    />
                    <Checkbox
                        reference={lowercase}
                        id={"lowercase"}
                        label={"Lowercase"}
                    />
                </div>
                <div className="input-group p-3 d-flex bd-highlight mb-3">
                    <div className="w-50 container-md">
                        <span className="input-group-text">Hypothesis translation</span>
                        <textarea className="form-control" id="input-text-hypothesis" rows={5} onChange={(e) => {setHypothesis(e.target.value)}}/>
                    </div>
                    <div className="w-50 container-md">
                        <span className="input-group-text">Reference translation</span>
                        <textarea className="form-control" id="input-text-reference" rows={5} onChange={(e) => {setReference(e.target.value)}}/>
                    </div>
                </div>

                <input className="btn btn-outline-secondary mb-2" id="submit-button" type="submit" value="Evaluate"
                />
            </form>
        </div>
    );
}
