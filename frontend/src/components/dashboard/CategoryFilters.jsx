import React from 'react'

const categories = [
  'All Categories',
  'Grant Help',
  'Fund Question',
  'Giving Portal Issue',
  'Advisor Request',
  'Scholarship',
  'Corporate Giving',
  'Unique Asset',
]

function CategoryFilters({ selectedCategory, onCategoryChange }) {
  return (
    <div className="chip-row" role="tablist" aria-label="Request categories">
      {categories.map((category) => {
        const isActive = selectedCategory === category

        return (
          <button
            key={category}
            type="button"
            className={`chip${isActive ? ' is-active' : ''}`}
            onClick={() => onCategoryChange(category)}
          >
            {category}
          </button>
        )
      })}
    </div>
  )
}

export default CategoryFilters
