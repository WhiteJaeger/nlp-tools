import React from "react";

export default function OutputContainer(props) {

    function renderWordToPOSMap(wordToPOSMap) {
        const elements = wordToPOSMap.map((wordToPOS, idx) => {
            return (
                <>
                    <tr key={idx}>
                        <td>
                            {wordToPOS[0]}
                        </td>
                        <td>
                            {wordToPOS[1]}
                        </td>
                    </tr>
                </>
            )
        })
        return (
            <>
                <div className="container w-50" id="result-table">
                    <table className="table table-hover table-bordered">
                        <thead>
                        <tr>
                            <th>
                                Word
                            </th>
                            <th>
                                Part-of-speech
                            </th>
                        </tr>
                        </thead>
                        <tbody>
                        {elements}
                        </tbody>
                    </table>
                </div>
            </>
        )
    }

    return (
        <>
            <div className="container mt-2" id="result-container">
                <div className="card">
                    <div className="card-body">
                        <h4 className="card-title">Result</h4>
                        <p className="card-text"><strong id="sentence">Sentence: </strong>{props.sentence}</p>
                    </div>
                    {renderWordToPOSMap(props.elements)}
                </div>
            </div>
        </>
    )
}