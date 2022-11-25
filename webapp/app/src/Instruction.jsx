import React from 'react';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import CardHeader from 'react-bootstrap/CardHeader';
import Row from 'react-bootstrap/Row';
import './Instruction.css';

export class Instruction extends React.Component {
    render() {
      return (
        <Row className="instruction">
          <h3>Як скористатися перекладачем?</h3>
          <Col>
            <Card className='h-100 border-black-50 instruction-card'>
              <CardHeader className="card-title">Крок 1:</CardHeader>
              <div className="card-body">
                <p className="card-text">Виберіть з якої мови перекласти (англійська чи українська)</p>
              </div>
            </Card>
          </Col>
          <Col>
            <Card className='h-100 border-black-50 instruction-card'>
              <CardHeader className="card-title">Крок 2:</CardHeader>
              <div className="card-body">
                <p className="card-text">Вкладіть текст до віконця зліва для перекладу</p>
              </div>
            </Card>
          </Col>
          <Col>
            <Card className='h-100 border-black-50 instruction-card'>
              <CardHeader className="card-title">Крок 3:</CardHeader>
              <div className="card-body">
                <p className="card-text">Натисніть кнопку "Перекласти" щоб отримати переклад</p>
              </div>
            </Card>
          </Col>
        </Row>
      );
    }
  }
