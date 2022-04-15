import React from "react";

export function HeadContent(props) {
    return (
        <>
            <div className="head-content container border my-3 pt-3">
                <h3>{props.header}</h3>
                <p>{props.content}</p>
            </div>
        </>
    )
}