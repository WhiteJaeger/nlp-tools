import React from "react";
import TranslationsRow from "../shared/TranslationsRow";
import Card from "../shared/Card";

export default function OutputContainer(props) {
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