import React from "react";


export default function MetricConfiguration(props) {

    const metricsWithMinNgramLength = ['chrf', 'gleu'];

    function metricHasMinimumNGramLength(metricName) {
        return metricsWithMinNgramLength.includes(metricName);
    }

    return (
        <>
            <div className="input-group mb-3 py-2 options">
                <div className="container">
                    <h4 className="py-2">Select Additional Parameters</h4>
                </div>
                {metricHasMinimumNGramLength(props.metric) && <LengthSelect
                    nGramLengths={props.nGramLengths}
                    isMaximum={false}
                    minValue={1}
                    maxValue={4}
                    setFunction={props.setFunction}
                />}

                <LengthSelect
                    nGramLengths={props.nGramLengths}
                    isMaximum={true}
                    minValue={metricHasMinimumNGramLength(props.metric) ? props.nGramLengths.minimum : 1}
                    maxValue={4}
                    setFunction={props.setFunction}
                />
            </div>
        </>
    )
}


function LengthSelect(props) {

    function renderOptions(minValue, maxValue) {
        const options = [];
        options.push(<option disabled value="">Choose {props.isMaximum ? "Maximum" : "Minimum"}</option>)
        for (let idx = minValue; idx <= maxValue; idx++) {
            options.push(<option key={idx} value={idx}>{idx}</option>)
        }
        return options;
    }

    function handleChange(event) {
        if (props.isMaximum) {
            props.setFunction({...props.nGramLengths, maximum: event.target.value})
        } else {
            props.setFunction({...props.nGramLengths, minimum: event.target.value})
        }
    }

    const className = `custom-select ${props.isMaximum ? "" : "me-2"}`;
    const selectName = `${props.isMaximum ? "maximum" : "minimum"}-ngram-length`

    return (
        <>
            <div className="input-group-prepend">
                <label className="input-group-text"
                       htmlFor={selectName}>{props.isMaximum ? "Maximum" : "Minimum"} N-gram Length</label>
            </div>
            <select className={className}
                    value={props.isMaximum ? props.nGramLengths.maximum : props.nGramLengths.minimum}
                    name={selectName}
                    id={selectName} required
                    onChange={handleChange}>
                {renderOptions(props.minValue, props.maxValue)}
            </select>
        </>
    )
}
