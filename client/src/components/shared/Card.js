import React from "react";

export default function Card(props) {
    return (
        <div>
            <div className="card">
                <div className="card-body">
                    <h4 className="card-title"><strong>{props.title}</strong></h4>
                    <p className="card-text fs-4">{props.text}</p>
                </div>
            </div>
        </div>
    )
}