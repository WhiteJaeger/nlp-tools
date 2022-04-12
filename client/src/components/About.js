import React from "react";

export default function About() {
    return (
        <div className="about">
            <div className="container">
                <div className="row">
                    <div className="col-md-6 offset-md-3">
                        <img
                            className="img-fluid rounded mb-4 mb-lg-0"
                            src="http://placehold.jp/150x150.png"
                            alt=""
                        />
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-6 offset-md-3">
                        <h1 className="font-weight-light">About</h1>
                        <p>
                            Lorem Ipsum is simply dummy text of the printing and typesetting
                            industry. Lorem Ipsum has been the industry's standard dummy text
                            ever since the 1500s, when an unknown printer took a galley of
                            type and scrambled it to make a type specimen book.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
