import React from 'react';
import { render, screen } from '@testing-library/react';
import PageJoinGame from '../pages/PageJoinGame';
import { MemoryRouter } from 'react-router-dom';

describe('PageJoinGame Component',()=>{
  test('Renderiza sin errores', () => {
    render(
    <MemoryRouter>
        <PageJoinGame></PageJoinGame>
    </MemoryRouter>
   )
  });
})



