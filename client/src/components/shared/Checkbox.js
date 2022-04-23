import React from "react";

export default function Checkbox(props) {
    return (
        <div className="form-check form-check-inline">
            <input className="form-check-input" ref={props.reference} type="checkbox" id={props.id}
                   name={props.id}
                   defaultChecked={false}/>
            <label className="form-check-label" htmlFor={props.id}>{props.label}</label>
        </div>
    )
}
