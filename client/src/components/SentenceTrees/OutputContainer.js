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
                    <img src={props.imageSource} className="card-img-bottom" alt="sentence_tree"/>
                </div>
            </div>
        </>
    )
}