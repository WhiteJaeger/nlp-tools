import React, {useEffect, useState} from "react";


export default function NGramMetrics() {

    const [metrics, setMetrics] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(
                '/api/available-metrics',
            );

            setMetrics(await response.json());
        };

        fetchData();
    });

    function renderMetrics(metricsData) {
        const metricsView = []
        for (const [metric, displayName] of Object.entries(metricsData)) {
            metricsView.push(<option value={metric}>{displayName}</option>)
        }
        return metricsView;
    }

    return (
        <div className="container" id="n-gram-metrics">
            <form className="form-control" onSubmit={e => e.preventDefault()}>
                <div className="input-group mb-3 options">
                    <div className="input-group-prepend">
                        <label className="input-group-text" htmlFor="metric-select">Metrics</label>
                    </div>
                    <select className="custom-select" name="metric" required>
                        <option selected disabled value="">Choose Metric</option>
                        {renderMetrics(metrics)}
                    </select>
                </div>
                <div className="container border-top border-bottom" id="preprocessing">
                    <h5 className="display-5">Text pre-processing:</h5>
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="checkbox" id="contractions" name="contractions"
                               value="1"/>
                        <label className="form-check-label" htmlFor="contractions">Expand contractions (e.g. I`m ->
                            I am)</label>
                    </div>
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="checkbox" id="spec-chars" name="spec-chars"
                               value="1"/>
                        <label className="form-check-label" htmlFor="spec-chars">Remove special characters (e.g.
                            ",")</label>
                    </div>
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="checkbox" id="lowercase" name="lowercase" value="1"/>
                        <label className="form-check-label" htmlFor="lowercase">Lowercase</label>
                    </div>
                </div>
                <div className="d-flex bd-highlight mb-3">
                    <div className="p-2 bd-highlight">Type your hypothesis translation here:
                        <p><textarea id="input-text-hypothesis"/></p>
                    </div>
                    <div className="ml-auto p-2 bd-highlight">Type your reference translation here:
                        <p><textarea id="input-text-reference"/></p>
                    </div>
                </div>

                <input className="btn btn-outline-secondary mb-2" id="submit-button" type="submit" value="Evaluate"
                />
            </form>
        </div>
    );
}
