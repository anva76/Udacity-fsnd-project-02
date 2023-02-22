import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import AddCategory from './AddCategory';
import $ from 'jquery';

const QUESTIONS_PER_PAGE = 10

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: '',
      currentSearchTerm: null,
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
          page: result.actual_page,
          currentSearchTerm: null,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / QUESTIONS_PER_PAGE);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
          currentSearchTerm: null,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ search_term: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
          currentSearchTerm: searchTerm,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            if (this.state.currentCategory) {

              const cat_id = Object.keys(this.state.categories)
                          .find(key => this.state.categories[key] === this.state.currentCategory)
              this.getByCategory(cat_id)
              
            } else {
              this.getQuestions()
            }
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

  provideDefaultImgUrl(event) {
    event.target.src = 'default.svg'
  }

  renderCategoryName = () => {
    if (this.state.currentCategory) {
      return (
        <span className='header-highlight'>
           | {this.state.currentCategory}
        </span>
      )

    } else if (this.state.currentSearchTerm) {
      return (
        <span className='header-highlight'>
           | Search "{this.state.currentSearchTerm}"
        </span>
      ) 

    } else {
      return
    }
  }

  submitNewCategory = (categoryType) => {
      if (categoryType.trim().length === 0) return
      
      $.ajax({
        url: '/categories', 
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          category: categoryType,
        }),
        xhrFields: {
          withCredentials: true,
        },
        crossDomain: true,
        success: (result) => {
          this.getQuestions()
          return;
        },
        error: (error) => {
          alert('Unable to add category. Please try your request again');
          return;
        },
      })     

  }
  
  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            className='category-header'
            onClick={() => {
              this.selectPage(1)
            }}
          >
            Categories
          </h2>

          <AddCategory submitCategory={this.submitNewCategory}/>

          <ul className='category-ul'>
            {Object.keys(this.state.categories).map((id) => (
              <li
                className={`category-item ${this.state.categories[id] === this.state.currentCategory ? 'selected' : ''}`}
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
              >
                <img
                  onError={this.provideDefaultImgUrl}
                  className='category'
                  alt={`${this.state.categories[id].toLowerCase()}`}
                  src={`${this.state.categories[id].toLowerCase()}.svg`}
                />
                {this.state.categories[id]}
              </li>
            ))}
          </ul>

          <Search submitSearch={this.submitSearch} />
          
        </div>
        <div className='questions-list'>
          <h2>Questions {this.renderCategoryName()}</h2>

          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}

          <div className='pagination-menu'>{this.createPagination()}</div>

        </div>
      </div>
    );
  }
}

export default QuestionView;
