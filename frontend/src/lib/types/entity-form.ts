export type FieldType = 'text' | 'number' | 'select';

export interface SelectOption {
	value: string | number;
	label: string;
}

export interface FieldConfig {
	name: string;
	label: string;
	type: FieldType;
	
	placeholder?: string;
	required?: boolean;
	options?: SelectOption[];
}

export interface EntityFormConfig {
	title: string;
	subtitle: string;
	fields: FieldConfig[];
	cancelHref: string;
}
