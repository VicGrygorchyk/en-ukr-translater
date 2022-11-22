import React from 'react';
import './Box.css';

export class Box extends React.Component {
    render() {
      return (
        <textarea className='box'
        placeholder={this.props.text}
        onChange={this.props.onChangeHandler}
        />
      );
    }
  }
