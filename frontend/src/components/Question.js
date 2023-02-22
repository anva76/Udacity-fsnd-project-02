import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  provideDefaultImgUrl(event) {
    // if there is no svg file for some category, a default icon is provided
    event.target.src = 'default.svg'
  }

  renderQuestionCategoryImg(category) {
        // if category is null for any reason, a default icon is provided
        return (
          <img
            onError={this.provideDefaultImgUrl}
            className='category'
            alt={category ? `${category.toLowerCase()}` : 'default icon'}
            src={category ? `${category.toLowerCase()}.svg` : 'default.svg'}
          />
        ) 

  }
  
  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className='Question-holder'>
        <div className='Question'>{question}</div>
        <div className='Question-status'>
          {this.renderQuestionCategoryImg(category)}
          <div className='difficulty'>Difficulty: {difficulty}</div>
          <img
            src='delete.png'
            alt='delete'
            className='delete'
            onClick={() => this.props.questionAction('DELETE')}
          />
        </div>
        <div
          className='show-answer button'
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
        <div className='answer-holder'>
          <span
            style={{
              visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
