import React from 'react';

export class Instruction extends React.Component {
    render() {
      return (
        <div className="instruction">
          <h3>Як користуватися перекладачем?</h3>
          <ul>
            <li className='instructions-list'>
              <h4>Крок 1:</h4>
              <span>Вкладіть текст англійською мовою до віконця зліва</span>
            </li>
            <li>
              <h4>Крок 2:</h4>
              <span>Натисніть кнопку "Перекласти" щоб отримати переклад</span>
            </li>
          </ul>
        </div>
      );
    }
  }
