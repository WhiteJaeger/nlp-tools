import React, {useEffect, useRef, useState} from "react";
import {fetchAndSetData} from "../utils";
import Checkbox from "./shared/Checkbox";
import {TextArea} from "./shared/TextArea";


export default function NGramMetrics() {

    const [metrics, setMetrics] = useState({});
    const [hypothesis, setHypothesis] = useState('');
    const [reference, setReference] = useState('');
    const [metric, setMetric] = useState('');
    const [isLoading, setIsLoading] = useState(false);
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

    async function handleSubmit(event) {
        event.preventDefault();
        setIsLoading(true);
        const data = {
            preprocessing: {
                expandContractions: expandContractions.current.checked,
                lowercase: lowercase.current.checked,
                removeSpecialCharacters: removeSpecialCharacters.current.checked,
            },
            hypothesis: hypothesis,
            reference: reference,
            metric: metric
        };
        const response = await fetch('/api/n-gram-metric', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const serverResponse = await response.json();
        setIsLoading(false);
        console.log(serverResponse);
        for (const setFunction of [setMetric, setReference, setHypothesis]) {
            setFunction('');
        }
        for (const reference of [expandContractions, lowercase, removeSpecialCharacters]) {
            reference.current.checked = false;
        }

    }

    if (isLoading) {
        return (
            <h2>Loading...</h2>
        )
    } else {

        return (
            <div className="container" id="n-gram-metrics">
                <form className="form-control" onSubmit={handleSubmit}>
                    <div className="input-group mb-3 options">
                        <div className="input-group-prepend">
                            <label className="input-group-text" htmlFor="metric-select">Metrics</label>
                        </div>
                        <select className="custom-select" value={metric} name="metric" required
                                onChange={(e) => {
                                    setMetric(e.target.value)
                                }}>
                            <option disabled value="">Choose Metric</option>
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
                        <TextArea
                            containerClass="w-50 container-md"
                            displayText="Hypothesis translation"
                            formID="input-text-hypothesis"
                            value={hypothesis}
                            rows={5}
                            setFunction={setHypothesis}
                        />
                        <TextArea
                            containerClass="w-50 container-md"
                            displayText="Reference translation"
                            formID="input-text-reference"
                            value={reference}
                            rows={5}
                            setFunction={setReference}
                        />
                    </div>

                    <input className="btn btn-outline-secondary mb-2" id="submit-button" type="submit" value="Evaluate"
                    />
                </form>
            </div>
        );
    }
}
