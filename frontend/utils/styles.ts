// primary | secondary
export const themes = {
  primary: {
    bg: 'bg-light-primary-bg dark:bg-dark-primary-bg',
    'disabled:bg':
      'disabled:bg-light-primary-bg disabled:dark:bg-dark-primary-bg',
    'bg-flipped': 'bg-dark-primary-bg dark:bg-light-primary-bg',
    'hover:bg-flipped':
      'hover:bg-dark-primary-bg dark:hover:bg-light-primary-bg',
    'bg-active': 'bg-light-primary-bg-active dark:bg-dark-primary-bg-active',
    ring: 'ring-light-primary-ring dark:ring-dark-primary-ring',
    border: 'border-light-primary-border dark:border-dark-primary-border',
    'border-active':
      'border-light-primary-border-active dark:border-dark-primary-border-active',
    'hover:border-active':
      'hover:border-light-primary-border-active dark:hover:border-dark-primary-border-active',
    'focus:border-active':
      'focus:border-light-primary-border-active dark:focus:border-dark-primary-border-active',
      'focus-within:border-active':
      'focus-within:border-light-primary-border-active dark:focus-within:border-dark-primary-border-active',
    text: 'text-light-primary-text dark:text-dark-primary-text',
    'disabled:text':
      'disabled:text-light-primary-text disabled:dark:text-dark-primary-text',
    'text-active':
      'text-light-primary-text-active dark:text-dark-primary-text-active',
    'text-flipped': 'text-dark-primary-text dark:text-light-primary-text',
    'hover:text-flipped':
      'hover:text-dark-primary-text dark:hover:text-light-primary-text',
    'hover:text-active':
      'hover:text-light-primary-text-active dark:hover:text-dark-primary-text-active',
    divide:
      'divide-light-primary-border-divide dark:divide-dark-primary-border-divide',
    shadow:
      'shadow-light-primary-border-active/5 dark:shadow-dark-primary-border-active/5',
  },
  secondary: {
    bg: 'bg-light-secondary-bg dark:bg-dark-secondary-bg',
    'disabled:bg':
      'disabled:bg-light-secondary-bg disabled:dark:bg-dark-secondary-bg',
    'bg-flipped': 'bg-dark-secondary-bg dark:bg-light-secondary-bg',
    'hover:bg-flipped':
      'hover:bg-dark-secondary-bg dark:hover:bg-light-secondary-bg',
    'bg-active':
      'bg-light-secondary-bg-active dark:bg-dark-secondary-bg-active',
    ring: 'ring-light-secondary-ring dark:ring-dark-secondary-ring',
    border: 'border-light-secondary-border dark:border-dark-secondary-border',
    'border-active':
      'border-light-secondary-border-active dark:border-dark-secondary-border-active',
    'hover:border-active':
      'hover:border-light-secondary-border-active dark:hover:border-dark-secondary-border-active',
    'focus:border-active':
      'focus:border-light-secondary-border-active dark:focus:border-dark-secondary-border-active',
      'focus-within:border-active':
      'focus-within:border-light-secondary-border-active dark:focus-within:border-dark-secondary-border-active',
    text: 'text-light-secondary-text dark:text-dark-secondary-text',
    'disabled:text':
      'disabled:text-light-secondary-text disabled:dark:text-dark-secondary-text',
    'text-active':
      'text-light-secondary-text-active dark:text-dark-secondary-text-active',
    'text-flipped': 'text-dark-secondary-text dark:text-light-secondary-text',
    'hover:text-flipped':
      'hover:text-dark-secondary-text dark:hover:text-light-secondary-text',
    'hover:text-active':
      'hover:text-light-secondary-text-active dark:hover:text-dark-secondary-text-active',
    divide:
      'divide-light-secondary-border-divide dark:divide-dark-secondary-border-divide',
    shadow:
      'shadow-light-secondary-border-active/10 dark:shadow-dark-secondary-border-active/10',
  },
} as const;
