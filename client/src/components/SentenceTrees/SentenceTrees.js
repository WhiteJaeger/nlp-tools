import React, {useState} from "react";
import HeadContent from "../shared/HeadContent";
import TextArea from "../shared/TextArea";
import Loading from "../shared/Loading";
import OutputContainer from "./OutputContainer";
import {fetchImage, postAndGetResponse} from "../../utils";


export default function SentenceTrees() {
    const [sentence, setSentence] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showOutput, setShowOutput] = useState(false);
    const [output, setOutput] = useState({sentence: '', imageSource: ''});

    async function handleSubmit(event) {
        event.preventDefault();
        setIsLoading(true);
        setShowOutput(false);

        const data = {
            sentence: sentence
        };
        const serverData = await postAndGetResponse('sentence-trees', data);
        await fetchImage(serverData['imageSource']).then((image) => {
            setOutput({imageSource: image, sentence: serverData['sentence']});
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
                <div className="container" id="sentence-trees">
                    <HeadContent
                        header="Sentence Trees Builder"
                        content="This page provides an interface to build a sentence tree from a given sentence."
                    />
                    <form className="form-control" onSubmit={handleSubmit}>
                        <div className="input-group d-flex bd-highlight mb-3">
                            <div className="container">
                                <h4 className="py-2">Type a Sentence</h4>
                            </div>
                            <TextArea
                                containerClass="w-50 container-md"
                                displayText="Sentence"
                                formID="input-text"
                                value={sentence}
                                rows={5}
                                setFunction={setSentence}
                            />
                        </div>

                        <input className="btn btn-outline-secondary mb-2" id="submit-button" type="submit"
                               value="Submit"
                        />
                    </form>
                </div>
                {showOutput && <OutputContainer
                    imageSource={output.imageSource}
                    sentence={output.sentence}
                />}
            </>
        )
    }
}
