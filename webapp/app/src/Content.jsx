import React from 'react';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

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
      translated: "Тут з'явиться текст перекладений українською мовою",
      spinnerClass: 'hidden'
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
    this.setState(state => ({
      error: state.error,
      isLoaded: state.isLoaded,
      translated: state.translated,
      textAreaValue: state.value,
      spinnerClass: "spinner-border spinner-border-sm"
    }));
    
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
        textAreaValue: state.textAreaValue,
        spinnerClass: "hidden"
      }));
    } catch (err) {
      this.setState(state => ({
        error: err,
        isLoaded: true,
        translated: '',
        textAreaValue: state.textAreaValue,
        spinnerClass: "hidden"
      }));
    }
  };

  render() {
    return (
      <main className='main'>
      <Container className='container container-fluid'>
        <Instruction />
          <Row  className='row-trans'>
            <Col className='col-5 '>
              <div className='column-trans'>
                <Box className='box' text={this.state.engText} onChangeHandler={this.handleChangeEng}>   
                </Box>
              </div>
            </Col>
            <Col className='col-2'>
              <div className='column-trans'>
                <button onClick={this.handleClick} className='btn translate-btn'>
                  Перекласти
                  <span className={this.state.spinnerClass} role="status" aria-hidden="true"></span>
                </button>
                <button className='btn translate-btn'>&#60;- Змінити мову -&#62;</button>
              </div>
              </Col>
            <Col className='col-5'>
              <div className='column-trans'>
                <div className='box'>
                  { this.state.translated }
                </div>
              </div>
            </Col>
          </Row>
      </Container>
    </main>
    );
  }
}
