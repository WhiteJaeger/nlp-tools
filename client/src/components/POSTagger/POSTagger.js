import React, {useState} from "react";
import {postAndGetResponse} from "../../utils";
import Loading from "../shared/Loading";
import HeadContent from "../shared/HeadContent";
import OutputContainer from "./OutputContainer";
import SingleTextInputForm from "../shared/SingleTextInputForm";

export default function POSTagger() {
    const [sentence, setSentence] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showOutput, setShowOutput] = useState(false);
    const [output, setOutput] = useState({sentence: '', posTags: []});

    async function handleSubmit(event) {
        event.preventDefault();
        setIsLoading(true);
        setShowOutput(false);

        const data = {
            sentence: sentence
        };
        await postAndGetResponse('pos', data).then((data) => {
            setOutput({sentence: data['sentence'], posTags: data['posTags']});
            setIsLoading(false);
            setShowOutput(true);
            setSentence('');
        });
    }

    if (isLoading) {
        return (
            <Loading/>
        )
    } else {
        return (
            <>
                <div className="container" id="pos-tagger">
                    <HeadContent
                        header="Part-of-speech Tagger"
                        content="This Part-of-Speech tagger is based on the Continuous Random Fields model.
It was trained on the following NLTK corpora: conll2000, Treebank subset, masc.
Training set consisted of ~60000 sentences, testing set of ~25000 sentences."
                    />
                    <SingleTextInputForm
                        handleSubmit={handleSubmit}
                        sentence={sentence}
                        setSentence={setSentence}
                    />
                </div>
                {showOutput && <OutputContainer
                    sentence={output.sentence}
                    elements={output.posTags}
                />}
            </>
        )
    }
}
