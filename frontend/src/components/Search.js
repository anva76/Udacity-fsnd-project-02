import React, { Component } from 'react';

class Search extends Component {
  state = {
    query: '',
  };

  getInfo = (event) => {
    event.preventDefault();
    if (this.state.query.trim().length !== 0 ) {
        this.props.submitSearch(this.state.query)
    }
  };

  handleInputChange = () => {
      this.setState({
        query: this.search.value,
      });
  };

  render() {
    return (
      <form onSubmit={this.getInfo} className='search-form'>
        <input
          className='search-input'
          placeholder='Search questions...'
          ref={(input) => (this.search = input)}
          onChange={this.handleInputChange}
        />
        <button type='submit' className='search-button'>
          <img
              className='search-icon'
              alt='Search'
              src='search-icon.svg'
          />          
        </button>
      </form>
    );
  }
}

export default Search;
