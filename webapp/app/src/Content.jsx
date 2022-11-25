import React from 'react';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { Instruction } from './Instruction';
import { Box } from './Box';
import './Content.css';
import { ReactComponent as SwitchArrows } from './assets/exchange-svgrepo-com.svg';


const languagesLabels = {
  eng: 'Англійська',
  ukr: 'Українська'
}

function getSourceLang(sourceLangIsEng) {
  return sourceLangIsEng == true ? languagesLabels.eng : languagesLabels.ukr;
}

function getTargetLang(sourceLangIsEng) {
  return sourceLangIsEng == true ? languagesLabels.ukr : languagesLabels.eng;
}

export class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      engText: 'Вкладіть сюди текст для перекладу',
      textAreaValue: '',
      translated: "Тут з'явиться перекладений текст",
      sourceLangIsEng: true
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleChangeEng = this.handleChangeEng.bind(this);
    this.handleLangSelected = this.handleLangSelected.bind(this);
  }

  handleChangeEng(event) {
    this.setState(state => ({
      error: state.error,
      isLoaded: state.isLoaded,
      translated: state.translated,
      textAreaValue: event.target.value
    }));
  }


  handleLangSelected() {
    this.setState(state => ({
      ...state,
      sourceLangIsEng: !state.sourceLangIsEng
    }));
  }

  async handleClick() {
    this.setState(state => ({
      error: state.error,
      isLoaded: state.isLoaded,
      translated: state.translated,
      textAreaValue: state.value,
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
      }));
    } catch (err) {
      this.setState(state => ({
        error: err,
        isLoaded: true,
        translated: '',
        textAreaValue: state.textAreaValue,
      }));
    }
  };

  render() {
    return (
      <main className='main'>
      <Container className='container container-fluid'>
        <Instruction />
          <Row  className='row-trans'>
           <Col className='col-2'>
           </Col>
           <Col className='col-3'>
            <h4 className='sourceLang'>{getSourceLang(this.state.sourceLangIsEng)}</h4>
           </Col>
           <Col className='col-2'>
           <button className='select-lang-btn' onClick={this.handleLangSelected}>
            <SwitchArrows 
              className='switch-arrows'
              // viewBox="0 0 100 100"
              // preserveAspectRatio="x200Y200 meet"
            /> <p>змінити мову</p>
           </button>
           </Col>
           <Col className='col-3'>
            <h4 className='targetLang'>{getTargetLang(this.state.sourceLangIsEng)}</h4>
           </Col>
           <Col className='col-2'>
           </Col>
          </Row>
          <Row  className='row-trans'>
            <Col className='col-6'>
              <div className='column-trans'>
                <Box className='box' text={this.state.engText} onChangeHandler={this.handleChangeEng}>   
                </Box>
              </div>
            </Col>
            <Col className='col-6'>
              <div className='column-trans'>
                <div className='box'>
                  { this.state.translated }
                </div>
              </div>
            </Col>
          </Row>
          <Row className='row-trans'>
            <Col className='col-4'></Col>
            <Col className='col-4'>
                <button onClick={this.handleClick} className='translate-btn'>
                    { this.state.isLoaded? 'Зачекайте...' : 'Перекласти'}
                    <span className={ !this.state.isLoaded? 'hidden' : 'spinner-border spinner-border-sm loading'}></span>
                </button>
            </Col>
            <Col className='col-4'></Col>
          </Row>
      </Container>
    </main>
    );
  }
}
