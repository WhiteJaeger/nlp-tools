import React from "react";
import TextArea from "./TextArea";

export default function SingleTextInputForm(props) {
    return (
        <form className="form-control" onSubmit={props.handleSubmit}>
            <div className="input-group d-flex bd-highlight mb-3">
                <div className="container">
                    <h4 className="py-2">Type a Sentence</h4>
                </div>
                <TextArea
                    containerClass="w-50 container-md"
                    displayText="Sentence"
                    formID="input-text"
                    value={props.sentence}
                    rows={5}
                    setFunction={props.setSentence}
                />
            </div>

            <input className="btn btn-outline-secondary mb-2" id="submit-button" type="submit"
                   value="Submit"
            />
        </form>
    )
}
