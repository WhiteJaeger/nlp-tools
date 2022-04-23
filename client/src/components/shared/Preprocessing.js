import React from "react";
import Checkbox from "./Checkbox";


export default function Preprocessing(props) {
    return (
        <div className="container border-top border-bottom py-2" id="preprocessing">
            <h4 className="py-2">Choose Text Pre-processing</h4>
            <Checkbox
                payload={props.expandContractions}
                id={"expand-contractions"}
                label={"Expand contractions (e.g. I`m -> I am)"}
            />
            <Checkbox
                payload={props.removeSpecialCharacters}
                id={"remove-special-characters"}
                label={"Remove special characters (e.g. \",\")"}
            />
            <Checkbox
                payload={props.lowercase}
                id={"lowercase"}
                label={"Lowercase"}
            />
        </div>
    )
}