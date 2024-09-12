import React from "react";
import { render } from "@testing-library/react";
import PageCreateGame from '../pages/PageCreateGame'
import { MemoryRouter } from 'react-router-dom';


describe('PageCreateGame Component',()=>{
  test('Renderiza sin errores',()=>{
    render(
        <MemoryRouter> 
        <PageCreateGame />
      </MemoryRouter>
  
    )
})
})


