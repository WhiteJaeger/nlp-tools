import React from "react";

export default function OutputContainer(props) {
    return (
        <>
            <div className="container mt-2">
                <div className="card">
                    <div className="card-body">
                        <h4 className="card-title">Result</h4>
                        <p className="card-text"><strong>Sentence: </strong>{props.sentence}</p>
                    </div>
                    {props.elements}
                </div>
            </div>
        </>
    )
}