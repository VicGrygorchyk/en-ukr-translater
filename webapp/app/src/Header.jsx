import React from 'react';
import './Header.css'

export class Header extends React.Component {
    render() {
      return (
        <header className="header">
            <p>
                {this.props.title}
            </p>
        </header>
      );
    }
  }
