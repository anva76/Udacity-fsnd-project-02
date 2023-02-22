import React, { Component } from 'react';

class AddCategory extends Component {
  state = {
    newCategory: '',
  };

  formSubmit = (e) => {
    e.preventDefault()
    if (this.state.newCategory.trim().length !== 0 ) {
        this.props.submitCategory(this.state.newCategory)
        this.newCategoryInp.value = ''
    }
  };

  handleAddCategoryChange = () => {
    this.setState({
      newCategory: this.newCategoryInp.value,
    });
  }

  render() {
    return (
      <form className='category-snippet-holder' onSubmit={this.formSubmit}>
        <input
          className='category-input'
          placeholder='New category'
          ref={(input) => (this.newCategoryInp = input)}
          onChange={this.handleAddCategoryChange}
        />
        <button type='submit' className='category-button'>+</button>
      </form>
 
    )
  }
}

export default AddCategory
