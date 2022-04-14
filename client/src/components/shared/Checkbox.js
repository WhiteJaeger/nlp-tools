import React from "react";

class Checkbox extends React.Component {
    render() {
    return (
        <div className="form-check form-check-inline">
            <input className="form-check-input" ref={this.props.reference} type="checkbox" id={this.props.id}
                   name={this.props.id}
                   defaultChecked={false}/>
            <label className="form-check-label" htmlFor={this.props.id}>{this.props.label}</label>
        </div>
    )
        }
}

export default Checkbox;
