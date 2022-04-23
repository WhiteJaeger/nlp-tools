import React from "react";

export default function TextArea(props) {
    return (
        <div className={props.containerClass}>
            <span className="input-group-text">{props.displayText}</span>
            <textarea required className="form-control" placeholder="Type here..." id={props.formID} value={props.value}
                      rows={props.rows} onChange={(e) => {
                props.setFunction(e.target.value)
            }}/>
        </div>
    )
}
