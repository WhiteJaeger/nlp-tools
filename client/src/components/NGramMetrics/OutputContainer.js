import React from "react";
import TranslationsRow from "../shared/TranslationsRow";
import Card from "../shared/Card";

export default function OutputContainer(props) {
    if (props.scores) {
        function renderScoresRows(scores) {
            const tableRows = []
            for (const [metricDisplayName, score] of Object.entries(scores)) {
                tableRows.push(
                    <tr key={metricDisplayName}>
                        <td>
                            {metricDisplayName}
                        </td>
                        <td>
                            {score}
                        </td>
                    </tr>)
            }
            return tableRows;
        }

        return (
            <>
                <div className="container mt-2" id="result-container">
                    <div>
                        <TranslationsRow
                            reference={props.reference}
                            hypothesis={props.hypothesis}
                        />
                    </div>
                    <div className="mt-2 text-center">
                        <table className="table table-hover table-bordered">
                            <thead className="fs-4">
                            <tr>
                                <th>
                                    Metric
                                </th>
                                <th>
                                    Score
                                </th>
                            </tr>
                            </thead>
                            <tbody>
                            {renderScoresRows(props.scores)}
                            </tbody>
                        </table>
                    </div>
                </div>
            </>
        )
    }
    return (
        <>
            <div className="container mt-2" id="result-container">
                <div className="row justify-content-md-center row-cols-md-2 text-center">
                    <TranslationsRow
                        reference={props.reference}
                        hypothesis={props.hypothesis}
                    />
                    <Card
                        title="Metric"
                        text={props.metric}
                        id="metric"
                    />
                </div>
                <div className="row row-cols-1 mt-2 text-center">
                    <Card
                        title="Score"
                        text={props.score}
                        id="score"
                    />
                </div>
            </div>
        </>
    )
}