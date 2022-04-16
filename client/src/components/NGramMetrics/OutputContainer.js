import React from "react";

export default function OutputContainer(props) {
    return (
        <>
            <hr/>
            <div className="container" id="output-container">
                <div className="container">
                    <h2 className="text-center">
                        Score for the "{props.metric}" metric: {props.score}
                    </h2>
                </div>
                <div className="row">
                    <div className="col-sm-4 offset-2">
                        <div className="card">
                            <div className="card-body">
                                <h5 className="card-title">Hypothesis</h5>
                                <p className="card-text">{props.hypothesis}</p>
                            </div>
                        </div>
                    </div>
                    <div className="col-sm-4">
                        <div className="card">
                            <div className="card-body">
                                <h5 className="card-title">Reference</h5>
                                <p className="card-text">{props.reference}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}