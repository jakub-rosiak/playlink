import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import prettier from 'eslint-config-prettier';

/** @type {import('eslint').Linter.Config[]} */
export default [
	{
		ignores: ['.svelte-kit/', 'dist/', 'build/']
	},
	{
		languageOptions: {
			globals: {
				...globals.browser,
				...globals.node
			},
			ecmaVersion: 2022,
			sourceType: 'module'
		}
	},
	...svelte.configs['flat/recommended'],
	prettier,
	{
		rules: {
			'svelte/no-at-html-tags': 'warn',
			'svelte/no-navigation-without-resolve': 'off'
		}
	}
];
