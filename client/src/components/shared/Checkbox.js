import React from "react";

export default function Checkbox(props) {
    return (
        <div className="form-check form-check-inline">
            <input className="form-check-input" onChange={(event) => {
                props.payload.setFunction(event.target.checked)
            }} checked={props.payload.value} type="checkbox" id={props.id}
                   name={props.id}/>
            <label className="form-check-label" htmlFor={props.id}>{props.label}</label>
        </div>
    )
}
