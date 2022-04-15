import React from "react";

export function TextArea(props) {
    return (
        <div className={props.containerClass}>
            <span className="input-group-text">{props.displayText}</span>
            <textarea className="form-control" id={props.formID} value={props.value} rows={props.rows} onChange={(e) => {
                props.setFunction(e.target.value)
            }}/>
        </div>
    )
}
