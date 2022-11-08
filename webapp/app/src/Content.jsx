import React from 'react';
import { Instruction } from './Instruction';
import { Box } from './Box';
import './Content.css';

export class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      engText: 'Вкладіть сюди англійський текст',
      textAreaValue: '',
      translated: "Тут з'явиться текст перекладений українською мовою"
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleChangeEng = this.handleChangeEng.bind(this);
  }

  handleChangeEng(event) {
    this.setState(state => ({
      error: state.error,
      isLoaded: state.isLoaded,
      translated: state.translated,
      textAreaValue: event.target.value
    }));
  }

  async handleClick() {
    console.log(this.state)
    try {
      const response = await fetch('/translate', {
        method: 'POST',
        body: JSON.stringify({
          input: this.state.textAreaValue
        }),
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
      });
      console.log(response);
      const result = await response.json();
      const translated = result.map((text) => text.translation_text).join(' ');

      this.setState(state => ({
        error: null,
        isLoaded: true,
        translated: translated,
        textAreaValue: state.textAreaValue
      }));
    } catch (err) {
      this.setState(state => ({
        error: err,
        isLoaded: true,
        translated: '',
        textAreaValue: state.textAreaValue
      }));
    }
  };

  render() {
    return (
      <main className='main'>
      <div className='container'>
        <div className="row-1">
          <Instruction />
        </div>
        <div className='row-2'>
          <Box text={this.state.engText} onChangeHandler={this.handleChangeEng}/>
          <div className="box">
            { this.state.translated }
          </div>
        </div>
        <div className='row-3'>
          <button onClick={this.handleClick} className='translate-btn'>Перекласти</button>
        </div>
      </div>
    </main>
    );
  }
}
