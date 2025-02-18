import React from 'react';

export interface SelectorProps {
  id: string;
  label: string;
  options: string[];
}

export default function Selector(props: SelectorProps) {
  return (
    <div className='flex flex-row'>
      <label htmlFor={props.id} className='bg-blue-950 px-2 py-0.5 text-white'>{props.label}</label>
      <select id={props.id} className='px-2 py-1'>
        {props.options.map((option) => (
          <option key={option}>{option}</option>
        ))}
      </select>
    </div>
  );
}