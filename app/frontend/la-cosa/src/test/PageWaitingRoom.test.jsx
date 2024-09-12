import React from 'react';
import { render} from '@testing-library/react';
import PageWaitingRoom from '../pages/PageWaitingRoom'
import { MemoryRouter } from 'react-router-dom';


describe('PageWaitingRoom Component',()=>{
    test('Renderizada sin errores',()=>{
        render(
            <MemoryRouter>
                <PageWaitingRoom></PageWaitingRoom>
            </MemoryRouter>
        )
    })
})

