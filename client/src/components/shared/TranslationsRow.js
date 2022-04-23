import React from "react";

export default function TranslationsRow(props) {
    return (
        <div>
            <div className="card" id="texts">
                <div className="card-body">
                    <h4 className="card-title text-center"><strong>Reference and Hypothesis</strong></h4>
                    <div className="d-flex justify-content-evenly">
                        <div className="fs-4" id="reference-text"><strong>Reference: </strong>{props.reference}</div>
                        <div className="fs-4" id="hypothesis-text"><strong>Hypothesis: </strong>{props.hypothesis}</div>
                    </div>
                </div>
            </div>
        </div>
    )
}

