import React from "react";

export default function TranslationsRow(props) {
    return (
        <div>
            <div className="card">
                <div className="card-body">
                    <h4 className="card-title text-center"><strong>Reference and Hypothesis</strong></h4>
                    <div className="d-flex justify-content-evenly">
                        <div className="fs-4"><strong>Reference: </strong>{props.reference}</div>
                        <div className="fs-4"><strong>Hypothesis: </strong>{props.hypothesis}</div>
                    </div>
                </div>
            </div>
        </div>
    )
}

