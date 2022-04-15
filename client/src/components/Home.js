import React from "react";

export default function Home() {
    return (
        <>
            <div className="container border py-2 my-2">
                <h3>Description</h3>
                <div className="container">
                    <p>This site provides an interface for interaction with different Natural Language Processing
                        metrics
                        and
                        other
                        NLP tools.</p>
                    <p className="fs-4">Translation evaluation metrics include:</p>
                    <ul>
                        <li>N-Gram based:
                            <ul>
                                <li>BLEU</li>
                                <li>GLEU</li>
                                <li>Character n-gram F-score</li>
                                <li>NIST</li>
                                <li>METEOR</li>
                            </ul>
                        </li>
                        <li>Sentence Trees based:
                            <ul>
                                <li>Subtree metric</li>
                            </ul>
                        </li>
                    </ul>
                    <p className="fs-4">Other NLP tools:</p>
                    <ul>
                        <li>Context POS tagger</li>
                        <li>Sentence trees builder</li>
                    </ul>
                    <p>These lists are expected to expand.</p>
                </div>
            </div>
            <footer>
                <div className="container border py-2 my-2">
                    <h4>Contribution</h4>
                    <div className="container">
                        <p>If you find errors or something seems ambiguous to you, please contact me via:</p>
                        <ul>
                            <li>Submitting an issue on <a className="btn-link"
                                                          href="https://github.com/WhiteJaeger/nlp-metrics"
                                                          target="_blank" rel="noreferrer">Github repository</a>.
                            </li>
                            <li>Emailing me: logerk3@gmail.com</li>
                        </ul>
                    </div>
                </div>
            </footer>
        </>
    );
}
