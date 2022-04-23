import React from "react";
import TranslationsRow from "../shared/TranslationsRow";
import Card from "../shared/Card";

export default function OutputContainer(props) {
    return (
        <>
            <div className="container mt-2">
                <div className="row justify-content-md-center row-cols-md-2 text-center">
                    <TranslationsRow
                        reference={props.reference}
                        hypothesis={props.hypothesis}
                    />
                    <Card
                        title="Depth"
                        text={props.depth}
                        id="depth"
                    />
                </div>
                <div className="row row-cols-1 row-cols-md-2 mt-2 text-center">
                    <Card
                        title="Subtree Metric Score"
                        text={props.score}
                        id="subtree-score"
                    />
                    <Card
                        title="Subtree Metric Augmented Score"
                        text={props.scoreAugmented}
                        id="subtree-augmented-score"
                    />
                </div>
            </div>
        </>
    )
}