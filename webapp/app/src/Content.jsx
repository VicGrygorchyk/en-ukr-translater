import React from 'react';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { Instruction } from './Instruction';
import { Box } from './Box';
import './Content.css';
import { ReactComponent as SwitchArrows } from './assets/exchange-svgrepo-com.svg';
import { ApiClient } from './api/apiClient';

const languagesLabels = {
  eng: 'Англійська',
  ukr: 'Українська'
}

function getSourceLang(sourceLangIsEng) {
  return sourceLangIsEng === true ? languagesLabels.eng : languagesLabels.ukr;
}

function getTargetLang(sourceLangIsEng) {
  return sourceLangIsEng === true ? languagesLabels.ukr : languagesLabels.eng;
}

export class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: true,
      engText: 'Вкладіть сюди текст для перекладу',
      textAreaValue: '',
      translated: "Тут з'явиться перекладений текст",
      sourceLangIsEng: true
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleChangeEng = this.handleChangeEng.bind(this);
    this.handleLangSelected = this.handleLangSelected.bind(this);

    this.apiClient = new ApiClient();
  }

  handleChangeEng(event) {
    this.setState(state => ({
      ...state,
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
    const textAreaValue = this.state.textAreaValue;
    if (/^\s+$/.test(textAreaValue) || textAreaValue === '') {
      return;
    }

    this.setState(state => ({
      error: null,
      isLoaded: false,
      translated: state.translated,
      textAreaValue
    }));

    try {
      const body = {
          input: textAreaValue,
          source_lang: this.state.sourceLangIsEng ? 'en' : 'uk'
      }
      const translated = await this.apiClient.translate(body);

      this.setState(state => ({
        error: null,
        isLoaded: true,
        translated: translated,
        textAreaValue: state.textAreaValue,
      }));
    } catch (err) {
      console.log(err);
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
                    { !this.state.isLoaded? 'Зачекайте...' : 'Перекласти'}
                    <span className={ this.state.isLoaded? 'hidden' : 'spinner-border spinner-border-sm loading'}></span>
                </button>
            </Col>
            <Col className='col-4'></Col>
          </Row>
      </Container>
    </main>
    );
  }
}
