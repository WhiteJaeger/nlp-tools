import React, {useEffect, useState} from "react";
import {fetchAndSetData, postAndGetResponse} from "../../utils";
import TextArea from "../shared/TextArea";
import HeadContent from "../shared/HeadContent";
import Loading from "../shared/Loading";
import OutputContainer from "./OutputContainer";
import Preprocessing from "../shared/Preprocessing";


export default function NGramMetrics() {

    const [metrics, setMetrics] = useState({});
    const [hypothesis, setHypothesis] = useState('');
    const [reference, setReference] = useState('');
    const [metric, setMetric] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showOutput, setShowOutput] = useState(false);
    const [output, setOutput] = useState({hypothesis: '', reference: '', metric: '', score: '', scores: {}});
    const [expandContractions, setExpandContractions] = useState(false);
    const [removeSpecialCharacters, setRemoveSpecialCharacters] = useState(false);
    const [lowercase, setLowercase] = useState(false);

    useEffect(() => {
        fetchAndSetData('available-metrics', setMetrics);
    }, []);

    function renderMetrics(metricsData) {
        const metricsView = []
        metricsView.push(<option key="all" value="all">All</option>);
        for (const [metric, displayName] of Object.entries(metricsData)) {
            metricsView.push(<option key={metric} value={metric}>{displayName}</option>)
        }
        return metricsView;
    }

    function handleSubmit(event) {
        event.preventDefault();
        setIsLoading(true);
        setShowOutput(false);

        const data = {
            preprocessing: {
                expandContractions: expandContractions,
                lowercase: lowercase,
                removeSpecialCharacters: removeSpecialCharacters,
            },
            hypothesis: hypothesis,
            reference: reference,
        };
        postAndGetResponse(`n-gram-metric/${metric}`, data).then((serverResponse) => {
            setIsLoading(false);
            for (const setFunction of [setMetric, setReference, setHypothesis]) {
                setFunction('');
            }
            for (const setFunction of [setExpandContractions, setLowercase, setRemoveSpecialCharacters]) {
                setFunction(false);
            }

            setOutput(serverResponse);
            setShowOutput(true);
        });
    }

    if (isLoading) {
        return (
            <Loading/>
        )
    }
    return (
        <>
            <div className="container" id="n-gram-metrics">
                <HeadContent
                    header="Sentence Level Translation Evaluation"
                    content="This page provides an interface to measure the goodness of a given translation with N-gram based metrics."
                />
                <form className="form-control" onSubmit={handleSubmit}>
                    <div className="input-group mb-3 py-2 options">
                        <div className="container">
                            <h4 className="py-2">Select Metric</h4>
                        </div>
                        <div className="input-group-prepend">
                            <label className="input-group-text" htmlFor="metric-select">Metrics</label>
                        </div>
                        <select className="custom-select" value={metric} name="metric" id="metric-select" required
                                onChange={(e) => {
                                    setMetric(e.target.value)
                                }}>
                            <option disabled value="">Choose Metric</option>
                            {renderMetrics(metrics)}
                        </select>
                    </div>
                    <Preprocessing
                        expandContractions={{value: expandContractions, setFunction: setExpandContractions}}
                        removeSpecialCharacters={{
                            value: removeSpecialCharacters,
                            setFunction: setRemoveSpecialCharacters
                        }}
                        lowercase={{value: lowercase, setFunction: setLowercase}}
                    />
                    <div className="input-group d-flex bd-highlight mb-3">
                        <div className="container">
                            <h4 className="py-2">Type Hypothesis and Reference Translations</h4>
                        </div>
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

                    <input className="btn btn-outline-secondary mb-2" id="submit-button" type="submit"
                           value="Evaluate"
                    />
                </form>
            </div>
            {showOutput && output.score && <OutputContainer
                hypothesis={output.hypothesis}
                reference={output.reference}
                metric={output.metric}
                score={output.score}
            />}
            {showOutput && output.scores && <OutputContainer
                hypothesis={output.hypothesis}
                reference={output.reference}
                scores={output.scores}
            />}
        </>
    );
}
