import React, {useEffect, useRef, useState} from "react";
import {fetchAndSetData, postAndGetResponse} from "../../utils";
import Checkbox from "../shared/Checkbox";
import TextArea from "../shared/TextArea";
import HeadContent from "../shared/HeadContent";
import Loading from "../shared/Loading";
import OutputContainer from "./OutputContainer";


export default function NGramMetrics() {

    const [metrics, setMetrics] = useState({});
    const [hypothesis, setHypothesis] = useState('');
    const [reference, setReference] = useState('');
    const [metric, setMetric] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showOutput, setShowOutput] = useState(false);
    const [output, setOutput] = useState({hypothesis: '', reference: '', metric: '', score: ''});
    const expandContractions = useRef(null);
    const removeSpecialCharacters = useRef(null);
    const lowercase = useRef(null);

    useEffect(() => {
        fetchAndSetData('/api/available-metrics', setMetrics);
    }, []);

    function renderMetrics(metricsData) {
        const metricsView = []
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
                expandContractions: expandContractions.current.checked,
                lowercase: lowercase.current.checked,
                removeSpecialCharacters: removeSpecialCharacters.current.checked,
            },
            hypothesis: hypothesis,
            reference: reference,
            metric: metric
        };
        postAndGetResponse('/api/n-gram-metric', data).then((serverResponse) => {
            setIsLoading(false);
            for (const setFunction of [setMetric, setReference, setHypothesis]) {
                setFunction('');
            }
            for (const checkboxReference of [expandContractions, lowercase, removeSpecialCharacters]) {
                checkboxReference.current.checked = false;
            }

            setOutput(serverResponse);
            setShowOutput(true);
        });
    }

    if (isLoading) {
        return (
            <Loading/>
        )
    } else {
        return (
            <>
                <div className="container" id="n-gram-metrics">
                    <HeadContent
                        header="Sentence Level Translation Evaluator"
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
                            <select className="custom-select" value={metric} name="metric" required
                                    onChange={(e) => {
                                        setMetric(e.target.value)
                                    }}>
                                <option disabled value="">Choose Metric</option>
                                {renderMetrics(metrics)}
                            </select>
                        </div>
                        <div className="container border-top border-bottom py-2" id="preprocessing">
                            <h4 className="py-2">Choose Text Pre-processing</h4>
                            <Checkbox
                                reference={expandContractions}
                                id={"expand-contractions"}
                                label={"Expand contractions (e.g. I`m -> I am)"}
                            />
                            <Checkbox
                                reference={removeSpecialCharacters}
                                id={"remove-special-characters"}
                                label={"Remove special characters (e.g. \",\")"}
                            />
                            <Checkbox
                                reference={lowercase}
                                id={"lowercase"}
                                label={"Lowercase"}
                            />
                        </div>
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
                {showOutput && <OutputContainer
                    hypothesis={output.hypothesis}
                    reference={output.reference}
                    metric={output.metric}
                    score={output.score}
                />}
            </>
        );
    }
}
