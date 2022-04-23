import React from "react";


export default function Loading() {
    return (
        <>
            <div className="d-flex justify-content-center m-5">
                <strong>Loading...</strong>
                <div className="spinner-border ml-4" role="status" aria-hidden="true"/>
            </div>
        </>
    )
}
